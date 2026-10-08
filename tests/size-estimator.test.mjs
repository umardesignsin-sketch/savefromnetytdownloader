import assert from 'node:assert/strict';
import test from 'node:test';

import { estimateBytes, estimateUrl, formatEstimate, parseEstimateQuery } from '../static/js/size-estimator.mjs';

test('estimate includes both video and audio streams', () => {
  assert.equal(estimateBytes(60, 8_000, 128), 60_960_000);
  assert.equal(estimateBytes(60, 8_000, 0), 60_000_000);
});

test('a 25-minute 19 Mbps combined stream cannot be a 23 MB file', () => {
  const estimate = formatEstimate(estimateBytes(25 * 60, 19_000));
  assert.equal(estimate.mb, '3,562.5');
  assert.equal(estimate.overLimit, true);
});

test('unknown or invalid required values are rejected', () => {
  assert.throws(() => estimateBytes(0, 8_000), RangeError);
  assert.throws(() => estimateBytes(60, 0), RangeError);
  assert.throws(() => estimateBytes(60, 8_000, -1), RangeError);
  assert.throws(() => estimateBytes(NaN, 8_000), RangeError);
});

test('shared calculator links restore valid inputs without accepting invalid ranges', () => {
  const values = { minutes: 25, seconds: 0, videoKbps: 19000, audioKbps: 128 };
  const url = estimateUrl('https://savefromnet.fun/guides/video-file-size-estimates', values);
  assert.deepEqual(parseEstimateQuery(new URL(url).search), values);
  assert.equal(parseEstimateQuery('?minutes=0&seconds=0&videoKbps=19000&audioKbps=128'), null);
  assert.equal(parseEstimateQuery('?minutes=25&seconds=0&videoKbps=-1&audioKbps=128'), null);
  assert.equal(parseEstimateQuery('?minutes=25&seconds=0&videoKbps=19000&audioKbps=Infinity'), null);
});
