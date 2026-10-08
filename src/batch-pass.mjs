const COOKIE = "sfn_batch_pass";
const ORDER_ID = /^[a-f0-9]{32}$/;
const TOKEN = /^[A-Za-z0-9_-]{43}$/;
const PASS_DAYS = 30;
const textEncoder = new TextEncoder();

function json(data, status = 200) {
  return Response.json(data, { status, headers: { "Cache-Control": "private, no-store", "X-Robots-Tag": "noindex, nofollow" } });
}

function hex(bytes) {
  return [...bytes].map(byte => byte.toString(16).padStart(2, "0")).join("");
}

function randomToken() {
  return btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(32))))
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function boundedText(request, maxBytes) {
  const reader = request.body?.getReader();
  if (!reader) return "";
  const chunks = [];
  let length = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > maxBytes) return null;
      chunks.push(value);
    }
    const bytes = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    return new TextDecoder().decode(bytes);
  } finally { reader.cancel().catch(() => {}); }
}

async function tokenHash(token) {
  return hex(new Uint8Array(await crypto.subtle.digest("SHA-256", textEncoder.encode(token))));
}

function cookieFrom(request) {
  const match = (request.headers.get("Cookie") || "").match(/(?:^|;\s*)sfn_batch_pass=([a-f0-9]{32})\.([A-Za-z0-9_-]{43})(?:;|$)/);
  return match && ORDER_ID.test(match[1]) && TOKEN.test(match[2]) ? { orderId: match[1], token: match[2] } : null;
}

function store(env, orderId) {
  return env.BATCH_PASSES.getByName(orderId);
}

