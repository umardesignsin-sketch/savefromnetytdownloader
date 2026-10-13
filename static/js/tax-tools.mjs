import { calculateTax, parseAmount } from './tax-core.mjs';

const form = document.getElementById('tax-form');

if (form) {
  const config = JSON.parse(form.dataset.config);
  const $ = id => document.getElementById(id);
  const money = config.currency
    ? new Intl.NumberFormat(config.locale, { style: 'currency', currency: config.currency })
    : new Intl.NumberFormat(config.locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const rateSelect = $('tax-rate');
  const unit = config.currency === 'GBP' ? 'penny' : 'cent';
  const clearResults = () => ['tax-net', 'tax-amount-out', 'tax-gross'].forEach(id => { $(id).textContent = '—'; });
  const customRow = $('tax-custom-row');

  function selectedRate() {
    if (rateSelect.value === 'custom') return parseAmount($('tax-custom-rate').value);
    let rate = Number(rateSelect.value);
    if (config.local_rate) {
      const local = $('tax-local-rate').value.trim();
      const localRate = local ? parseAmount(local) : 0;
      if (!Number.isFinite(localRate)) return NaN;
      rate += localRate;
    }
    return rate;
  }

  function update() {
    customRow.hidden = rateSelect.value !== 'custom';
    const direction = form.querySelector('input[name="tax-direction"]:checked').value;
    const amountText = $('tax-amount').value;
    const rate = selectedRate();
    const status = $('tax-status');
    status.classList.remove('error');
    if (!amountText.trim()) {
      status.textContent = 'Enter an amount to calculate.';
      clearResults();
      return;
    }
    const result = calculateTax(parseAmount(amountText), rate, direction);
    if (!result) {
      status.textContent = 'Enter a positive amount and a rate between 0 and 100%.';
      status.classList.add('error');
      clearResults();
      return;
    }
    status.textContent = `Rate used: ${Number(rate.toFixed(4))}% ${config.tax}. Results are rounded to the nearest ${unit}.`;
    $('tax-net').textContent = money.format(result.net);
    $('tax-amount-out').textContent = money.format(result.tax);
    $('tax-gross').textContent = money.format(result.gross);
  }

  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('submit', event => { event.preventDefault(); update(); });
  update();
}
