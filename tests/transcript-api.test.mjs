import test from 'node:test';
import assert from 'node:assert/strict';
import { Buffer } from 'node:buffer';
import { TranscriptAccountStore, developerCheckout, developerKey, developerPortal, developerStatus, developerWebhook, paidTranscript } from '../src/transcript-api.mjs';
import { developerDashboardHtml } from '../src/developer-dashboard.mjs';

test('developer request example has copyable curl lines', () => {
  assert.match(developerDashboardHtml, /curl -X POST https:\/\/savefromnet\.fun\/api\/v2\/youtube\/transcript/);
  assert.doesNotMatch(developerDashboardHtml, /\n\+\s+-H/);
});

function fixture() {
  const instances = new Map();
  const env = {
    DODO_MODE: 'test', DODO_API_KEY: 'test', DODO_TRANSCRIPT_PRODUCT_ID: 'pdt_transcript',
    DODO_TRANSCRIPT_WEBHOOK_SECRET: `whsec_${Buffer.from('b'.repeat(32)).toString('base64')}`,
    EVENT_LIMIT: { limit: async () => ({ success: true }) },
    ANALYZE_LIMIT: { limit: async () => ({ success: true }) },
    TRANSCRIPT_ACCOUNTS: { getByName(id) {
      if (!instances.has(id)) {
        const values = new Map();
        instances.set(id, { values, handler: new TranscriptAccountStore({ storage: {
          get: async key => values.get(key), put: async (key, value) => values.set(key, value),
          setAlarm: async () => {}, deleteAll: async () => values.clear(),
        } }) });
      }
      return { fetch: (url, init) => instances.get(id).handler.fetch(new Request(url, init)) };
    } },
  };
  return { env, instances };
}
async function signed(env, body, valid = true) {
  const payload = JSON.stringify(body);
  const id = 'msg_transcript_test';
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const key = await crypto.subtle.importKey('raw', Buffer.from(env.DODO_TRANSCRIPT_WEBHOOK_SECRET.slice(6), 'base64'),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const signature = Buffer.from(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(`${id}.${timestamp}.${payload}`))).toString('base64');
  return new Request('https://savefromnet.fun/api/developer/webhook', { method: 'POST', body: payload,
    headers: { 'webhook-id': id, 'webhook-timestamp': timestamp, 'webhook-signature': `v1,${valid ? signature : 'invalid'}` } });
}

