import assert from 'node:assert/strict';
import test from 'node:test';
import { calculateTax, parseAmount, roundCents } from '../static/js/tax-core.mjs';
import { backgroundIssues, computeCrop, estimateCrown, fileIssues, poseIssues, setJpegDpi, sheetLayout } from '../static/js/passport-core.mjs';

const US = { photo_mm: [50.8, 50.8], photo_px: [600, 600], head_mm: [25.4, 34.9], target_head_mm: 31, top_ratio: 0.32, sheet: { px: [1800, 1200], gap_px: 0 } };
const UK = { photo_mm: [35, 45], photo_px: [413, 531], head_mm: [29, 34], target_head_mm: 31.5, top_ratio: 0.35, sheet: { px: [1800, 1200], gap_px: 24 } };

test('tax: worked examples from the pages', () => {
  assert.deepEqual(calculateTax(100, 20, 'add'), { net: 100, tax: 20, gross: 120 });
  assert.deepEqual(calculateTax(120, 20, 'remove'), { net: 100, tax: 20, gross: 120 });
  assert.deepEqual(calculateTax(110, 10, 'remove'), { net: 100, tax: 10, gross: 110 });
  assert.deepEqual(calculateTax(100, 19, 'add'), { net: 100, tax: 19, gross: 119 });
  assert.deepEqual(calculateTax(100, 8.25, 'add'), { net: 100, tax: 8.25, gross: 108.25 });
});

test('tax: rounds to the cent and rejects bad input', () => {
  assert.deepEqual(calculateTax(9.99, 6.875, 'add'), { net: 9.99, tax: 0.69, gross: 10.68 });
  assert.equal(roundCents(1.005), 1.01);
  assert.equal(calculateTax(-1, 20, 'add'), null);
  assert.equal(calculateTax(10, 120, 'add'), null);
  assert.equal(calculateTax(NaN, 20, 'add'), null);
});

test('tax: parses UK, US and European number formats', () => {
  assert.equal(parseAmount('£1,234.50'), 1234.5);
  assert.equal(parseAmount('1.234,50'), 1234.5);
  assert.equal(parseAmount('12,50'), 12.5);
  assert.equal(parseAmount(' $99 '), 99);
  assert.ok(Number.isNaN(parseAmount('12a')));
  assert.ok(Number.isNaN(parseAmount('')));
});

test('passport: crown uses hair for US rules and the skull estimate for UK rules', () => {
  const face = { chinY: 800, foreheadY: 480, hairTop: 330 };
  assert.equal(estimateCrown(face, 'hair'), 330);
  assert.equal(estimateCrown(face, 'skull'), 800 - 320 * 1.25);
  assert.equal(estimateCrown({ ...face, hairTop: 450 }, 'skull'), 450); // bald or short hair sits below the estimate
});

test('passport: crop scales the head to the target and reports what is missing', () => {
  const crop = computeCrop(UK, { chinY: 900, crownY: 500, centerX: 1000 }, 2000, 3000);
  assert.equal(crop.fits, true);
  assert.ok(Math.abs(crop.sh / crop.sw - 45 / 35) < 1e-9);
  assert.ok(Math.abs((900 - 500) / crop.pxPerMm - 31.5) < 1e-9);
  assert.ok(Math.abs((500 - crop.sy) / crop.pxPerMm - (45 - 31.5) * 0.35) < 1e-9);
  const tight = computeCrop(UK, { chinY: 900, crownY: 100, centerX: 300 }, 600, 1000);
  assert.equal(tight.fits, false);
  assert.ok(tight.missing.top > 0 && tight.missing.left > 0);
});

test('passport: print sheets hold six US or eight 35 x 45 mm photos', () => {
  const us = sheetLayout(US);
  assert.equal(us.positions.length, 6);
  assert.deepEqual(us.positions.at(-1), [1200, 600]);
  const uk = sheetLayout(UK);
  assert.equal(uk.positions.length, 8);
  for (const [x, y] of uk.positions) assert.ok(x >= 0 && y >= 0 && x + 413 <= 1800 && y + 531 <= 1200);
});

test('passport: marks a canvas JPEG as 300 dpi', () => {
  const bytes = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 0, 16, 0x4a, 0x46, 0x49, 0x46, 0, 1, 1, 0, 0, 1, 0, 1]);
  setJpegDpi(bytes, 300);
  assert.deepEqual([...bytes.slice(13, 18)], [1, 1, 44, 1, 44]);
  const notJfif = new Uint8Array([0x89, 0x50, 0x4e, 0x47]);
  assert.deepEqual(setJpegDpi(notJfif, 300), notJfif);
});

test('passport: file, background and pose checks explain each problem', () => {
  const online = { min_kb: 50, max_kb: 10240, min_px: [600, 750], formats: null };
  assert.deepEqual(fileIssues(online, { size: 2_000_000, width: 3000, height: 4000 }), []);
  assert.equal(fileIssues(online, { size: 20_000, width: 500, height: 700 }).length, 2);
  assert.match(fileIssues({ ...online, formats: ['JPEG', 'PNG'] }, { size: 99_999, width: 900, height: 900, format: 'WEBP' })[0], /not listed/);
  assert.deepEqual(backgroundIssues({ fraction: 0.4, meanL: 235, stdL: 8, meanChroma: 6 }, 'white'), []);
  assert.equal(backgroundIssues({ fraction: 0.4, meanL: 120, stdL: 45, meanChroma: 6 }, 'light').length, 2);
  assert.match(backgroundIssues({ fraction: 0.4, meanL: 190, stdL: 8, meanChroma: 40 }, 'white')[0], /white or off-white/);
  const level = { leftEye: { x: 100, y: 200 }, rightEye: { x: 200, y: 200 }, nose: { x: 150, y: 260 } };
  assert.deepEqual(poseIssues(level), []);
  assert.equal(poseIssues({ ...level, rightEye: { x: 200, y: 230 }, blinkLeft: 0.9, jawOpen: 0.6 }).length, 3);
});
