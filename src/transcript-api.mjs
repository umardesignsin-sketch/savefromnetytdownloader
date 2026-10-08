import { verifyDodoWebhook } from "./batch-pass.mjs";

const COOKIE = "sfn_developer";
const ACCOUNT = /^[a-f0-9]{32}$/;
const TOKEN = /^[A-Za-z0-9_-]{43}$/;
const SUBSCRIPTION = /^sub_[A-Za-z0-9]+$/;
const SESSION = /^cks_[A-Za-z0-9]+$/;
const LIMIT = 1000;
const encoder = new TextEncoder();

function json(value, status = 200, extra = {}) {
  return Response.json(value, { status, headers: { "Cache-Control": "private, no-store", "X-Robots-Tag": "noindex, nofollow", ...extra } });
}
function hex(bytes) { return [...bytes].map(byte => byte.toString(16).padStart(2, "0")).join(""); }
function randomToken() {
  return btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(32))))
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
async function hash(value) { return hex(new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(value)))); }
function credentials(request) {
  const match = (request.headers.get("Cookie") || "").match(/(?:^|;\s*)sfn_developer=([a-f0-9]{32})\.([A-Za-z0-9_-]{43})(?:;|$)/);
  return match ? { id: match[1], token: match[2] } : null;
}
function apiKey(request) {
  const match = (request.headers.get("Authorization") || "").match(/^Bearer (sfn_([a-f0-9]{32})_([A-Za-z0-9_-]{43}))$/);
  return match ? { id: match[2], key: match[1] } : null;
}
function account(env, id) { return env.TRANSCRIPT_ACCOUNTS.getByName(id); }
async function call(env, id, path, value = {}) {
  const response = await account(env, id).fetch(`https://developer.internal${path}`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(value),
  });
  const result = await response.json();
  return { result, status: response.status };
}
function sameOrigin(request) { return request.headers.get("Origin") === new URL(request.url).origin; }
function configured(env) {
  return Boolean(env.TRANSCRIPT_ACCOUNTS && env.DODO_API_KEY && env.DODO_TRANSCRIPT_PRODUCT_ID && env.DODO_TRANSCRIPT_WEBHOOK_SECRET);
}
function checkoutBase(env) { return env.DODO_MODE === "live" ? "https://live.dodopayments.com" : "https://test.dodopayments.com"; }
async function dodoGet(env, path) {
  const response = await fetch(`${checkoutBase(env)}${path}`, { headers: { Authorization: `Bearer ${env.DODO_API_KEY}` } });
  if (!response.ok) throw new Error(`Dodo lookup failed: ${response.status}`);
  return response.json();
}
async function boundedText(request, max = 65536) {
  if (Number(request.headers.get("Content-Length") || 0) > max) return null;
  const reader = request.body?.getReader();
  if (!reader) return "";
  const chunks = []; let length = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.byteLength;
      if (length > max) return null;
      chunks.push(value);
    }
    const bytes = new Uint8Array(length); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    return new TextDecoder().decode(bytes);
  } finally { reader.cancel().catch(() => {}); }
}

