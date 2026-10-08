import test from 'node:test';
import assert from 'node:assert/strict';
import { Buffer } from 'node:buffer';
import { BatchPassStore, batchRecoveryCode, batchWebhook, hasBatchPass, passStatus, redeemBatchPass, startBatchCheckout, verifyDodoWebhook } from '../src/batch-pass.mjs';

function testEnvironment() {
  const instances = new Map();
  const env = {
    BATCH_PASS_ENABLED: 'true', DODO_API_KEY: 'test-key', DODO_BATCH_PRODUCT_ID: 'pdt_batch',
    DODO_WEBHOOK_SECRET: `whsec_${Buffer.from('a'.repeat(32)).toString('base64')}`,
    BATCH_TIER_SIGNING_KEY: 'test-signing-key', DODO_MODE: 'test',
    EVENT_LIMIT: { limit: async () => ({ success: true }) },
    DOWNLOAD_LIMIT: { limit: async () => ({ success: true }) },
    BATCH_PASSES: { getByName(id) {
      if (!instances.has(id)) {
        const values = new Map();
        const storage = { get: async key => values.get(key), put: async (key, value) => values.set(key, value),
          setAlarm: async () => {}, deleteAll: async () => values.clear() };
        instances.set(id, new BatchPassStore({ storage }));
      }
      return { fetch: (url, init) => instances.get(id).fetch(new Request(url, init)) };
    } },
  };
  return env;
}

async function signedWebhook(env, body, valid = true) {
  const payload = JSON.stringify(body);
  const id = 'msg_batch_test';
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const key = await crypto.subtle.importKey('raw', Buffer.from(env.DODO_WEBHOOK_SECRET.slice(6), 'base64'),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const signature = Buffer.from(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(`${id}.${timestamp}.${payload}`))).toString('base64');
  return new Request('https://savefromnet.fun/api/batch-pass/webhook', { method: 'POST',
    headers: { 'webhook-id': id, 'webhook-timestamp': timestamp, 'webhook-signature': `v1,${valid ? signature : 'bad'}` }, body: payload });
}

test('checkout, signed fulfillment, entitlement, and refund', async () => {
  const env = testEnvironment();
  const originalFetch = globalThis.fetch;
  let orderId;
  let paymentProduct = 'pdt_batch';
  globalThis.fetch = async (url, init) => {
    if (String(url).endsWith('/checkouts')) {
      const body = JSON.parse(init.body);
      assert.equal(body.product_cart[0].product_id, 'pdt_batch');
      orderId = body.metadata.batch_order_id;
      return Response.json({ session_id: 'cks_test123', checkout_url: 'https://test.checkout.dodopayments.com/session/cks_test123' });
    }
    if (String(url).includes('/payments/')) return Response.json({
      payment_id: 'pay_test123', status: 'succeeded', metadata: { batch_order_id: orderId },
      checkout_session_id: 'cks_test123', product_cart: [{ product_id: paymentProduct, quantity: 1 }],
    });
    throw new Error(`Unexpected request: ${url}`);
  };
  try {
    const request = new Request('https://savefromnet.fun/api/batch-pass/checkout', { method: 'POST',
      headers: { Origin: 'https://savefromnet.fun', 'CF-Connecting-IP': '127.0.0.1' } });
    const checkout = await startBatchCheckout(request, env);
    assert.equal(checkout.status, 200);
    assert.equal((await checkout.json()).checkoutUrl, 'https://test.checkout.dodopayments.com/session/cks_test123');
    const cookie = checkout.headers.get('Set-Cookie').split(';')[0];
    const browser = new Request('https://savefromnet.fun/api/batch-pass/status', { headers: { Cookie: cookie } });
    assert.equal((await (await passStatus(browser, env)).json()).pending, true);
    assert.equal(await hasBatchPass(browser, env), false);
    const bad = await batchWebhook(await signedWebhook(env, { type: 'payment.succeeded', data: { metadata: { batch_order_id: orderId }, payment_id: 'pay_test123' } }, false), env);
    assert.equal(bad.status, 400);
    assert.equal(await hasBatchPass(browser, env), false);
    paymentProduct = 'pdt_other';
    const wrongProduct = await batchWebhook(await signedWebhook(env, { type: 'payment.succeeded', data: { payment_id: 'pay_test123' } }), env);
    assert.equal(wrongProduct.status, 200);
    assert.equal(await hasBatchPass(browser, env), false);
    paymentProduct = 'pdt_batch';
    const paid = await batchWebhook(await signedWebhook(env, { type: 'payment.succeeded', data: { metadata: { batch_order_id: orderId }, payment_id: 'pay_test123', checkout_session_id: 'cks_test123' } }), env);
    assert.equal(paid.status, 200);
    assert.equal(await hasBatchPass(browser, env), true);
    assert.equal((await (await passStatus(browser, env)).json()).paidFiles, 10);
    const recovery = await batchRecoveryCode(new Request('https://savefromnet.fun/api/batch-pass/recovery', {
      method: 'POST', headers: { Cookie: cookie, Origin: 'https://savefromnet.fun' },
    }), env);
    const code = (await recovery.json()).recoveryCode;
    assert.match(code, /^[a-f0-9]{32}\.[A-Za-z0-9_-]{43}$/);
    const redeemed = await redeemBatchPass(new Request('https://savefromnet.fun/api/batch-pass/redeem', {
      method: 'POST', headers: { Origin: 'https://savefromnet.fun', 'Content-Type': 'application/json' },
      body: JSON.stringify({ code }),
    }), env);
    assert.equal(redeemed.status, 200);
    assert.equal(await hasBatchPass(new Request(browser.url, { headers: { Cookie: redeemed.headers.get('Set-Cookie').split(';')[0] } }), env), true);
    const refunded = await batchWebhook(await signedWebhook(env, { type: 'refund.succeeded', data: { payment_id: 'pay_test123' } }), env);
    assert.equal(refunded.status, 200);
    assert.equal(await hasBatchPass(browser, env), false);
  } finally { globalThis.fetch = originalFetch; }
});

test('webhook rejects stale delivery', async () => {
  const env = testEnvironment();
  const request = await signedWebhook(env, { type: 'payment.succeeded', data: {} });
  request.headers.set('webhook-timestamp', String(Math.floor(Date.now() / 1000) - 1000));
  assert.equal(await verifyDodoWebhook(request, env.DODO_WEBHOOK_SECRET, await request.text()), false);
});
