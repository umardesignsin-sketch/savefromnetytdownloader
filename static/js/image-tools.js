(() => {
  const form = document.getElementById('image-form');
  if (!form) return;
  const file = document.getElementById('image-file');
  const label = document.getElementById('image-file-label');
  const button = document.getElementById('image-submit');
  const status = document.getElementById('image-status');
  const result = document.getElementById('image-result');
  const detail = document.getElementById('image-result-detail');
  const link = document.getElementById('image-download');
  const quality = document.getElementById('image-quality');
  let previousUrl = null;
  const size = value => value >= 1048576 ? `${(value / 1048576).toFixed(2)} MB` : `${Math.max(1, Math.round(value / 1024))} KB`;
  function clearResult() {
    result.hidden = true;
    if (previousUrl) URL.revokeObjectURL(previousUrl);
    previousUrl = null;
  }
  file.addEventListener('change', () => {
    clearResult();
    status.textContent = '';
    if (file.files[0]) label.textContent = `${file.files[0].name} · ${size(file.files[0].size)}`;
  });
  if (quality) quality.addEventListener('input', () => { document.getElementById('quality-value').textContent = quality.value; });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    clearResult();
    status.classList.remove('error');
    const selected = file.files[0];
    if (!selected) { status.textContent = 'Choose an image first.'; status.classList.add('error'); return; }
    if (selected.size > 8 * 1024 * 1024) { status.textContent = 'Choose an image under 8 MB.'; status.classList.add('error'); return; }
    const payload = new FormData(form);
    payload.set('tool', form.dataset.tool);
    button.disabled = true;
    status.textContent = 'Processing image…';
    try {
      const response = await fetch('/api/image/process', { method: 'POST', body: payload });
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || 'The image could not be processed. Try another file.');
      }
      const blob = await response.blob();
      previousUrl = URL.createObjectURL(blob);
      const disposition = response.headers.get('content-disposition') || '';
      const filename = disposition.match(/filename="?([^";]+)"?/i)?.[1] || `converted-image.${blob.type.split('/')[1] || 'bin'}`;
      link.href = previousUrl;
      link.download = filename;
      const dimensions = response.headers.get('X-SFN-Dimensions');
      const original = Number(response.headers.get('X-SFN-Input-Bytes')) || selected.size;
      detail.textContent = `${size(original)} original → ${size(blob.size)} result${dimensions ? ` · ${dimensions.replace('x', ' × ')} pixels` : ''}`;
      result.hidden = false;
      status.textContent = 'Image ready. Save the result below.';
      result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
      status.textContent = error.message;
      status.classList.add('error');
    } finally {
      button.disabled = false;
    }
  });
  window.addEventListener('pagehide', clearResult);
})();
