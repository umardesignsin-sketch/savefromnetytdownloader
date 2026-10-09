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
  const cropStage = document.getElementById('crop-stage');
  const cropPreview = document.getElementById('crop-preview');
  const cropSelection = document.getElementById('crop-selection');
  let previousUrl = null;
  let previewUrl = null;
  let cropSize = null;
  const size = value => value >= 1048576 ? `${(value / 1048576).toFixed(2)} MB` : `${Math.max(1, Math.round(value / 1024))} KB`;
  function clearResult() {
    result.hidden = true;
    if (previousUrl) URL.revokeObjectURL(previousUrl);
    previousUrl = null;
  }
  function drawCrop() {
    if (!cropSize) return;
    const x = Number(document.getElementById('crop-x').value) || 0;
    const y = Number(document.getElementById('crop-y').value) || 0;
    const width = Number(document.getElementById('crop-width').value) || 0;
    const height = Number(document.getElementById('crop-height').value) || 0;
    cropSelection.style.left = `${100 * x / cropSize.width}%`;
    cropSelection.style.top = `${100 * y / cropSize.height}%`;
    cropSelection.style.width = `${100 * width / cropSize.width}%`;
    cropSelection.style.height = `${100 * height / cropSize.height}%`;
  }
  if (cropStage) {
    for (const id of ['crop-x', 'crop-y', 'crop-width', 'crop-height']) document.getElementById(id).addEventListener('input', drawCrop);
    let anchor = null;
    const point = event => {
      const bounds = cropPreview.getBoundingClientRect();
      return {
        x: Math.max(0, Math.min(cropSize.width, Math.round((event.clientX - bounds.left) * cropSize.width / bounds.width))),
        y: Math.max(0, Math.min(cropSize.height, Math.round((event.clientY - bounds.top) * cropSize.height / bounds.height))),
      };
    };
    cropStage.addEventListener('pointerdown', event => {
      if (!cropSize) return;
      anchor = point(event);
      cropStage.setPointerCapture(event.pointerId);
    });
    cropStage.addEventListener('pointermove', event => {
      if (!anchor || !cropSize) return;
      const current = point(event);
      const left = Math.min(anchor.x, current.x);
      const top = Math.min(anchor.y, current.y);
      document.getElementById('crop-x').value = left;
      document.getElementById('crop-y').value = top;
      document.getElementById('crop-width').value = Math.max(1, Math.min(cropSize.width - left, Math.abs(current.x - anchor.x)));
      document.getElementById('crop-height').value = Math.max(1, Math.min(cropSize.height - top, Math.abs(current.y - anchor.y)));
      drawCrop();
    });
    cropStage.addEventListener('pointerup', () => { anchor = null; });
    cropStage.addEventListener('pointercancel', () => { anchor = null; });
  }
  file.addEventListener('change', () => {
    clearResult();
    status.textContent = '';
    if (file.files[0]) label.textContent = `${file.files[0].name} · ${size(file.files[0].size)}`;
    if (form.dataset.tool === 'image-cropper' && quality) {
      const png = file.files[0]?.type === 'image/png' || file.files[0]?.name.toLowerCase().endsWith('.png');
      quality.closest('label').hidden = Boolean(png);
    }
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    previewUrl = null;
    cropSize = null;
    if (cropStage) cropStage.hidden = true;
    if (form.dataset.tool === 'image-cropper' && file.files[0]) {
      previewUrl = URL.createObjectURL(file.files[0]);
      const currentUrl = previewUrl;
      const preview = new Image();
      preview.onload = () => {
        if (previewUrl !== currentUrl) return;
        cropSize = { width: preview.naturalWidth, height: preview.naturalHeight };
        document.getElementById('crop-size-hint').textContent = `Image size: ${preview.naturalWidth} × ${preview.naturalHeight} pixels. Crop coordinates use this displayed orientation.`;
        document.getElementById('crop-x').value = 0;
        document.getElementById('crop-y').value = 0;
        document.getElementById('crop-width').value = preview.naturalWidth;
        document.getElementById('crop-height').value = preview.naturalHeight;
        cropPreview.src = currentUrl;
        cropStage.hidden = false;
        drawCrop();
      };
      preview.onerror = () => {
        if (previewUrl !== currentUrl) return;
        document.getElementById('crop-size-hint').textContent = 'Enter the crop dimensions in pixels. This browser cannot preview this image format.';
        URL.revokeObjectURL(currentUrl);
        previewUrl = null;
      };
      preview.src = currentUrl;
    }
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
  window.addEventListener('pagehide', () => { clearResult(); if (previewUrl) URL.revokeObjectURL(previewUrl); });
})();
