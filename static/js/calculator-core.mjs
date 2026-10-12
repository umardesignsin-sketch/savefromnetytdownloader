// A small arithmetic parser. Never evaluate visitor input as JavaScript.
export function evaluateExpression(expression) {
  if (typeof expression !== 'string' || !expression.trim() || expression.length > 120) {
    throw new Error('Enter an expression of up to 120 characters.');
  }
  const source = expression.replaceAll('×', '*').replaceAll('÷', '/').replaceAll('−', '-').replaceAll('√', 'sqrt');
  const tokens = [];
  for (let i = 0; i < source.length;) {
    if (/\s/.test(source[i])) { i++; continue; }
    const number = source.slice(i).match(/^(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?/);
    if (number) { tokens.push({ type: 'number', value: Number(number[0]) }); i += number[0].length; continue; }
    if (source.slice(i, i + 4) === 'sqrt') { tokens.push({ type: 'sqrt' }); i += 4; continue; }
    if ('+-*/()%'.includes(source[i])) { tokens.push({ type: source[i] }); i++; continue; }
    throw new Error('Use numbers and the supported arithmetic operators only.');
  }
  let index = 0;
  const peek = () => tokens[index]?.type;
  const consume = type => { if (peek() !== type) throw new Error('Check the expression and parentheses.'); index++; };
  function primary() {
    if (peek() === '+') { index++; return primary(); }
    if (peek() === '-') { index++; return -primary(); }
    if (peek() === 'sqrt') { index++; consume('('); const value = sum(); consume(')'); if (value < 0) throw new Error('Cannot take the square root of a negative number.'); return Math.sqrt(value); }
    if (peek() === '(') { index++; const value = sum(); consume(')'); return value; }
    if (peek() === 'number') return tokens[index++].value;
    throw new Error('Check the expression and parentheses.');
  }
  function percent() { let value = primary(); while (peek() === '%') { index++; value /= 100; } return value; }
  function product() {
    let value = percent();
    while (peek() === '*' || peek() === '/') {
      const op = tokens[index++].type;
      const right = percent();
      if (op === '/' && right === 0) throw new Error('Division by zero is undefined.');
      value = op === '*' ? value * right : value / right;
    }
    return value;
  }
  function sum() {
    let value = product();
    while (peek() === '+' || peek() === '-') {
      const op = tokens[index++].type;
      const right = product();
      value = op === '+' ? value + right : value - right;
    }
    return value;
  }
  const result = sum();
  if (index !== tokens.length) throw new Error('Check the expression and parentheses.');
  if (!Number.isFinite(result)) throw new Error('The result is too large to display.');
  return Object.is(result, -0) ? 0 : result;
}

export function formatResult(value) {
  return Number(value.toPrecision(12)).toLocaleString('en-US', { maximumSignificantDigits: 12 });
}