async function storeCall(env, orderId, path, data) {
  const response = await store(env, orderId).fetch(`https://batch.internal${path}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error(`Batch pass store error: ${response.status}`);
  return response.json();
}

export class BatchPassStore {
  constructor(ctx) { this.ctx = ctx; }

  async fetch(request) {
    const path = new URL(request.url).pathname;
    const body = await request.json().catch(() => ({}));
    const storage = this.ctx.storage;
    if (path === "/create") {
      if (await storage.get("order")) return json({ error: "Order already exists" }, 409);
      await storage.put("order", { tokenHash: body.tokenHash, created: Date.now(), status: "pending", sessionIds: [] });
      await storage.setAlarm(Date.now() + 45 * 24 * 3600 * 1000);
      return json({ ok: true });
    }
    const order = await storage.get("order");
    if (!order) return json({ error: "Order not found" }, 404);
    if (path === "/session") {
      if (order.status !== "pending" || order.sessionIds.length >= 5) return json({ error: "Checkout attempts exhausted" }, 409);
      order.sessionIds.push(body.sessionId);
      await storage.put("order", order);
      return json({ ok: true });
    }
    if (path === "/status") {
      const submitted = await tokenHash(String(body.token || ""));
      if (submitted !== order.tokenHash) return json({ error: "Pass not found" }, 404);
      const active = order.status === "paid" && order.expiresAt > Date.now();
      return json({ active, pending: order.status === "pending", expiresAt: active ? order.expiresAt : null });
    }
    if (path === "/paid") {
      if (!order.sessionIds.length) return json({ error: "Checkout session is not ready" }, 503);
      if (!body.sessionId || !order.sessionIds.includes(body.sessionId)) return json({ error: "Wrong checkout session" }, 409);
      if (order.status === "revoked") return json({ ok: true });
      if (order.status === "paid") return json({ ok: true });
      order.status = "paid";
      order.paymentId = body.paymentId;
      order.expiresAt = Date.now() + PASS_DAYS * 24 * 3600 * 1000;
      await storage.put("order", order);
      return json({ ok: true });
    }
    if (path === "/revoke") {
      if (order.paymentId !== body.paymentId) return json({ error: "Payment mismatch" }, 409);
      order.status = "revoked";
      await storage.put("order", order);
      return json({ ok: true });
    }
    return json({ error: "Not found" }, 404);
  }

  async alarm() { await this.ctx.storage.deleteAll(); }
}

export function batchPassConfigured(env) {
  return env.BATCH_PASS_ENABLED === "true" && Boolean(env.DODO_API_KEY && env.DODO_BATCH_PRODUCT_ID && env.DODO_WEBHOOK_SECRET && env.BATCH_TIER_SIGNING_KEY && env.BATCH_PASSES);
}

export async function signedBatchTier(env) {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const key = await crypto.subtle.importKey("raw", textEncoder.encode(env.BATCH_TIER_SIGNING_KEY),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const signature = await crypto.subtle.sign("HMAC", key, textEncoder.encode(`${timestamp}:pro`));
  return { timestamp, signature: hex(new Uint8Array(signature)) };
}

export async function passStatus(request, env) {
  const available = batchPassConfigured(env);
  const buyer = available ? cookieFrom(request) : null;
  if (!buyer) return json({ available, active: false, pending: false, freeFiles: 5, paidFiles: 10 });
  try {
    const result = await storeCall(env, buyer.orderId, "/status", { token: buyer.token });
    return json({ available, ...result, freeFiles: 5, paidFiles: 10 });
  } catch {
    return json({ available, active: false, pending: false, freeFiles: 5, paidFiles: 10 });
  }
}

export async function batchRecoveryCode(request, env) {
  if (!batchPassConfigured(env)) return json({ error: "Batch Pro is unavailable." }, 503);
  if (request.headers.get("Origin") !== new URL(request.url).origin) return json({ error: "Invalid request." }, 403);
  const buyer = cookieFrom(request);
  if (!buyer || !await hasBatchPass(request, env)) return json({ error: "No active Batch Pro pass in this browser." }, 403);
  return json({ recoveryCode: `${buyer.orderId}.${buyer.token}` });
}

export async function redeemBatchPass(request, env) {
  if (!batchPassConfigured(env)) return json({ error: "Batch Pro is unavailable." }, 503);
  if (request.headers.get("Origin") !== new URL(request.url).origin) return json({ error: "Invalid request." }, 403);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const { success } = await env.EVENT_LIMIT.limit({ key: `batch-redeem:${ip}` });
  if (!success) return json({ error: "Too many attempts. Try again shortly." }, 429);
  if (Number(request.headers.get("content-length") || 0) > 200) return json({ error: "Invalid recovery code." }, 400);
  const raw = await boundedText(request, 200);
  if (raw === null) return json({ error: "Invalid recovery code." }, 400);
  let input;
  try { input = JSON.parse(raw); } catch { return json({ error: "Invalid recovery code." }, 400); }
  const match = typeof input.code === "string" ? input.code.trim().match(/^([a-f0-9]{32})\.([A-Za-z0-9_-]{43})$/) : null;
  if (!match) return json({ error: "Invalid recovery code." }, 400);
  try {
    const result = await storeCall(env, match[1], "/status", { token: match[2] });
    if (!result.active) return json({ error: "This pass is unavailable or expired." }, 403);
  } catch { return json({ error: "This pass was not found." }, 404); }
  const result = json({ active: true });
  result.headers.append("Set-Cookie", `${COOKIE}=${match[1]}.${match[2]}; Max-Age=${(PASS_DAYS + 2) * 86400}; Path=/; Secure; HttpOnly; SameSite=Lax`);
  return result;
}

export async function activeBatchOrder(request, env) {
  if (!batchPassConfigured(env)) return false;
  const buyer = cookieFrom(request);
  if (!buyer) return false;
  try {
    const result = await storeCall(env, buyer.orderId, "/status", { token: buyer.token });
    return result.active === true ? buyer.orderId : null;
  } catch { return false; }
}

export async function hasBatchPass(request, env) {
  return Boolean(await activeBatchOrder(request, env));
}

export async function startBatchCheckout(request, env) {
  if (!batchPassConfigured(env)) return json({ error: "Checkout is not available yet." }, 503);
  const origin = new URL(request.url).origin;
  if (request.headers.get("Origin") !== origin) return json({ error: "Invalid checkout request." }, 403);
  if (await hasBatchPass(request, env)) return json({ error: "Your batch pass is already active." }, 409);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  const { success } = await env.DOWNLOAD_LIMIT.limit({ key: `batch-checkout:${ip}` });
  if (!success) return json({ error: "Too many checkout attempts. Try again shortly." }, 429);
  let buyer = cookieFrom(request);
  if (buyer) {
    try {
      const previous = await storeCall(env, buyer.orderId, "/status", { token: buyer.token });
      if (!previous.pending) buyer = null;
    } catch { buyer = null; }
  }
  const orderId = buyer?.orderId || hex(crypto.getRandomValues(new Uint8Array(16)));
  const token = buyer?.token || randomToken();
  if (!buyer) await storeCall(env, orderId, "/create", { tokenHash: await tokenHash(token) });
  const apiBase = env.DODO_MODE === "live" ? "https://live.dodopayments.com" : "https://test.dodopayments.com";
  let checkout;
  try {
    const response = await fetch(`${apiBase}/checkouts`, {
      method: "POST",
      headers: { Authorization: `Bearer ${env.DODO_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        product_cart: [{ product_id: env.DODO_BATCH_PRODUCT_ID, quantity: 1 }],
        metadata: { batch_order_id: orderId },
        return_url: `${origin}/batch-image-converter?checkout=returned`,
        cancel_url: `${origin}/batch-image-converter?checkout=cancelled`,
      }),
    });
    if (!response.ok) throw new Error(`Dodo checkout request failed: ${response.status}`);
    checkout = await response.json();
    const target = new URL(checkout.checkout_url);
    if (target.protocol !== "https:" || !(target.hostname === "dodopayments.com" || target.hostname.endsWith(".dodopayments.com"))) throw new Error("Unexpected checkout URL");
    if (!/^cks_[A-Za-z0-9]+$/.test(checkout.session_id || "")) throw new Error("Unexpected checkout session");
    await storeCall(env, orderId, "/session", { sessionId: checkout.session_id });
  } catch (error) {
    console.error("Batch checkout unavailable", error);
    return json({ error: "Checkout could not start. Please try again later." }, 502);
  }
  const result = json({ checkoutUrl: checkout.checkout_url });
  result.headers.append("Set-Cookie", `${COOKIE}=${orderId}.${token}; Max-Age=${(PASS_DAYS + 2) * 86400}; Path=/; Secure; HttpOnly; SameSite=Lax`);
  return result;
}