// Each account ID maps to one serial Durable Object. No global key index or raw API key is stored.
export class TranscriptAccountStore {
  constructor(ctx) { this.ctx = ctx; }
  async fetch(request) {
    const path = new URL(request.url).pathname;
    const body = await request.json().catch(() => ({}));
    const storage = this.ctx.storage;
    if (path === "/create") {
      if (await storage.get("account")) return json({ error: "Account exists." }, 409);
      await storage.put("account", { ownerHash: body.ownerHash, keyHash: null, status: "pending", sessionIds: [],
        subscriptionId: null, periodStart: 0, periodEnd: 0, used: 0, pending: {}, minute: 0, calls: 0 });
      await storage.setAlarm(Date.now() + 45 * 86400000);
      return json({ ok: true });
    }
    const state = await storage.get("account");
    if (!state) return json({ error: "Account not found." }, 404);
    const owner = body.ownerHash && body.ownerHash === state.ownerHash;
    const key = body.keyHash && body.keyHash === state.keyHash;
    if (path === "/session") {
      if (!owner || !SESSION.test(body.sessionId || "") || state.sessionIds.length >= 5) return json({ error: "Checkout unavailable." }, 403);
      state.sessionIds.push(body.sessionId);
    } else if (path === "/status") {
      if (!owner) return json({ error: "Invalid account." }, 403);
      return json({ status: state.status, active: state.status === "active" && state.periodEnd > Date.now(),
        used: state.used, limit: LIMIT, remaining: Math.max(0, LIMIT - state.used),
        periodEnd: state.periodEnd || null, hasKey: Boolean(state.keyHash) });
    } else if (path === "/subscription") {
      if (!owner || !state.subscriptionId) return json({ error: "Subscription not found." }, 403);
      return json({ subscriptionId: state.subscriptionId });
    } else if (path === "/key") {
      if (!owner || state.status !== "active" || state.periodEnd <= Date.now()) return json({ error: "No active subscription." }, 403);
      state.pending = Object.fromEntries(Object.entries(state.pending).filter(([, at]) => Date.now() - at < 180000));
      if (Object.keys(state.pending).length) return json({ error: "Wait for active requests to finish before rotating the key." }, 409);
      state.keyHash = body.keyHash;
    } else if (path === "/sync") {
      if (!SUBSCRIPTION.test(body.subscriptionId || "") || !state.sessionIds.includes(body.sessionId) && state.subscriptionId !== body.subscriptionId) {
        return json({ error: "Subscription mismatch." }, 409);
      }
      if (state.subscriptionId && state.subscriptionId !== body.subscriptionId) return json({ error: "Subscription mismatch." }, 409);
      state.subscriptionId = body.subscriptionId;
      if (body.status === "active" && body.paymentConfirmed === true && Number.isFinite(body.periodEnd) && body.periodEnd > Date.now()) {
        if (Number.isFinite(body.periodStart) && body.periodStart > state.periodStart) {
          state.periodStart = body.periodStart;
          state.used = 0;
          state.pending = {};
        }
        state.status = "active";
        state.periodEnd = body.periodEnd;
      } else if (["cancelled", "expired", "failed", "on_hold", "paused"].includes(body.status)) {
        state.status = body.status;
        state.pending = {};
      }
    } else if (path === "/reserve") {
      if (!key) return json({ code: "invalid_api_key", error: "Invalid API key." }, 401);
      if (state.status !== "active" || state.periodEnd <= Date.now()) return json({ code: "subscription_inactive", error: "Subscription inactive or renewal pending." }, 403);
      const now = Date.now();
      state.pending = Object.fromEntries(Object.entries(state.pending).filter(([, at]) => now - at < 180000));
      if (state.used + Object.keys(state.pending).length >= LIMIT) return json({ code: "quota_exceeded", error: "Monthly transcript allowance used." }, 429);
      if (Object.keys(state.pending).length >= 2) return json({ code: "too_many_concurrent_requests", error: "Two transcript requests are already processing." }, 429);
      const minute = Math.floor(now / 60000);
      if (state.minute !== minute) { state.minute = minute; state.calls = 0; }
      if (state.calls >= 4) return json({ code: "rate_limit_exceeded", error: "Try again in a minute." }, 429);
      state.calls++;
      state.pending[body.reservation] = now;
    } else if (path === "/settle") {
      if (state.pending[body.reservation]) {
        delete state.pending[body.reservation];
        if (body.success) state.used++;
      }
    } else return json({ error: "Not found." }, 404);
    await storage.put("account", state);
    return json({ ok: true });
  }

  async alarm() {
    const state = await this.ctx.storage.get("account");
    if (state?.status === "pending") await this.ctx.storage.deleteAll();
  }
}

