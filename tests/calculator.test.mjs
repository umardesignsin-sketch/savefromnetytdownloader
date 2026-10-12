import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateExpression, formatResult } from '../static/js/calculator-core.mjs';

test('arithmetic precedence and parentheses', () => {
  assert.equal(evaluateExpression('2 + 3 × 4'), 14);
  assert.equal(evaluateExpression('(2 + 3) × 4'), 20);
  assert.equal(evaluateExpression('100 ÷ (5 × 2)'), 10);
  assert.equal(evaluateExpression('-2 + 5'), 3);
});

test('percent, root, decimals and formatting', () => {
  assert.equal(evaluateExpression('80 × 25%'), 20);
  assert.equal(evaluateExpression('√(81) + .5'), 9.5);
  assert.equal(formatResult(evaluateExpression('1000 + 20')), '1,020');
});

test('rejects input that is not arithmetic', () => {
  for (const input of ['', '2+', '(2+3', '1/0', 'sqrt(-1)', '1e999', 'alert(1)', '2**3', '2;3', '1+NaN']) {
    assert.throws(() => evaluateExpression(input), Error, input);
  }
});