export async function verifyDodoWebhook(request, secret, rawBody) {
  const id = request.headers.get("webhook-id") || "";
  const timestamp = request.headers.get("webhook-timestamp") || "";
  const signatures = (request.headers.get("webhook-signature") || "").split(" ");
  if (!/^[-_A-Za-z0-9]{1,128}$/.test(id) || !/^\d{10}$/.test(timestamp) || Math.abs(Date.now() / 1000 - Number(timestamp)) > 300 || !secret?.startsWith("whsec_")) return false;
  let keyBytes;
  try { keyBytes = Uint8Array.from(atob(secret.slice(6)), char => char.charCodeAt(0)); }
  catch { return false; }
  const key = await crypto.subtle.importKey("raw", keyBytes, { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
  const signed = textEncoder.encode(`${id}.${timestamp}.${rawBody}`);
  for (const entry of signatures) {
    if (!entry.startsWith("v1,")) continue;
    try {
      const signature = Uint8Array.from(atob(entry.slice(3)), char => char.charCodeAt(0));
      if (signature.length === 32 && await crypto.subtle.verify("HMAC", key, signature, signed)) return true;
    } catch { /* Ignore malformed or unsupported signatures. */ }
  }
  return false;
}

async function fetchDodoPayment(env, paymentId) {
  const apiBase = env.DODO_MODE === "live" ? "https://live.dodopayments.com" : "https://test.dodopayments.com";
  const response = await fetch(`${apiBase}/payments/${encodeURIComponent(paymentId)}`, {
    headers: { Authorization: `Bearer ${env.DODO_API_KEY}` },
  });
  if (!response.ok) throw new Error(`Payment lookup failed: ${response.status}`);
  return response.json();
}

export async function batchWebhook(request, env) {
  if (!batchPassConfigured(env)) return new Response("Unavailable", { status: 503 });
  if (Number(request.headers.get("content-length") || 0) > 65536) return new Response("Too large", { status: 413 });
  const rawBody = await boundedText(request, 65536);
  if (rawBody === null) return new Response("Too large", { status: 413 });
  if (!await verifyDodoWebhook(request, env.DODO_WEBHOOK_SECRET, rawBody)) return new Response("Invalid signature", { status: 400 });
  let event;
  try { event = JSON.parse(rawBody); } catch { return new Response("Invalid payload", { status: 400 }); }
  if (event.type === "payment.succeeded") {
    const data = event.data || {};
    if (!/^pay_[A-Za-z0-9]+$/.test(data.payment_id || "")) return new Response("Ignored", { status: 200 });
    try {
      const payment = await fetchDodoPayment(env, data.payment_id);
      const orderId = payment.metadata?.batch_order_id;
      if (payment.status !== "succeeded" || payment.payment_id !== data.payment_id ||
          !ORDER_ID.test(orderId || "") ||
          !/^cks_[A-Za-z0-9]+$/.test(payment.checkout_session_id || "") ||
          payment.product_cart?.length !== 1 ||
          payment.product_cart[0].product_id !== env.DODO_BATCH_PRODUCT_ID ||
          payment.product_cart[0].quantity !== 1) return new Response("Ignored", { status: 200 });
      await storeCall(env, orderId, "/paid", { paymentId: data.payment_id, sessionId: payment.checkout_session_id });
    } catch (error) {
      console.error("Batch pass fulfillment failed", error);
      return new Response("Try again", { status: 503 });
    }
  } else if (event.type === "refund.succeeded" || event.type === "dispute.lost") {
    const paymentId = event.data?.payment_id;
    if (!/^pay_[A-Za-z0-9]+$/.test(paymentId || "")) return new Response("Ignored", { status: 200 });
    try {
      const payment = await fetchDodoPayment(env, paymentId);
      const orderId = payment.metadata?.batch_order_id;
      if (ORDER_ID.test(orderId || "")) await storeCall(env, orderId, "/revoke", { paymentId });
    } catch (error) {
      console.error("Batch pass revocation failed", error);
      return new Response("Try again", { status: 503 });
    }
  }
  return new Response("OK", { status: 200 });
}
