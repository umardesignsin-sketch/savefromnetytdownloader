const form = document.getElementById('download-form');
const urlInput = document.getElementById('url');
const urlError = document.getElementById('url-error');
const qualitySelect = document.getElementById('quality');
const submitBtn = document.getElementById('submit-btn');

const progressCard = document.getElementById('progress-card');
const bar = document.getElementById('progress-bar');
const pctLabel = document.getElementById('job-percent');
const titleLabel = document.getElementById('job-title');
const stageLabel = document.getElementById('job-stage');
const metaLabel = document.getElementById('job-meta');
const resultBox = document.getElementById('job-result');

const historyBody = document.getElementById('history-body');

const YT_PATTERN = /^(https?:\/\/)?(www\.|m\.|music\.)?(youtube\.com\/(watch\?.*v=|shorts\/|live\/|embed\/)[\w-]{11}|youtu\.be\/[\w-]{11})/i;

let pollTimer = null;

function showUrlError(message) {
  urlInput.classList.add('is-invalid');
  urlError.textContent = message;
}

function clearUrlError() {
  urlInput.classList.remove('is-invalid');
  urlError.textContent = '';
}

urlInput.addEventListener('input', clearUrlError);

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearUrlError();

  const url = urlInput.value.trim();
  if (!url) return showUrlError('Please paste a YouTube URL.');
  if (!YT_PATTERN.test(url)) {
    return showUrlError('That doesn’t look like a YouTube video link.');
  }

  setBusy(true);
  resetProgress();

  try {
    const res = await fetch('/api/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, quality: qualitySelect.value }),
    });
    const data = await res.json();
    if (!res.ok) {
      setBusy(false);
      progressCard.classList.add('d-none');
      return showUrlError(data.error || 'Could not start the download.');
    }
    poll(data.job_id);
  } catch (err) {
    setBusy(false);
    progressCard.classList.add('d-none');
    showUrlError('Could not reach the server.');
  }
});

function setBusy(busy) {
  submitBtn.disabled = busy;
  submitBtn.innerHTML = busy
    ? '<span class="spinner-border spinner-border-sm me-2"></span>Working…'
    : 'Download';
}

function resetProgress() {
  clearInterval(pollTimer);
  progressCard.classList.remove('d-none');
  resultBox.classList.add('d-none');
  resultBox.innerHTML = '';
  bar.className = 'progress-bar progress-bar-striped progress-bar-animated';
  bar.style.width = '0%';
  pctLabel.textContent = '0%';
  titleLabel.textContent = 'Preparing…';
  stageLabel.textContent = 'Queued';
  metaLabel.textContent = '';
}

function poll(jobId) {
  const tick = async () => {
    let state;
    try {
      const res = await fetch(`/api/progress/${jobId}`);
      state = await res.json();
      if (!res.ok) throw new Error(state.error || 'Lost track of this download.');
    } catch (err) {
      clearInterval(pollTimer);
      setBusy(false);
      return renderError(err.message);
    }

    const pct = Math.min(100, Number(state.percent) || 0);
    bar.style.width = `${pct}%`;
    pctLabel.textContent = `${pct.toFixed(1)}%`;
    stageLabel.textContent = state.stage || state.status;
    if (state.title) titleLabel.textContent = state.title;
    metaLabel.textContent = [state.speed, state.eta ? `ETA ${state.eta}` : null]
      .filter(Boolean).join(' · ');

    if (state.status === 'done') {
      clearInterval(pollTimer);
      setBusy(false);
      bar.className = 'progress-bar bg-success';
      bar.style.width = '100%';
      pctLabel.textContent = '100%';
      metaLabel.textContent = '';
      resultBox.classList.remove('d-none');
      resultBox.innerHTML =
        `<a class="btn btn-success" href="/api/file/${jobId}">Save file</a>`;
      loadHistory();
    } else if (state.status === 'error') {
      clearInterval(pollTimer);
      setBusy(false);
      renderError(state.error || 'Download failed.');
      loadHistory();
    }
  };

  tick();
  pollTimer = setInterval(tick, 800);
}

function renderError(message) {
  bar.className = 'progress-bar bg-danger';
  bar.style.width = '100%';
  pctLabel.textContent = '—';
  stageLabel.textContent = 'Failed';
  metaLabel.textContent = '';
  resultBox.classList.remove('d-none');
  resultBox.innerHTML =
    `<div class="alert alert-danger mb-0 py-2">${escapeHtml(message)}</div>`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text ?? '';
  return div.innerHTML;
}

const STATUS_BADGE = {
  done: 'text-bg-success',
  error: 'text-bg-danger',
  downloading: 'text-bg-primary',
  queued: 'text-bg-secondary',
};

async function loadHistory() {
  try {
    const rows = await (await fetch('/api/history')).json();
    if (!rows.length) {
      historyBody.innerHTML =
        '<tr><td colspan="5" class="text-secondary py-4 text-center">No downloads yet.</td></tr>';
      return;
    }
    historyBody.innerHTML = rows.map((r) => `
      <tr>
        <td class="title-cell" title="${escapeHtml(r.title || r.url)}">
          ${escapeHtml(r.title || r.url)}
          ${r.error ? `<div class="text-danger small">${escapeHtml(r.error)}</div>` : ''}
        </td>
        <td><span class="badge text-bg-dark">${escapeHtml(r.quality)}</span></td>
        <td><span class="badge ${STATUS_BADGE[r.status] || 'text-bg-secondary'}">${escapeHtml(r.status)}</span></td>
        <td class="text-secondary small">${escapeHtml(r.created_at)} UTC</td>
        <td class="text-end text-nowrap">
          ${r.available
            ? `<a class="btn btn-sm btn-outline-success" href="/api/file/${r.job_id}">Save</a>`
            : ''}
          <button class="btn btn-sm btn-outline-secondary" data-delete="${r.job_id}">Remove</button>
        </td>
      </tr>`).join('');
  } catch (err) {
    historyBody.innerHTML =
      '<tr><td colspan="5" class="text-danger py-4 text-center">Could not load history.</td></tr>';
  }
}

historyBody.addEventListener('click', async (event) => {
  const jobId = event.target.dataset?.delete;
  if (!jobId) return;
  event.target.disabled = true;
  await fetch(`/api/history/${jobId}`, { method: 'DELETE' });
  loadHistory();
});

document.getElementById('refresh-history').addEventListener('click', loadHistory);
loadHistory();
