(() => {
  const form = document.getElementById('download-form');
  const input = document.getElementById('url');
  const errorBox = document.getElementById('url-error');
  const submit = document.getElementById('submit-btn');
  const status = document.getElementById('analysis-status');
  const statusLabel = document.getElementById('analysis-label');
  const result = document.getElementById('result');
  const progress = document.getElementById('progress-card');
  const history = document.getElementById('history-list');
  const tool = document.body.dataset.tool;
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  let media = null;
  let chosen = null;
  let pollTimer = null;

  menu.addEventListener('click', () => {
    const opened = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(opened));
  });

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  }
  function formatSize(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) return 'Size unknown';
    return bytes >= 1048576 ? `${(bytes / 1048576).toFixed(1)} MB` : `${(bytes / 1024).toFixed(0)} KB`;
  }
  function formatDuration(seconds) {
    if (!Number.isFinite(seconds) || seconds <= 0) return '';
    const value = Math.floor(seconds);
    return `${Math.floor(value / 60)}:${String(value % 60).padStart(2, '0')}`;
  }
  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = false;
    input.setAttribute('aria-invalid', 'true');
  }
  function clearError() {
    errorBox.textContent = '';
    errorBox.hidden = true;
    input.removeAttribute('aria-invalid');
  }
  function track(event, format = '') {
    if (!media) return;
    fetch('/api/event', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({event,platform:media.platform,tool,format}),keepalive:true}).catch(() => {});
  }
  async function post(path, payload) {
    const response = await fetch(path, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const body = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(body.error || 'The server could not process this request.');
    return body;
  }
  input.addEventListener('input', clearError);
  document.getElementById('paste-btn').addEventListener('click', async () => {
    try { input.value = await navigator.clipboard.readText(); clearError(); input.focus(); }
    catch { input.focus(); showError('Clipboard access is unavailable. Paste the link into the field.'); }
  });

  form.addEventListener('submit', async event => {
    event.preventDefault();
    clearError();
    clearInterval(pollTimer);
    result.hidden = true;
    progress.hidden = true;
    media = null;
    chosen = null;
    const url = input.value.trim();
    if (!url) return showError('Paste a public media URL first.');
    submit.disabled = true;
    submit.textContent = 'Analyzing…';
    status.hidden = false;
    statusLabel.textContent = 'Analyzing URL...';
    try {
      const found = await post('/api/analyze', {url, tool});
      statusLabel.textContent = 'Finding available formats...';
      media = found;
      renderResult(found);
      result.hidden = false;
      result.scrollIntoView({behavior:'smooth',block:'nearest'});
    } catch (error) {
      showError(error.message);
      status.hidden = true;
    } finally {
      submit.disabled = false;
      submit.textContent = 'Download';
      status.hidden = true;
    }
  });

  function renderResult(found) {
    const safeThumb = (() => { try { const url = new URL(found.thumbnail); return url.protocol === 'https:' ? escapeHtml(url.href) : null; } catch { return null; } })();
    const thumb = safeThumb ? `<img class="result-thumb" src="${safeThumb}" alt="Media thumbnail" loading="lazy" referrerpolicy="no-referrer">` : '<div class="result-thumb-placeholder" aria-hidden="true">▶</div>';
    const meta = [found.author ? `@${found.author.replace(/^@/, '')}` : '', formatDuration(found.duration), found.platform].filter(Boolean).map(escapeHtml).join(' · ');
    result.innerHTML = `<div class="result-top">${thumb}<div><span class="section-kicker">${escapeHtml(found.platform.toUpperCase())} · ${escapeHtml(found.type.toUpperCase())}</span><h3>${escapeHtml(found.title || 'Untitled media')}</h3><p class="result-meta">${meta}</p></div></div><div class="format-heading"><h4>Available downloads</h4><span>${found.formats.length} real option${found.formats.length === 1 ? '' : 's'}</span></div><div class="format-list" role="group" aria-label="Available formats">${found.formats.map((item,index) => {
      const dimensions = Array.isArray(item.resolution) && item.resolution.every(Boolean) ? `${item.resolution[0]} × ${item.resolution[1]}` : '';
      const detail = [dimensions, item.bitrate ? `~${item.bitrate} kbps` : ''].filter(Boolean).join(' · ');
      const size = formatSize(item.filesize);
      const sizeLabel = size === 'Size unknown' ? size : `${item.filesize_estimated ? '≈ ' : ''}${size}`;
      return `<button type="button" class="format-option" data-format="${escapeHtml(item.id)}" aria-pressed="${index === 0}"><span class="format-icon">${escapeHtml(item.extension)}</span><span class="format-detail"><strong>${escapeHtml(item.quality || item.extension.toUpperCase())}</strong><small>${escapeHtml(detail || `${item.type} · source format`)}</small></span><span class="format-size">${escapeHtml(sizeLabel)}</span><span class="format-check" aria-hidden="true">${index === 0 ? '✓' : ''}</span></button>`;
    }).join('')}</div><div class="format-actions"><button type="button" id="start-download" class="submit-btn">Prepare download <span aria-hidden="true">↓</span></button></div>`;
    chosen = found.formats[0];
    result.querySelectorAll('.format-option').forEach(button => button.addEventListener('click', () => {
      chosen = found.formats.find(item => item.id === button.dataset.format);
      result.querySelectorAll('.format-option').forEach(option => {
        const active = option === button;
        option.setAttribute('aria-pressed', String(active));
        option.querySelector('.format-check').textContent = active ? '✓' : '';
      });
      track('format_selected', chosen.extension);
    }));
    document.getElementById('start-download').addEventListener('click', startDownload);
  }

  async function startDownload() {
    if (!media || !chosen) return;
    const button = document.getElementById('start-download');
    button.disabled = true;
    button.textContent = 'Preparing…';
    progress.hidden = false;
    document.getElementById('job-title').textContent = media.title || 'Preparing media';
    document.getElementById('job-stage').textContent = 'Preparing download...';
    document.getElementById('job-percent').textContent = '0%';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('job-result').innerHTML = '';
    try {
      const job = await post('/api/download', {analysis_id:media.analysis_id,format_id:chosen.id,tool});
      poll(job.job_id, chosen.extension);
      progress.scrollIntoView({behavior:'smooth',block:'nearest'});
    } catch (error) {
      document.getElementById('job-stage').textContent = 'Could not start';
      document.getElementById('job-result').innerHTML = `<p class="result-error">${escapeHtml(error.message)}</p>`;
      track('error_occurred', chosen.extension);
      button.disabled = false;
      button.innerHTML = 'Prepare download <span aria-hidden="true">↓</span>';
    }
  }

  function poll(jobId, extension) {
    clearInterval(pollTimer);
    const tick = async () => {
      try {
        const response = await fetch(`/api/progress/${encodeURIComponent(jobId)}`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Could not check progress.');
        const percent = Math.max(0, Math.min(100, Number(data.percent) || 0));
        document.getElementById('job-percent').textContent = `${Math.round(percent)}%`;
        document.getElementById('progress-bar').style.width = `${percent}%`;
        document.getElementById('job-stage').textContent = data.stage || data.status;
        document.getElementById('job-meta').textContent = [data.speed, data.eta ? `ETA ${data.eta}` : ''].filter(Boolean).join(' · ');
        if (data.status === 'done') {
          clearInterval(pollTimer);
          document.getElementById('job-stage').textContent = 'Download ready!';
          document.getElementById('job-percent').textContent = '100%';
          document.getElementById('progress-bar').style.width = '100%';
          document.getElementById('job-result').innerHTML = `<a class="ready-link" href="${escapeHtml(data.download_url)}">Save ${escapeHtml(extension.toUpperCase())} file ↓</a>`;
          document.getElementById('start-download').disabled = false;
          document.getElementById('start-download').innerHTML = 'Prepare download <span aria-hidden="true">↓</span>';
          loadHistory();
        } else if (data.status === 'error') {
          throw new Error(data.error || 'Processing failed. Please try again.');
        }
      } catch (error) {
        clearInterval(pollTimer);
        document.getElementById('job-stage').textContent = 'Could not process this media';
        document.getElementById('job-result').innerHTML = `<p class="result-error">${escapeHtml(error.message)}</p>`;
        track('error_occurred', extension);
        document.getElementById('start-download').disabled = false;
        document.getElementById('start-download').innerHTML = 'Prepare download <span aria-hidden="true">↓</span>';
        loadHistory();
      }
    };
    tick();
    pollTimer = setInterval(tick, 1100);
  }

  async function loadHistory() {
    try {
      const response = await fetch('/api/history');
      const rows = await response.json();
      if (!rows.length) { history.innerHTML = '<p>No downloads in this browser yet.</p>'; return; }
      history.innerHTML = rows.map(row => `<div class="history-row"><div><strong>${escapeHtml(row.title || 'Media file')}</strong><small>${escapeHtml(row.quality)} · ${escapeHtml(row.status)} · ${escapeHtml(row.created_at)} UTC</small></div>${row.download_url ? `<a href="${escapeHtml(row.download_url)}">Save</a>` : ''}<button type="button" data-delete="${escapeHtml(row.job_id)}">Remove</button></div>`).join('');
    } catch { history.innerHTML = '<p>Could not load history.</p>'; }
  }
  history.addEventListener('click', async event => {
    const jobId = event.target.dataset.delete;
    if (!jobId) return;
    event.target.disabled = true;
    await fetch(`/api/history/${encodeURIComponent(jobId)}`, {method:'DELETE'});
    loadHistory();
  });
  document.querySelector('.history-section details').addEventListener('toggle', event => { if (event.target.open) loadHistory(); });
})();
