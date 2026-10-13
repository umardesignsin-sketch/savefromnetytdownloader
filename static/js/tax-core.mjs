// Pure arithmetic for the VAT, GST and sales tax calculators.

export function roundCents(value) {
  return Math.sign(value) * Math.round(Math.abs(value) * 100 + 1e-7) / 100;
}

// Accepts "1,234.50", "1234.5", "£99", and European "1.234,50" or "12,50".
export function parseAmount(text) {
  let value = String(text ?? '').trim().replace(/[\s£$€]|AUD|USD|GBP|EUR/gi, '');
  if (!value) return NaN;
  if (/^\d{1,3}(\.\d{3})+(,\d+)?$/.test(value) || /^\d+,\d{1,2}$/.test(value)) {
    value = value.replace(/\./g, '').replace(',', '.');
  } else {
    value = value.replace(/,/g, '');
  }
  return /^(\d+\.?\d*|\.\d+)$/.test(value) ? Number(value) : NaN;
}

// direction "add": amount excludes tax. direction "remove": amount already includes tax.
export function calculateTax(amount, ratePercent, direction) {
  if (!Number.isFinite(amount) || amount < 0 || !Number.isFinite(ratePercent) || ratePercent < 0 || ratePercent > 100) return null;
  if (direction === 'remove') {
    const gross = roundCents(amount);
    const net = roundCents(gross / (1 + ratePercent / 100));
    return { net, tax: roundCents(gross - net), gross };
  }
  const net = roundCents(amount);
  const tax = roundCents(net * ratePercent / 100);
  return { net, tax, gross: roundCents(net + tax) };
}