export async function developerStatus(request, env) {
  const buyer = credentials(request);
  if (!buyer) return json({ available: configured(env), active: false, status: "signed_out", limit: LIMIT });
  const { result, status } = await call(env, buyer.id, "/status", { ownerHash: await hash(buyer.token) });
  return status === 200 ? json({ available: configured(env), ...result }) : json({ available: configured(env), active: false, status: "signed_out", limit: LIMIT });
}
export async function developerCheckout(request, env) {
  if (!configured(env)) return json({ error: "Subscription checkout is not configured yet." }, 503);
  if (!sameOrigin(request)) return json({ error: "Invalid checkout request." }, 403);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (!(await env.EVENT_LIMIT.limit({ key: `developer-checkout:${ip}` })).success) return json({ error: "Too many checkout attempts." }, 429);
  let buyer = credentials(request);
  if (buyer) {
    const prior = await call(env, buyer.id, "/status", { ownerHash: await hash(buyer.token) });
    if (prior.status !== 200 || prior.result.status !== "pending") buyer = null;
  }
  if (!buyer) {
    buyer = { id: hex(crypto.getRandomValues(new Uint8Array(16))), token: randomToken() };
    await call(env, buyer.id, "/create", { ownerHash: await hash(buyer.token) });
  }
  try {
    const response = await fetch(`${checkoutBase(env)}/checkouts`, {
      method: "POST", headers: { Authorization: `Bearer ${env.DODO_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ product_cart: [{ product_id: env.DODO_TRANSCRIPT_PRODUCT_ID, quantity: 1 }],
        metadata: { transcript_account_id: buyer.id },
        return_url: `${new URL(request.url).origin}/developers?checkout=returned`,
        cancel_url: `${new URL(request.url).origin}/developers?checkout=cancelled` }),
    });
    if (!response.ok) throw new Error(`Dodo checkout failed: ${response.status}`);
    const checkout = await response.json();
    const target = new URL(checkout.checkout_url);
    if (target.protocol !== "https:" || !(target.hostname === "dodopayments.com" || target.hostname.endsWith(".dodopayments.com")) || !SESSION.test(checkout.session_id)) throw new Error("Unexpected checkout response");
    const saved = await call(env, buyer.id, "/session", { ownerHash: await hash(buyer.token), sessionId: checkout.session_id });
    if (saved.status !== 200) throw new Error("Checkout session could not be saved");
    const result = json({ checkoutUrl: checkout.checkout_url });
    result.headers.append("Set-Cookie", `${COOKIE}=${buyer.id}.${buyer.token}; Max-Age=34560000; Path=/; Secure; HttpOnly; SameSite=Lax`);
    return result;
  } catch (error) {
    console.error("Developer checkout unavailable", error);
    return json({ error: "Checkout could not start. Please try later." }, 502);
  }
}
export async function developerRecovery(request, env) {
  if (!sameOrigin(request)) return json({ error: "Invalid request." }, 403);
  const buyer = credentials(request);
  if (!buyer) return json({ error: "No developer account in this browser." }, 403);
  const { status } = await call(env, buyer.id, "/status", { ownerHash: await hash(buyer.token) });
  return status === 200 ? json({ recoveryCode: `${buyer.id}.${buyer.token}` }) : json({ error: "Account unavailable." }, 403);
}
export async function developerRedeem(request, env) {
  if (!sameOrigin(request)) return json({ error: "Invalid request." }, 403);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (!(await env.EVENT_LIMIT.limit({ key: `developer-redeem:${ip}` })).success) return json({ error: "Too many attempts." }, 429);
  const raw = await boundedText(request, 200);
  let code;
  try { code = JSON.parse(raw).code; } catch { return json({ error: "Invalid recovery code." }, 400); }
  const match = typeof code === "string" && code.trim().match(/^([a-f0-9]{32})\.([A-Za-z0-9_-]{43})$/);
  if (!match) return json({ error: "Invalid recovery code." }, 400);
  const { status } = await call(env, match[1], "/status", { ownerHash: await hash(match[2]) });
  if (status !== 200) return json({ error: "Account not found." }, 404);
  const result = json({ ok: true });
  result.headers.append("Set-Cookie", `${COOKIE}=${match[1]}.${match[2]}; Max-Age=34560000; Path=/; Secure; HttpOnly; SameSite=Lax`);
  return result;
}
export async function developerKey(request, env) {
  if (!sameOrigin(request)) return json({ error: "Invalid request." }, 403);
  const buyer = credentials(request);
  if (!buyer) return json({ error: "Sign in with your recovery code." }, 403);
  const key = `sfn_${buyer.id}_${randomToken()}`;
  const { status, result } = await call(env, buyer.id, "/key", { ownerHash: await hash(buyer.token), keyHash: await hash(key) });
  return status === 200 ? json({ apiKey: key }) : json(result, status);
}
export async function developerPortal(request, env) {
  if (!configured(env)) return json({ error: "Billing is unavailable." }, 503);
  if (!sameOrigin(request)) return json({ error: "Invalid request." }, 403);
  const buyer = credentials(request);
  if (!buyer) return json({ error: "Restore your account first." }, 403);
  const owned = await call(env, buyer.id, "/subscription", { ownerHash: await hash(buyer.token) });
  if (owned.status !== 200) return json({ error: "Subscription not found." }, 403);
  try {
    const subscription = await dodoGet(env, `/subscriptions/${owned.result.subscriptionId}`);
    if (subscription.subscription_id !== owned.result.subscriptionId || subscription.metadata?.transcript_account_id !== buyer.id ||
        subscription.product_id !== env.DODO_TRANSCRIPT_PRODUCT_ID || !/^cus_[A-Za-z0-9]+$/.test(subscription.customer?.customer_id || "")) {
      return json({ error: "Subscription unavailable." }, 403);
    }
    const returnUrl = encodeURIComponent(`${new URL(request.url).origin}/developers`);
    const response = await fetch(`${checkoutBase(env)}/customers/${subscription.customer.customer_id}/customer-portal/session?return_url=${returnUrl}`, {
      method: "POST", headers: { Authorization: `Bearer ${env.DODO_API_KEY}` },
    });
    if (!response.ok) throw new Error(`Portal request failed: ${response.status}`);
    const portal = await response.json();
    const target = new URL(portal.link);
    if (target.protocol !== "https:" || !(target.hostname === "dodopayments.com" || target.hostname.endsWith(".dodopayments.com"))) throw new Error("Unexpected portal URL");
    return json({ portalUrl: portal.link });
  } catch (error) {
    console.error("Developer portal unavailable", error);
    return json({ error: "Billing portal is unavailable. Please try again later." }, 502);
  }
}
export async function paidTranscript(request, env) {
  const headers = { "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" };
  if (request.method !== "POST") return json({ code: "method_not_allowed", error: "Use POST." }, 405, { Allow: "POST" });
  if (!/^application\/json(?:\s*;|$)/i.test(request.headers.get("Content-Type") || "")) return json({ code: "unsupported_media_type", error: "Send JSON." }, 415);
  if (Number(request.headers.get("Content-Length") || 0) > 4096) return json({ code: "request_too_large", error: "Request too large." }, 413);
  const raw = await boundedText(request, 4096);
  let input;
  try { input = JSON.parse(raw); } catch { return json({ code: "invalid_request", error: "Send a YouTube URL and optional language." }, 400); }
  if (typeof input?.url !== "string" || !input.url.trim() || input.url.length > 2048 ||
      (input.language !== undefined && (typeof input.language !== "string" || !/^[A-Za-z0-9-]{2,20}$/.test(input.language)))) {
    return json({ code: "invalid_request", error: "Send a YouTube URL and optional language." }, 400);
  }
  const client = apiKey(request);
  if (!client) return json({ code: "api_key_required", error: "Send Authorization: Bearer <API key>." }, 401);
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (!(await env.ANALYZE_LIMIT.limit({ key: `paid-transcript:${ip}` })).success) {
    return json({ code: "rate_limit_exceeded", error: "Too many requests. Try again in a minute." }, 429, { "Retry-After": "60" });
  }
  const reservation = randomToken();
  const reserved = await call(env, client.id, "/reserve", { keyHash: await hash(client.key), reservation });
  if (reserved.status === 404) return json({ code: "invalid_api_key", error: "Invalid API key." }, 401);
  if (reserved.status !== 200) return json(reserved.result, reserved.status, reserved.status === 429 ? { "Retry-After": "60" } : {});
  let response;
  try {
    const upstream = new Request(new URL("/api/transcript", request.url), {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(input),
    });
    response = await env.DOWNLOADER.getByName("multi-primary").fetch(upstream);
  } catch {
    response = json({ code: "source_unavailable", error: "Transcript service is unavailable. Try again later." }, 503);
  }
  try {
    const settled = await call(env, client.id, "/settle", { reservation, success: response.ok });
    if (settled.status !== 200) throw new Error("Metering failed");
  }
  catch { return json({ code: "metering_unavailable", error: "Usage could not be recorded. Please retry later." }, 503); }
  const output = new Headers(response.headers);
  for (const [key, value] of Object.entries(headers)) output.set(key, value);
  output.delete("Content-Length");
  return new Response(response.body, { status: response.status, headers: output });
}
export async function developerWebhook(request, env) {
  if (!configured(env)) return new Response("Unavailable", { status: 503 });
  const raw = await boundedText(request);
  if (raw === null) return new Response("Too large", { status: 413 });
  if (!await verifyDodoWebhook(request, env.DODO_TRANSCRIPT_WEBHOOK_SECRET, raw)) return new Response("Invalid signature", { status: 400 });
  let event;
  try { event = JSON.parse(raw); } catch { return new Response("Invalid payload", { status: 400 }); }
  const relevant = ["payment.succeeded", "subscription.active", "subscription.renewed", "subscription.updated", "subscription.on_hold", "subscription.failed", "subscription.cancelled", "subscription.expired", "subscription.paused", "refund.succeeded", "dispute.lost"];
  if (!relevant.includes(event.type)) return new Response("Ignored", { status: 200 });
  try {
    let payment = null;
    if (["payment.succeeded", "refund.succeeded", "dispute.lost"].includes(event.type)) {
      const paymentId = event.data?.payment_id;
      if (!/^pay_[A-Za-z0-9]+$/.test(paymentId || "")) return new Response("Ignored", { status: 200 });
      payment = await dodoGet(env, `/payments/${paymentId}`);
      if (payment.payment_id !== paymentId || !SUBSCRIPTION.test(payment.subscription_id || "")) return new Response("Ignored", { status: 200 });
    }
    const id = payment?.subscription_id || event.data?.subscription_id;
    if (!SUBSCRIPTION.test(id || "")) return new Response("Ignored", { status: 200 });
    const subscription = await dodoGet(env, `/subscriptions/${id}`);
    const accountId = subscription.metadata?.transcript_account_id || payment?.metadata?.transcript_account_id;
    if (subscription.subscription_id !== id || !ACCOUNT.test(accountId || "") || subscription.product_id !== env.DODO_TRANSCRIPT_PRODUCT_ID || subscription.quantity !== 1) return new Response("Ignored", { status: 200 });
    // Dodo's product_cart is for one-time items and can be null on subscription payments.
    // The fetched subscription above is the source of truth for product and quantity.
    if (payment && payment.subscription_id !== id) return new Response("Ignored", { status: 200 });
    const status = ["refund.succeeded", "dispute.lost"].includes(event.type) ? "cancelled" : subscription.status;
    const confirmed = (event.type === "payment.succeeded" && payment.status === "succeeded" && payment.total_amount > 0 && !payment.is_update_payment_method) || event.type === "subscription.renewed";
    const result = await call(env, accountId, "/sync", {
      subscriptionId: id, sessionId: payment?.checkout_session_id || "", status,
      paymentConfirmed: confirmed,
      periodStart: Date.parse(subscription.previous_billing_date), periodEnd: Date.parse(subscription.next_billing_date),
    });
    if (result.status === 409) return new Response("Ignored", { status: 200 });
    if (result.status !== 200) throw new Error(`Account sync failed: ${result.status}`);
  } catch (error) {
    console.error("Transcript subscription sync failed", error);
    return new Response("Try again", { status: 503 });
  }
  return new Response("OK", { status: 200 });
}
