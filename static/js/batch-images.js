(() => {
  const form = document.getElementById('batch-form');
  if (!form) return;
  const files = document.getElementById('batch-files');
  const list = document.getElementById('batch-file-list');
  const format = document.getElementById('batch-format');
  const quality = document.getElementById('batch-quality');
  const width = document.getElementById('batch-width');
  const button = document.getElementById('batch-submit');
  const status = document.getElementById('batch-status');
  const result = document.getElementById('batch-result');
  const detail = document.getElementById('batch-result-detail');
  const download = document.getElementById('batch-download');
  const cap = document.getElementById('batch-cap');
  const pro = document.getElementById('batch-pro');
  const proStatus = document.getElementById('batch-pro-status');
  const buy = document.getElementById('batch-buy');
  const showCode = document.getElementById('batch-show-code');
  const recoveryCode = document.getElementById('batch-recovery-code');
  const restore = document.getElementById('batch-restore');
  const restoreForm = document.getElementById('batch-restore-form');
  const restoreInput = document.getElementById('batch-restore-input');
  const restoreStatus = document.getElementById('batch-restore-status');
  let objectUrl = null;
  let pass = { available: false, active: false, pending: false, freeFiles: 5, paidFiles: 10 };
  let pendingPolls = 0;
  const checkoutState = new URLSearchParams(window.location.search).get('checkout');
  const mb = bytes => `${(bytes / 1048576).toFixed(2)} MB`;

  function clearResult() {
    result.hidden = true;
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = null;
  }
  function updateOptions() {
    const resizing = format.value === 'resize';
    document.getElementById('batch-width-wrap').hidden = !resizing;
    document.getElementById('batch-quality-wrap').hidden = resizing || format.value === 'png';
    width.required = resizing;
  }
  function showError(message) {
    status.textContent = message;
    status.classList.add('error');
  }
  async function refreshPass() {
    try {
      const response = await fetch('/api/batch-pass/status', { cache: 'no-store' });
      if (!response.ok) return;
      pass = await response.json();
      pro.hidden = !pass.available;
      cap.textContent = pass.active ? `Batch Pro · up to ${pass.paidFiles} images` : `Free · up to ${pass.freeFiles} images`;
      buy.hidden = pass.active;
      showCode.hidden = !pass.active;
      restore.hidden = pass.active;
      proStatus.textContent = pass.active ? `Batch Pro is active in this browser until ${new Date(pass.expiresAt).toLocaleDateString()}.` :
        checkoutState === 'cancelled' ? 'Checkout cancelled. Your free batches are still available.' :
        pass.pending && pendingPolls >= 20 ? 'Payment has not been confirmed yet. Check your receipt and refresh this page shortly.' :
        pass.pending ? 'Payment is still being confirmed. This page will check again shortly.' :
        'Your free five-image batches remain available.';
      if (pass.pending && checkoutState !== 'cancelled' && pendingPolls++ < 20) window.setTimeout(refreshPass, 3000);
      if (!pass.pending) pendingPolls = 0;
    } catch { /* Free batch processing remains available. */ }
  }
  buy.addEventListener('click', async () => {
    buy.disabled = true;
    proStatus.textContent = 'Opening secure checkout…';
    try {
      const response = await fetch('/api/batch-pass/checkout', { method: 'POST' });
      const data = await response.json();
      if (!response.ok || !data.checkoutUrl) throw new Error(data.error || 'Checkout is unavailable.');
      window.location.assign(data.checkoutUrl);
    } catch (error) {
      proStatus.textContent = error.message;
      buy.disabled = false;
    }
  });
  showCode.addEventListener('click', async () => {
    try {
      const response = await fetch('/api/batch-pass/recovery', { method: 'POST' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Recovery code is unavailable.');
      recoveryCode.textContent = data.recoveryCode;
      recoveryCode.hidden = false;
      showCode.hidden = true;
    } catch (error) { proStatus.textContent = error.message; }
  });
  restoreForm.addEventListener('submit', async event => {
    event.preventDefault();
    restoreStatus.textContent = 'Checking your code…';
    try {
      const response = await fetch('/api/batch-pass/redeem', { method: 'POST',
        headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ code: restoreInput.value.trim() }) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Could not restore this pass.');
      restoreInput.value = '';
      restoreStatus.textContent = 'Batch Pro restored.';
      refreshPass();
    } catch (error) { restoreStatus.textContent = error.message; }
  });
  files.addEventListener('change', () => {
    clearResult();
    status.textContent = '';
    list.replaceChildren();
    for (const file of files.files) {
      const item = document.createElement('li');
      const name = document.createElement('span');
      const size = document.createElement('small');
      name.textContent = file.name;
      size.textContent = mb(file.size);
      item.append(name, size);
      list.append(item);
    }
  });
  format.addEventListener('change', () => { clearResult(); updateOptions(); });
  quality.addEventListener('input', () => { document.getElementById('batch-quality-value').textContent = quality.value; });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    clearResult();
    status.classList.remove('error');
    const selected = [...files.files];
    const maxFiles = pass.active ? pass.paidFiles : pass.freeFiles;
    if (!selected.length || selected.length > maxFiles) return showError(`Choose between 1 and ${maxFiles} images.`);
    if (selected.some(file => file.size > 8 * 1048576)) return showError('Each image must be 8 MB or smaller.');
    if (selected.reduce((sum, file) => sum + file.size, 0) > 20 * 1048576) return showError('The batch must be 20 MB or smaller.');
    if (format.value === 'resize' && (!Number.isInteger(Number(width.value)) || Number(width.value) < 1 || Number(width.value) > 8192)) return showError('Enter a width between 1 and 8192 pixels.');
    button.disabled = true;
    status.textContent = `Processing ${selected.length} image${selected.length === 1 ? '' : 's'}…`;
    try {
      const response = await fetch('/api/image/batch', { method: 'POST', body: new FormData(form) });
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || 'The batch could not be processed. Try again.');
      }
      const blob = await response.blob();
      objectUrl = URL.createObjectURL(blob);
      download.href = objectUrl;
      const count = Number(response.headers.get('X-SFN-Files')) || selected.length;
      const inputBytes = Number(response.headers.get('X-SFN-Input-Bytes')) || selected.reduce((sum, file) => sum + file.size, 0);
      const outputBytes = Number(response.headers.get('X-SFN-Output-Bytes')) || blob.size;
      detail.textContent = `${count} image${count === 1 ? '' : 's'} · ${mb(inputBytes)} in → ${mb(outputBytes)} processed · ${mb(blob.size)} ZIP`;
      result.hidden = false;
      status.textContent = 'Download ready.';
      result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
      showError(error.message);
    } finally {
      button.disabled = false;
    }
  });
  window.addEventListener('pagehide', clearResult);
  if (checkoutState) {
    window.history.replaceState(null, '', window.location.pathname);
  }
  refreshPass();
  updateOptions();
})();
