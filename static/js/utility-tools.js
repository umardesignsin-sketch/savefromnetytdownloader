(() => {
  const form = document.getElementById('utility-form');
  if (!form) return;
  const status = document.getElementById('utility-status');
  const result = document.getElementById('utility-result');
  const button = document.getElementById('utility-submit');
  const link = document.getElementById('utility-download');
  const detail = document.getElementById('utility-result-detail');
  const preview = document.getElementById('utility-preview');
  const fileInput = document.getElementById('utility-file');
  const hint = document.querySelector('.utility-hint');
  const originalHint = hint?.textContent || '';
  let resultUrl = null;
  const size = bytes => bytes >= 1048576 ? `${(bytes / 1048576).toFixed(2)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`;
  function reset() {
    result.hidden = true;
    preview.hidden = true;
    if (resultUrl) URL.revokeObjectURL(resultUrl);
    resultUrl = null;
  }
  form.addEventListener('change', event => {
    reset();
    if (event.target !== fileInput || !fileInput?.files[0] || !hint) return;
    hint.textContent = originalHint;
    const sourceUrl = URL.createObjectURL(fileInput.files[0]);
    const source = document.createElement(form.dataset.tool === 'audio-cutter' ? 'audio' : 'video');
    source.preload = 'metadata';
    source.onloadedmetadata = () => {
      if (Number.isFinite(source.duration) && source.duration > 0) {
        hint.textContent = `${originalHint} Detected duration: ${source.duration.toFixed(1)} seconds.`;
        const end = document.getElementById('utility-end');
        if (end) end.value = Math.max(0.1, Math.min(source.duration, form.dataset.tool === 'audio-cutter' ? 30 : form.dataset.tool === 'video-trimmer' ? 10 : 3)).toFixed(1);
      }
      URL.revokeObjectURL(sourceUrl);
    };
    source.onerror = () => URL.revokeObjectURL(sourceUrl);
    source.src = sourceUrl;
  });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    reset();
    status.classList.remove('error');
    const thumbnail = form.dataset.mode === 'thumbnail';
    const selected = thumbnail ? null : document.getElementById('utility-file').files[0];
    if (!thumbnail && (!selected || selected.size > 16 * 1024 * 1024)) {
      status.textContent = 'Choose a media file no larger than 16 MB.';
      status.classList.add('error');
      return;
    }
    const start = document.getElementById('utility-start');
    const end = document.getElementById('utility-end');
    if (start && end && (Number(end.value) <= 0 || (form.dataset.tool !== 'video-to-gif' && Number(end.value) <= Number(start.value)))) {
      status.textContent = 'Enter a valid start and end time.';
      status.classList.add('error');
      return;
    }
    button.disabled = true;
    status.textContent = thumbnail ? 'Finding the thumbnail…' : 'Inspecting and processing your file…';
    try {
      const response = await fetch(thumbnail ? '/api/thumbnail' : '/api/media/process', {
        method: 'POST',
        ...(thumbnail ? { headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url: document.getElementById('utility-url').value }) }
          : { body: (() => { const data = new FormData(form); data.set('tool', form.dataset.tool); return data; })() }),
      });
      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.error || 'This file could not be processed. Try another source.');
      }
      const blob = await response.blob();
      resultUrl = URL.createObjectURL(blob);
      const disposition = response.headers.get('content-disposition') || '';
      const filename = disposition.match(/filename="?([^";]+)"?/i)?.[1] || (thumbnail ? 'youtube-thumbnail.jpg' : 'savefromnet-output');
      link.href = resultUrl;
      link.download = filename;
      const original = Number(response.headers.get('X-SFN-Input-Bytes')) || selected?.size;
      detail.textContent = original ? `${size(original)} source → ${size(blob.size)} result` : `${size(blob.size)} JPG thumbnail`;
      if (blob.type.startsWith('image/')) { preview.src = resultUrl; preview.hidden = false; }
      result.hidden = false;
      status.textContent = 'Ready. Save the file below.';
      result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
      status.textContent = error.message;
      status.classList.add('error');
    } finally {
      button.disabled = false;
    }
  });
  window.addEventListener('pagehide', reset);
})();
