import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import * as batch from '../src/batch-pass.mjs';
import * as transcript from '../src/transcript-api.mjs';

// Exercise the production request handler with Cloudflare-only imports stubbed.
const source = readFileSync(new URL('../src/worker.js', import.meta.url), 'utf8')
  .replace(/^import .*;\r?\n/gm, '')
  .replace(/^export \{ VisitorAnalytics \};\r?\n/gm, '')
  .replace('export class BatchPassStore', 'class BatchPassStore')
  .replace('export class TranscriptAccountStore', 'class TranscriptAccountStore')
  .replace('export class DownloaderContainer', 'class DownloaderContainer')
  .replace('export default {', 'const worker = {');
const worker = new Function('Container', 'DurableObject', 'batch', 'transcript', 'guardAnalysis', 'developerDashboardHtml',
  `const { BatchPassStore: BatchPassHandler, activeBatchOrder, batchRecoveryCode, batchWebhook, passStatus, redeemBatchPass, signedBatchTier, startBatchCheckout } = batch;
const { TranscriptAccountStore: TranscriptAccountHandler, developerCheckout, developerKey, developerPortal, developerRecovery, developerRedeem, developerStatus, developerWebhook, paidTranscript } = transcript;
${source}
return worker;`)(class {}, class {}, batch, transcript, value => value, '<h1>Developers</h1>');

test('new utility APIs are rate limited and forwarded to the container', async () => {
  const forwarded = [];
  const keys = [];
  const env = {
    ANALYZE_LIMIT: { limit: async ({ key }) => { keys.push(key); return { success: true }; } },
    DOWNLOADER: { getByName: () => ({ fetch: async request => {
      forwarded.push(new URL(request.url).pathname);
      return Response.json({ ok: true });
    } }) },
  };
  for (const path of ['/api/translate', '/api/weather/us']) {
    const response = await worker.fetch(new Request(`https://savefromnet.fun${path}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '203.0.113.7' },
      body: '{}',
    }), env);
    assert.equal(response.status, 200);
  }
  assert.deepEqual(forwarded, ['/api/translate', '/api/weather/us']);
  assert.deepEqual(keys, ['/api/translate:203.0.113.7', '/api/weather/us:203.0.113.7']);
});

test('new utility APIs reject cross-origin and oversized requests before forwarding', async () => {
  let forwarded = 0;
  const env = {
    ANALYZE_LIMIT: { limit: async () => ({ success: true }) },
    DOWNLOADER: { getByName: () => ({ fetch: async () => { forwarded++; return Response.json({ ok: true }); } }) },
  };
  const path = 'https://savefromnet.fun/api/translate';
  const crossOrigin = await worker.fetch(new Request(path, {
    method: 'POST', headers: { Origin: 'https://other.example' }, body: '{}',
  }), env);
  assert.equal(crossOrigin.status, 403);
  const oversized = await worker.fetch(new Request(path, {
    method: 'POST', headers: { 'Content-Length': '4097' }, body: '{}',
  }), env);
  assert.equal(oversized.status, 413);
  env.ANALYZE_LIMIT.limit = async () => ({ success: false });
  const limited = await worker.fetch(new Request(path, { method: 'POST', body: '{}' }), env);
  assert.equal(limited.status, 429);
  assert.equal(forwarded, 0);
});
