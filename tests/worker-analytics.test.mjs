import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const source = readFileSync(new URL('../src/worker.js', import.meta.url), 'utf8')
  .replace(/^import .*;\r?\n/gm, '')
  .replace(/^export \{ VisitorAnalytics \};\r?\n/gm, '')
  .replace('export class DownloaderContainer', 'class DownloaderContainer')
  .replace('export default {', 'const worker = {');
const worker = new Function('Container', 'guardAnalysis', 'dashboardHtml', 'world',
  `${source}\nreturn worker;`)(class {}, value => value, '<h1>Analytics</h1>', []);

test('dashboard and country data require the admin password', async () => {
  const env = { DASHBOARD_PASSWORD: 'test-secret', VISITOR_ANALYTICS: {
    getByName: () => ({ fetch: async () => Response.json({ liveVisitors: 2 }) }),
  } };
  const rejected = await worker.fetch(new Request('https://savefromnet.fun/analytics'), env);
  assert.equal(rejected.status, 401);
  assert.match(rejected.headers.get('WWW-Authenticate'), /Basic/);
  const headers = { Authorization: `Basic ${btoa('admin:test-secret')}` };
  const page = await worker.fetch(new Request('https://savefromnet.fun/analytics', { headers }), env);
  assert.equal(page.status, 200);
  assert.match(await page.text(), /Analytics/);
  assert.equal(page.headers.get('X-Robots-Tag'), 'noindex, nofollow');
  const data = await worker.fetch(new Request('https://savefromnet.fun/api/analytics', { headers }), env);
  assert.equal((await data.json()).liveVisitors, 2);
  assert.equal(data.headers.get('Cache-Control'), 'private, no-store');
});

test('visit signal hashes the visitor and uses Cloudflare country, not client input', async () => {
  let forwarded;
  const env = {
    VISITOR_HASH_KEY: 'test-hmac-key',
    EVENT_LIMIT: { limit: async () => ({ success: true }) },
    VISITOR_ANALYTICS: { getByName: () => ({ fetch: async (_url, init) => {
      forwarded = JSON.parse(init.body);
      return new Response(null, { status: 204 });
    } }) },
  };
  const request = new Request('https://savefromnet.fun/api/visit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '203.0.113.4', 'User-Agent': 'Test Browser', Origin: 'https://savefromnet.fun' },
    body: JSON.stringify({ kind: 'page', country: 'ZZ', visitor: 'forged' }),
  });
  Object.defineProperty(request, 'cf', { value: { country: 'IN' } });
  assert.equal((await worker.fetch(request, env)).status, 204);
  assert.equal(forwarded.country, 'IN');
  assert.equal(forwarded.kind, 'page');
  assert.match(forwarded.visitor, /^[a-f0-9]{64}$/);
  assert.equal(JSON.stringify(forwarded).includes('203.0.113.4'), false);
  const crossSite = new Request('https://savefromnet.fun/api/visit', {
    method: 'POST', headers: { Origin: 'https://evil.example' }, body: '{"kind":"page"}',
  });
  assert.equal((await worker.fetch(crossSite, env)).status, 403);
});