test('paid API activates only after signed payment, meters successes, and rotates keys', async () => {
  const { env, instances } = fixture();
  const originalFetch = globalThis.fetch;
  let id;
  const started = new Date(Date.now() - 60000).toISOString();
  const ends = new Date(Date.now() + 25 * 86400000).toISOString();
  let product = 'pdt_transcript';
  globalThis.fetch = async (url, init) => {
    if (String(url).endsWith('/checkouts')) {
      const checkout = JSON.parse(init.body);
      id = checkout.metadata.transcript_account_id;
      assert.equal(checkout.product_cart[0].product_id, 'pdt_transcript');
      return Response.json({ session_id: 'cks_test123', checkout_url: 'https://test.checkout.dodopayments.com/session/cks_test123' });
    }
    if (String(url).includes('/payments/')) return Response.json({ payment_id: 'pay_test123', status: 'succeeded', subscription_id: 'sub_test123',
      checkout_session_id: 'cks_test123', product_cart: null, total_amount: 500, is_update_payment_method: false });
    if (String(url).includes('/subscriptions/')) return Response.json({ subscription_id: 'sub_test123', status: 'active',
      product_id: product, quantity: 1, customer: { customer_id: 'cus_test123' }, metadata: { transcript_account_id: id }, previous_billing_date: started, next_billing_date: ends });
    if (String(url).includes('/customer-portal/session')) return Response.json({ link: 'https://test.dodopayments.com/portal/test123' });
    throw Error(`Unexpected URL ${url}`);
  };
  try {
    const checkout = await developerCheckout(new Request('https://savefromnet.fun/api/developer/checkout', { method: 'POST',
      headers: { Origin: 'https://savefromnet.fun' } }), env);
    assert.equal(checkout.status, 200);
    const cookie = checkout.headers.get('Set-Cookie').split(';')[0];
    const browser = new Request('https://savefromnet.fun/api/developer/status', { headers: { Cookie: cookie } });
    assert.equal((await (await developerStatus(browser, env)).json()).active, false);
    const event = { type: 'payment.succeeded', data: { payment_id: 'pay_test123' } };
    assert.equal((await developerWebhook(await signed(env, event, false), env)).status, 400);
    assert.equal((await (await developerStatus(browser, env)).json()).active, false);
    product = 'wrong_product';
    assert.equal((await developerWebhook(await signed(env, event), env)).status, 200);
    assert.equal((await (await developerStatus(browser, env)).json()).active, false);
    product = 'pdt_transcript';
    assert.equal((await developerWebhook(await signed(env, event), env)).status, 200);
    assert.equal((await (await developerStatus(browser, env)).json()).active, true);
    const portal = await developerPortal(new Request('https://savefromnet.fun/api/developer/portal', { method: 'POST',
      headers: { Cookie: cookie, Origin: 'https://savefromnet.fun' },
    }), env);
    assert.equal(portal.status, 200);
    assert.match((await portal.json()).portalUrl, /dodopayments\.com/);
    const keyResponse = await developerKey(new Request('https://savefromnet.fun/api/developer/key', { method: 'POST', headers: {
      Cookie: cookie, Origin: 'https://savefromnet.fun',
    } }), env);
    assert.equal(keyResponse.status, 200);
    const key = (await keyResponse.json()).apiKey;
    assert.match(key, /^sfn_[a-f0-9]{32}_[A-Za-z0-9_-]{43}$/);
    let upstreamStatus = 200;
    env.DOWNLOADER = { getByName: () => ({ fetch: async request => {
      assert.equal(new URL(request.url).pathname, '/api/transcript');
      return Response.json(upstreamStatus === 200 ? { segments: [{ start_ms: 0, end_ms: 1000, text: 'hi' }] } : { error: 'No captions' }, { status: upstreamStatus });
    } }) };
    const call = token => paidTranscript(new Request('https://savefromnet.fun/api/v2/youtube/transcript', { method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: 'https://youtu.be/PRU2ShMzQRg' }),
    }), env);
    assert.equal((await call(key)).status, 200);
    upstreamStatus = 422;
    assert.equal((await call(key)).status, 422);
    assert.equal((await (await developerStatus(browser, env)).json()).used, 1);
    const rotated = (await (await developerKey(new Request('https://savefromnet.fun/api/developer/key', {
      method: 'POST', headers: { Cookie: cookie, Origin: 'https://savefromnet.fun' },
    }), env)).json()).apiKey;
    assert.equal((await call(key)).status, 401);
    upstreamStatus = 200;
    assert.equal((await call(rotated)).status, 200);
    assert.equal((await (await developerStatus(browser, env)).json()).used, 2);
    const state = instances.get(id).values.get('account');
    assert.equal(state.keyHash.length, 64);
    assert.equal(JSON.stringify(state).includes(rotated), false);
    assert.equal(JSON.stringify(state).includes('PRU2ShMzQRg'), false);
  } finally { globalThis.fetch = originalFetch; }
});

test('quota and concurrency reservations prevent overuse; failed work releases reservations', async () => {
  const { env, instances } = fixture();
  const id = 'a'.repeat(32);
  const token = 'b'.repeat(43);
  const hash = async value => Buffer.from(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value))).toString('hex');
  const state = { ownerHash: await hash('owner'), keyHash: await hash(`sfn_${id}_${token}`), status: 'active',
    sessionIds: ['cks_test123'], subscriptionId: 'sub_test123', periodStart: Date.now() - 1000,
    periodEnd: Date.now() + 86400000, used: 999, pending: {}, minute: 0, calls: 0 };
  const store = env.TRANSCRIPT_ACCOUNTS.getByName(id);
  instances.get(id).values.set('account', state);
  const send = (path, value) => store.fetch(`https://developer.internal${path}`, { method: 'POST', body: JSON.stringify(value) });
  assert.equal((await send('/reserve', { keyHash: state.keyHash, reservation: 'one' })).status, 200);
  assert.equal((await send('/reserve', { keyHash: state.keyHash, reservation: 'two' })).status, 429);
  assert.equal((await send('/settle', { reservation: 'one', success: false })).status, 200);
  assert.equal((await send('/reserve', { keyHash: state.keyHash, reservation: 'two' })).status, 200);
  assert.equal((await send('/settle', { reservation: 'two', success: true })).status, 200);
  assert.equal((await send('/reserve', { keyHash: state.keyHash, reservation: 'three' })).status, 429);
  const nextStart = Date.now() + 1000;
  assert.equal((await send('/sync', { subscriptionId: 'sub_test123', status: 'active', paymentConfirmed: true,
    periodStart: nextStart, periodEnd: Date.now() + 30 * 86400000 })).status, 200);
  assert.equal(instances.get(id).values.get('account').used, 0);
  assert.equal((await send('/reserve', { keyHash: state.keyHash, reservation: 'four' })).status, 200);
  assert.equal((await send('/sync', { subscriptionId: 'sub_test123', status: 'on_hold' })).status, 200);
  assert.equal((await send('/reserve', { keyHash: state.keyHash, reservation: 'five' })).status, 403);
});
