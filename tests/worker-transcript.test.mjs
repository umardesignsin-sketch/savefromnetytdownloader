import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import * as batch from '../src/batch-pass.mjs';

// Run the real fetch handler with the Cloudflare-only imports replaced by stubs.
const source = readFileSync(new URL('../src/worker.js', import.meta.url), 'utf8')
  .replace(/^import .*;\r?\n/gm, '')
  .replace(/^export \{ VisitorAnalytics \};\r?\n/gm, '')
  .replace('export class BatchPassStore', 'class BatchPassStore')
  .replace('export class DownloaderContainer', 'class DownloaderContainer')
  .replace('export default {', 'const worker = {');
const worker = new Function('Container', 'DurableObject', 'batch', 'guardAnalysis',
  `const { BatchPassStore: BatchPassHandler, activeBatchOrder, batchRecoveryCode, batchWebhook, passStatus, redeemBatchPass, signedBatchTier, startBatchCheckout } = batch;\n${source}\nreturn worker;`)(class {}, class {}, batch, value => value);

test('transcript requests reach the container and record their completed result', async () => {
  const events = [];
  const payload = { language: 'en', segments: [{ start_ms: 0, end_ms: 1000, text: 'Caption' }] };
  const env = {
    ANALYZE_LIMIT: { limit: async () => ({ success: true }) },
    DOWNLOADER: { getByName: () => ({ fetch: async () => new Response(JSON.stringify(payload), {
      status: 200, headers: { 'Content-Type': 'application/json' },
    }) }) },
    EVENTS: { writeDataPoint: event => events.push(event) },
  };
  const response = await worker.fetch(new Request('https://savefromnet.fun/api/transcript', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: 'https://youtu.be/PRU2ShMzQRg' }),
  }), env);
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), payload);
  assert.ok(events.some(event => event.blobs[0] === 'transcript_successful'));
});

test('versioned transcript API forwards to the existing extractor and keeps JSON errors', async () => {
  const events = [];
  const forwarded = [];
  const payload = { platform: 'youtube', language: 'en', segments: [{ start_ms: 0, end_ms: 1000, text: 'Caption' }] };
  const env = {
    ANALYZE_LIMIT: { limit: async () => ({ success: true }) },
    DOWNLOADER: { getByName: () => ({ fetch: async request => {
      forwarded.push({ pathname: new URL(request.url).pathname, body: await request.json() });
      return Response.json(payload, { headers: { 'Cache-Control': 'no-store' } });
    } }) },
    EVENTS: { writeDataPoint: event => events.push(event) },
  };
  const response = await worker.fetch(new Request('https://savefromnet.fun/api/v1/youtube/transcript', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: 'https://youtu.be/PRU2ShMzQRg', language: 'en' }),
  }), env);
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), payload);
  assert.deepEqual(forwarded, [{ pathname: '/api/transcript', body: { url: 'https://youtu.be/PRU2ShMzQRg', language: 'en' } }]);
  assert.ok(events.some(event => event.blobs[0] === 'transcript_successful'));
});

test('versioned transcript API rejects wrong methods and malformed or oversized requests before processing', async () => {
  let forwarded = 0;
  const env = { DOWNLOADER: { getByName: () => ({ fetch: async () => { forwarded++; return Response.json({}); } }) } };
  const endpoint = 'https://savefromnet.fun/api/v1/youtube/transcript';
  const cases = [
    [new Request(endpoint), 405, 'method_not_allowed'],
    [new Request(endpoint, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: '{}' }), 415, 'unsupported_media_type'],
    [new Request(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': '5010' }, body: JSON.stringify({ url: 'x'.repeat(5000) }) }), 413, 'request_too_large'],
    [new Request(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url: 'x'.repeat(5000) }) }), 400, 'invalid_request'],
    [new Request(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' }), 400, 'invalid_request'],
    [new Request(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url: 'https://youtu.be/PRU2ShMzQRg', language: '../bad' }) }), 400, 'invalid_request'],
  ];
  for (const [request, status, code] of cases) {
    const response = await worker.fetch(request, env);
    assert.equal(response.status, status);
    assert.equal((await response.json()).code, code);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
  }
  assert.equal(forwarded, 0);
});
