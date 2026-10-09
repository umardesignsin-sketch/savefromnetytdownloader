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
  const language = document.body.dataset.lang || 'en';
  const translations = {
    es: {unknownSize:'Tamaño desconocido', serverError:'El servidor no pudo procesar la solicitud.', clipboard:'No se puede acceder al portapapeles. Pega el enlace en el campo.', missingUrl:'Primero pega una URL pública.', analyzing:'Analizando…', analyzingUrl:'Analizando el enlace...', findingFormats:'Buscando formatos disponibles...', submit:'Analizar enlace', thumbnail:'Miniatura del contenido', untitled:'Contenido sin título', available:'Descargas disponibles', options:'opciones reales', option:'opción real', formats:'Formatos disponibles', source:'formato de origen', prepare:'Preparar descarga', preparing:'Preparando…', preparingFile:'Preparando archivo', preparingDownload:'Preparando descarga...', startFailed:'No se pudo iniciar', progressFailed:'No se pudo consultar el progreso.', ready:'¡Descarga lista!', save:'Guardar archivo', processingFailed:'Error al procesar. Inténtalo de nuevo.', mediaFailed:'No se pudo procesar este contenido', emptyHistory:'Aún no hay descargas en este navegador.', mediaFile:'Archivo multimedia', remove:'Eliminar', historyFailed:'No se pudo cargar el historial.'},
    fr: {unknownSize:'Taille inconnue', serverError:'Le serveur n’a pas pu traiter la demande.', clipboard:'Le presse-papiers est inaccessible. Collez le lien dans le champ.', missingUrl:'Collez d’abord un lien public.', analyzing:'Analyse…', analyzingUrl:'Analyse du lien...', findingFormats:'Recherche des formats disponibles...', submit:'Analyser le lien', thumbnail:'Miniature du contenu', untitled:'Contenu sans titre', available:'Téléchargements disponibles', options:'options réelles', option:'option réelle', formats:'Formats disponibles', source:'format source', prepare:'Préparer le téléchargement', preparing:'Préparation…', preparingFile:'Préparation du fichier', preparingDownload:'Préparation du téléchargement...', startFailed:'Démarrage impossible', progressFailed:'Impossible de vérifier la progression.', ready:'Téléchargement prêt !', save:'Enregistrer le fichier', processingFailed:'Échec du traitement. Réessayez.', mediaFailed:'Impossible de traiter ce contenu', emptyHistory:'Aucun téléchargement dans ce navigateur.', mediaFile:'Fichier multimédia', remove:'Supprimer', historyFailed:'Impossible de charger l’historique.'}
  };
  const t = (key, english) => translations[language]?.[key] || english;
  const stages = {
    es: {Queued:'En cola', Starting:'Iniciando', Downloading:'Descargando', Merging:'Combinando vídeo y audio', 'Extracting audio':'Extrayendo audio', Complete:'Completado', Failed:'Error'},
    fr: {Queued:'En attente', Starting:'Démarrage', Downloading:'Téléchargement', Merging:'Fusion vidéo et audio', 'Extracting audio':"Extraction de l'audio", Complete:'Terminé', Failed:'Échec'}
  };
  const errors = {
    es: {invalid_url:'El enlace no es una URL pública compatible.', unsupported:'Esta URL no es compatible. Usa un enlace directo a una publicación.', wrong_platform:'Usa un enlace de la plataforma de esta herramienta.', wrong_content_type:'Este enlace necesita una herramienta para otro tipo de contenido.', no_formats:'No hay archivos públicos accesibles para este enlace.', private:'El contenido es privado o requiere iniciar sesión.', restricted:'El contenido está restringido o requiere iniciar sesión.', region_restricted:'El contenido no está disponible en la región del servidor.', deleted:'La publicación se eliminó o no existe.', live:'No se pueden procesar emisiones en directo activas.', timeout:'La fuente tardó demasiado. Inténtalo de nuevo.', too_large:'Este contenido supera el límite de procesamiento.', rate_limited:'Demasiadas solicitudes. Inténtalo de nuevo en un minuto.', busy:'El servicio está ocupado. Inténtalo de nuevo pronto.', expired:'El análisis caducó. Pega de nuevo el enlace.', source_unavailable:'No se pudo acceder a esta publicación pública.', server_error:'El servicio no está disponible ahora. Inténtalo más tarde.'},
    fr: {invalid_url:'Ce lien n’est pas une URL publique compatible.', unsupported:'Cette URL n’est pas prise en charge. Utilisez le lien direct d’une publication.', wrong_platform:'Utilisez un lien de la plateforme de cet outil.', wrong_content_type:'Ce lien nécessite un outil adapté à un autre type de contenu.', no_formats:'Aucun fichier public accessible pour ce lien.', private:'Ce contenu est privé ou nécessite une connexion.', restricted:'Ce contenu est restreint ou nécessite une connexion.', region_restricted:'Ce contenu est indisponible dans la région du serveur.', deleted:'Cette publication a été supprimée ou est introuvable.', live:'Les diffusions en direct ne peuvent pas être traitées.', timeout:'La source a mis trop de temps à répondre. Réessayez.', too_large:'Ce contenu dépasse la limite de traitement.', rate_limited:'Trop de demandes. Réessayez dans une minute.', busy:'Le service est occupé. Réessayez bientôt.', expired:'L’analyse a expiré. Collez de nouveau le lien.', source_unavailable:'Cette publication publique est inaccessible.', server_error:'Le service est indisponible. Réessayez plus tard.'}
  };
  let media = null;
  let chosen = null;
  let pollTimer = null;

  menu.addEventListener('click', () => {
    const opened = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(opened));
  });

  // Trust and directory pages share the navigation but do not need the API UI.
  if (!form) return;

  if (document.body.dataset.pageType === 'tool') {
    fetch('/api/event', {method:'POST', headers:{'Content-Type':'application/json'},
      body:JSON.stringify({event:'tool_page_view', platform:document.body.dataset.platform, tool}),
      keepalive:true}).catch(() => {});
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  }
  function formatSize(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) return t('unknownSize', 'Size unknown');
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
    if (!response.ok) throw new Error(errors[language]?.[body.code] || body.error || t('serverError', 'The server could not process this request.'));
    return body;
  }
  input.addEventListener('input', clearError);
  document.getElementById('paste-btn').addEventListener('click', async () => {
    try { input.value = await navigator.clipboard.readText(); clearError(); input.focus(); }
    catch { input.focus(); showError(t('clipboard', 'Clipboard access is unavailable. Paste the link into the field.')); }
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
    if (!url) return showError(t('missingUrl', 'Paste a public media URL first.'));
    submit.disabled = true;
    submit.textContent = t('analyzing', 'Analyzing…');
    status.hidden = false;
    statusLabel.textContent = t('analyzingUrl', 'Analyzing URL...');
    try {
      const found = await post('/api/analyze', {url, tool});
      statusLabel.textContent = t('findingFormats', 'Finding available formats...');
      media = found;
      renderResult(found);
      result.hidden = false;
      result.scrollIntoView({behavior:'smooth',block:'nearest'});
    } catch (error) {
      showError(error.message);
      status.hidden = true;
    } finally {
      submit.disabled = false;
      submit.textContent = t('submit', 'Download');
      status.hidden = true;
    }
  });

  function renderResult(found) {
    const safeThumb = (() => { try { const url = new URL(found.thumbnail); return url.protocol === 'https:' ? escapeHtml(url.href) : null; } catch { return null; } })();
    const thumb = safeThumb ? `<img class="result-thumb" src="${safeThumb}" alt="${t('thumbnail', 'Media thumbnail')}" loading="lazy" referrerpolicy="no-referrer">` : '<div class="result-thumb-placeholder" aria-hidden="true">▶</div>';
    const meta = [found.author ? `@${found.author.replace(/^@/, '')}` : '', formatDuration(found.duration), found.platform].filter(Boolean).map(escapeHtml).join(' · ');
    result.innerHTML = `<div class="result-top">${thumb}<div><span class="section-kicker">${escapeHtml(found.platform.toUpperCase())} · ${escapeHtml(found.type.toUpperCase())}</span><h3>${escapeHtml(found.title || t('untitled', 'Untitled media'))}</h3><p class="result-meta">${meta}</p></div></div><div class="format-heading"><h4>${t('available', 'Available downloads')}</h4><span>${found.formats.length} ${found.formats.length === 1 ? t('option', 'real option') : t('options', 'real options')}</span></div><div class="format-list" role="group" aria-label="${t('formats', 'Available formats')}">${found.formats.map((item,index) => {
      const dimensions = Array.isArray(item.resolution) && item.resolution.every(Boolean) ? `${item.resolution[0]} × ${item.resolution[1]}` : '';
      const detail = [dimensions, item.bitrate ? `~${item.bitrate} kbps` : ''].filter(Boolean).join(' · ');
      const size = formatSize(item.filesize);
      const sizeLabel = size === t('unknownSize', 'Size unknown') ? size : `${item.filesize_estimated ? '≈ ' : ''}${size}`;
      return `<button type="button" class="format-option" data-format="${escapeHtml(item.id)}" aria-pressed="${index === 0}"><span class="format-icon">${escapeHtml(item.extension)}</span><span class="format-detail"><strong>${escapeHtml(item.quality || item.extension.toUpperCase())}</strong><small>${escapeHtml(detail || `${item.type} · ${t('source', 'source format')}`)}</small></span><span class="format-size">${escapeHtml(sizeLabel)}</span><span class="format-check" aria-hidden="true">${index === 0 ? '✓' : ''}</span></button>`;
    }).join('')}</div><div class="format-actions"><button type="button" id="start-download" class="submit-btn">${t('prepare', 'Prepare download')} <span aria-hidden="true">↓</span></button></div>`;
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
    button.textContent = t('preparing', 'Preparing…');
    progress.hidden = false;
    document.getElementById('job-title').textContent = media.title || t('preparingFile', 'Preparing media');
    document.getElementById('job-stage').textContent = t('preparingDownload', 'Preparing download...');
    document.getElementById('job-percent').textContent = '0%';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('job-result').innerHTML = '';
    try {
      const job = await post('/api/download', {analysis_id:media.analysis_id,format_id:chosen.id,tool});
      poll(job.job_id, chosen.extension);
      progress.scrollIntoView({behavior:'smooth',block:'nearest'});
    } catch (error) {
      document.getElementById('job-stage').textContent = t('startFailed', 'Could not start');
      document.getElementById('job-result').innerHTML = `<p class="result-error">${escapeHtml(error.message)}</p>`;
      track('error_occurred', chosen.extension);
      track('download_failed', chosen.extension);
      button.disabled = false;
      button.innerHTML = `${t('prepare', 'Prepare download')} <span aria-hidden="true">↓</span>`;
    }
  }

  function poll(jobId, extension) {
    clearInterval(pollTimer);
    const tick = async () => {
      try {
        const response = await fetch(`/api/progress/${encodeURIComponent(jobId)}`);
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || t('progressFailed', 'Could not check progress.'));
        const percent = Math.max(0, Math.min(100, Number(data.percent) || 0));
        document.getElementById('job-percent').textContent = `${Math.round(percent)}%`;
        document.getElementById('progress-bar').style.width = `${percent}%`;
        const stage = data.stage || data.status;
        document.getElementById('job-stage').textContent = stages[language]?.[stage] || stage;
        document.getElementById('job-meta').textContent = [data.speed, data.eta ? `${language === 'es' ? 'Tiempo restante' : language === 'fr' ? 'Temps restant' : 'ETA'} ${data.eta}` : ''].filter(Boolean).join(' · ');
        if (data.status === 'done') {
          clearInterval(pollTimer);
          document.getElementById('job-stage').textContent = t('ready', 'Download ready!');
          document.getElementById('job-percent').textContent = '100%';
          document.getElementById('progress-bar').style.width = '100%';
          document.getElementById('job-result').innerHTML = `<a class="ready-link" href="${escapeHtml(data.download_url)}">${t('save', 'Save')} ${escapeHtml(extension.toUpperCase())} ${language === 'en' ? 'file ' : ''}↓</a>`;
          document.getElementById('start-download').disabled = false;
          document.getElementById('start-download').innerHTML = `${t('prepare', 'Prepare download')} <span aria-hidden="true">↓</span>`;
          loadHistory();
        } else if (data.status === 'error') {
          throw new Error(data.error || t('processingFailed', 'Processing failed. Please try again.'));
        }
      } catch (error) {
        clearInterval(pollTimer);
        document.getElementById('job-stage').textContent = t('mediaFailed', 'Could not process this media');
        document.getElementById('job-result').innerHTML = `<p class="result-error">${escapeHtml(error.message)}</p>`;
        track('error_occurred', extension);
        track('download_failed', extension);
        document.getElementById('start-download').disabled = false;
        document.getElementById('start-download').innerHTML = `${t('prepare', 'Prepare download')} <span aria-hidden="true">↓</span>`;
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
      if (!rows.length) { history.innerHTML = `<p>${t('emptyHistory', 'No downloads in this browser yet.')}</p>`; return; }
      history.innerHTML = rows.map(row => `<div class="history-row"><div><strong>${escapeHtml(row.title || t('mediaFile', 'Media file'))}</strong><small>${escapeHtml(row.quality)} · ${escapeHtml(row.status)} · ${escapeHtml(row.created_at)} UTC</small></div>${row.download_url ? `<a href="${escapeHtml(row.download_url)}">${t('save', 'Save')}</a>` : ''}<button type="button" data-delete="${escapeHtml(row.job_id)}">${t('remove', 'Remove')}</button></div>`).join('');
    } catch { history.innerHTML = `<p>${t('historyFailed', 'Could not load history.')}</p>`; }
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
