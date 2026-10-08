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
