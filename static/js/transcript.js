(() => {
  const form = document.getElementById('transcript-form');
  if (!form) return;
  const input = document.getElementById('transcript-url');
  const submit = document.getElementById('transcript-submit');
  const error = document.getElementById('transcript-error');
  const status = document.getElementById('transcript-status');
  const result = document.getElementById('transcript-result');
  const language = document.getElementById('transcript-language');
  const search = document.getElementById('transcript-search');
  const cues = document.getElementById('transcript-cues');
  const count = document.getElementById('transcript-count');
  const actionStatus = document.getElementById('transcript-action-status');
  let transcript = null;

  function time(ms, separator = '.') {
    const value = Math.max(0, Math.floor(ms));
    const hours = Math.floor(value / 3600000);
    const minutes = Math.floor(value / 60000) % 60;
    const seconds = Math.floor(value / 1000) % 60;
    const millis = value % 1000;
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}${separator}${String(millis).padStart(3, '0')}`;
  }

  function showError(message) {
    error.textContent = message;
    error.hidden = false;
    input.setAttribute('aria-invalid', 'true');
  }

  function clearError() {
    error.textContent = '';
    error.hidden = true;
    input.removeAttribute('aria-invalid');
  }

  function renderCues() {
    if (!transcript) return;
    const query = search.value.trim().toLocaleLowerCase();
    const matches = transcript.segments.filter(item => item.text.toLocaleLowerCase().includes(query));
    const fragment = document.createDocumentFragment();
    for (const item of matches) {
      const row = document.createElement('li');
      const jump = document.createElement('a');
      jump.className = 'transcript-timestamp';
      jump.href = `${transcript.url}&t=${Math.floor(item.start_ms / 1000)}s`;
      jump.target = '_blank';
      jump.rel = 'noopener noreferrer';
      jump.textContent = time(item.start_ms).replace(/^00:/, '').replace(/\.\d{3}$/, '');
      jump.setAttribute('aria-label', `Open video at ${jump.textContent}`);
      const words = document.createElement('span');
      words.textContent = item.text;
      row.append(jump, words);
      fragment.append(row);
    }
    cues.replaceChildren(fragment);
    count.textContent = query
      ? `${matches.length} of ${transcript.segments.length} caption cues match your search.`
      : `${transcript.segments.length} caption cues · click a timestamp to open that moment on YouTube.`;
  }

  function render(data) {
    transcript = data;
    document.getElementById('transcript-title').textContent = data.title;
    document.getElementById('transcript-meta').textContent = [data.author, data.duration ? `${Math.floor(data.duration / 60)} min` : '', data.language].filter(Boolean).join(' · ');
    document.getElementById('transcript-source').href = data.url;
    document.getElementById('transcript-track-note').textContent = data.kind === 'manual'
      ? 'This is a creator-supplied caption track. Review it against the video before reuse.'
      : 'This is an automatic caption or translation track. Names and punctuation may be inaccurate.';
    language.replaceChildren(...data.languages.map(item => {
      const option = document.createElement('option');
      option.value = item.code;
      option.textContent = `${item.code} · ${item.kind === 'manual' ? 'manual' : 'automatic'}`;
      return option;
    }));
    language.value = data.language;
    search.value = '';
    renderCues();
    result.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  async function loadTranscript(selectedLanguage) {
    clearError();
    submit.disabled = true;
    language.disabled = true;
    status.textContent = selectedLanguage ? 'Loading that caption language…' : 'Checking available captions…';
    status.hidden = false;
    try {
      const response = await fetch('/api/transcript', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: input.value.trim(), ...(selectedLanguage ? { language: selectedLanguage } : {}) }),
      });
      const body = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(body.error || 'The transcript could not be loaded. Please try again.');
      render(body);
    } catch (failure) {
      showError(failure.message);
      if (transcript) language.value = transcript.language;
    } finally {
      submit.disabled = false;
      language.disabled = false;
      status.hidden = true;
    }
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    transcript = null;
    result.hidden = true;
    if (!input.value.trim()) return showError('Paste a public YouTube video link first.');
    loadTranscript();
  });
  input.addEventListener('input', clearError);
  document.getElementById('transcript-paste').addEventListener('click', async () => {
    try { input.value = await navigator.clipboard.readText(); clearError(); input.focus(); }
    catch { input.focus(); showError('Clipboard access is unavailable. Paste the link into the field.'); }
  });
  language.addEventListener('change', () => loadTranscript(language.value));
  search.addEventListener('input', renderCues);

  const plainText = () => transcript.segments.map(item => item.text).join('\n') + '\n';
  function subtitle(format) {
    return (format === 'vtt' ? 'WEBVTT\n\n' : '') + transcript.segments.map((item, index) =>
      `${format === 'srt' ? `${index + 1}\n` : ''}${time(item.start_ms, format === 'srt' ? ',' : '.')} --> ${time(item.end_ms, format === 'srt' ? ',' : '.')}\n${item.text}\n`
    ).join('\n');
  }
  function save(extension, content) {
    const blob = new Blob([content], { type: extension === 'txt' ? 'text/plain;charset=utf-8' : 'text/vtt;charset=utf-8' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const id = new URL(transcript.url).searchParams.get('v') || 'video';
    link.href = href;
    link.download = `youtube-transcript-${id}-${transcript.language}.${extension}`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(href), 30000);
    actionStatus.textContent = `${extension.toUpperCase()} download started.`;
  }
  document.getElementById('transcript-copy').addEventListener('click', async () => {
    if (!transcript) return;
    try { await navigator.clipboard.writeText(plainText()); actionStatus.textContent = 'Transcript text copied.'; }
    catch { actionStatus.textContent = 'Copy is unavailable in this browser. Download the TXT file instead.'; }
  });
  for (const extension of ['txt', 'srt', 'vtt']) {
    document.getElementById(`transcript-${extension}`).addEventListener('click', () => {
      if (transcript) save(extension, extension === 'txt' ? plainText() : subtitle(extension));
    });
  }
})();
