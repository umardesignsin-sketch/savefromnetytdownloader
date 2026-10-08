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
  let objectUrl = null;
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
    if (!selected.length || selected.length > 5) return showError('Choose between 1 and 5 images.');
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
  updateOptions();
})();
