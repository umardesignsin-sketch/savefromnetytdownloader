import assert from 'node:assert/strict';
import test from 'node:test';

import { estimateBytes, formatEstimate } from '../static/js/size-estimator.mjs';

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
