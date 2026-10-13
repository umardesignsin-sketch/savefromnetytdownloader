import { backgroundIssues, computeCrop, estimateCrown, fileIssues, poseIssues, setJpegDpi, sheetLayout } from './passport-core.mjs';

const VISION = 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21';
const FACE_MODEL = 'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task';
const PERSON_MODEL = 'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/1/selfie_segmenter.tflite';
const ANALYSIS_EDGE = 1280;
const FORMATS = { 'image/jpeg': 'JPEG', 'image/png': 'PNG', 'image/webp': 'WEBP', 'image/heic': 'HEIC', 'image/heif': 'HEIF' };

const form = document.getElementById('passport-form');
const $ = id => document.getElementById(id);
let modelsPromise = null;
const urls = [];

function loadModels() {
  if (!modelsPromise) modelsPromise = (async () => {
    const { FilesetResolver, FaceLandmarker, ImageSegmenter } = await import(`${VISION}/vision_bundle.mjs`);
    const vision = await FilesetResolver.forVisionTasks(`${VISION}/wasm`);
    const [faces, person] = await Promise.all([
      FaceLandmarker.createFromOptions(vision, { baseOptions: { modelAssetPath: FACE_MODEL }, runningMode: 'IMAGE', numFaces: 2, outputFaceBlendshapes: true }),
      ImageSegmenter.createFromOptions(vision, { baseOptions: { modelAssetPath: PERSON_MODEL }, runningMode: 'IMAGE', outputConfidenceMasks: true, outputCategoryMask: false }),
    ]);
    return { faces, person };
  })().catch(error => { modelsPromise = null; throw error; });
  return modelsPromise;
}

function clearOutput() {
  urls.splice(0).forEach(url => URL.revokeObjectURL(url));
  $('passport-output').hidden = true;
  $('passport-checks').innerHTML = '';
  $('passport-downloads').hidden = true;
}

function setStatus(text, isError = false) {
  const status = $('passport-status');
  status.textContent = text;
  status.classList.toggle('error', isError);
}

function renderChecks(items) {
  const list = $('passport-checks');
  list.innerHTML = '';
  for (const { ok, text } of items) {
    const item = document.createElement('li');
    item.className = ok ? 'check-pass' : 'check-warn';
    item.textContent = `${ok ? '✓' : '!'} ${text}`;
    list.append(item);
  }
}

// Find the topmost row where the person mask covers part of the face's column band.
function hairTop(mask, width, left, right, chinY) {
  const from = Math.max(0, Math.floor(left));
  const to = Math.min(width - 1, Math.ceil(right));
  const band = Math.max(1, to - from + 1);
  for (let y = 0; y < chinY; y++) {
    let covered = 0;
    for (let x = from; x <= to; x++) if (mask[y * width + x] > 0.5) covered++;
    if (covered / band >= 0.25) return y;
  }
  return null;
}

function backgroundStats(pixels, mask) {
  let count = 0, sum = 0, sumSq = 0, chroma = 0, total = 0;
  for (let i = 0; i < mask.length; i += 2) {
    total++;
    if (mask[i] >= 0.15) continue;
    const r = pixels[i * 4], g = pixels[i * 4 + 1], b = pixels[i * 4 + 2];
    const light = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    sum += light; sumSq += light * light; chroma += Math.max(r, g, b) - Math.min(r, g, b); count++;
  }
  if (!count) return { fraction: 0 };
  const meanL = sum / count;
  return { fraction: count / total, meanL, stdL: Math.sqrt(Math.max(0, sumSq / count - meanL * meanL)), meanChroma: chroma / count };
}

async function analyse(bitmap) {
  const scale = Math.min(1, ANALYSIS_EDGE / Math.max(bitmap.width, bitmap.height));
  const width = Math.round(bitmap.width * scale), height = Math.round(bitmap.height * scale);
  const canvas = document.createElement('canvas'); canvas.width = width; canvas.height = height;
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  ctx.drawImage(bitmap, 0, 0, width, height);
  const { faces, person } = await loadModels();
  const faceResult = faces.detect(canvas);
  const found = faceResult.faceLandmarks || [];
  if (found.length !== 1) return { faceCount: found.length };
  const points = found[0].map(p => ({ x: p.x * width, y: p.y * height }));
  const shapes = Object.fromEntries((faceResult.faceBlendshapes?.[0]?.categories || []).map(c => [c.categoryName, c.score]));
  const segmentation = person.segment(canvas);
  const masks = segmentation.confidenceMasks || [];
  const mask = masks[masks.length - 1].getAsFloat32Array();
  const chinY = points[152].y;
  const top = hairTop(mask, width, points[234].x, points[454].x, chinY);
  const stats = backgroundStats(ctx.getImageData(0, 0, width, height).data, mask);
  masks.forEach(item => item.close?.());
  const toSource = value => value / scale;
  return {
    faceCount: 1, scale,
    chinY: toSource(chinY), foreheadY: toSource(points[10].y),
    hairTop: top === null ? null : toSource(top), hairCut: top !== null && top <= 1,
    centerX: toSource((points[234].x + points[454].x) / 2),
    pose: { leftEye: points[33], rightEye: points[263], nose: points[1],
      blinkLeft: shapes.eyeBlinkLeft, blinkRight: shapes.eyeBlinkRight, jawOpen: shapes.jawOpen },
    background: stats,
  };
}

function canvasBlob(canvas) {
  return new Promise((resolve, reject) => canvas.toBlob(blob => blob ? resolve(blob) : reject(new Error('The image could not be created.')), 'image/jpeg', 0.95));
}

async function jpeg300(canvas) {
  const bytes = setJpegDpi(new Uint8Array(await (await canvasBlob(canvas)).arrayBuffer()), 300);
  return new Blob([bytes], { type: 'image/jpeg' });
}

function previewWithGuides(photo, spec) {
  const canvas = document.createElement('canvas');
  canvas.width = photo.width; canvas.height = photo.height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(photo, 0, 0);
  const pxPerMm = photo.height / spec.photo_mm[1];
  const topMargin = (spec.photo_mm[1] - spec.target_head_mm) * spec.top_ratio;
  const chin = (topMargin + spec.target_head_mm) * pxPerMm;
  ctx.lineWidth = Math.max(1, photo.width / 300);
  ctx.setLineDash([8, 6]);
  ctx.strokeStyle = 'rgba(35,133,75,.9)';
  for (const headMm of spec.head_mm) {
    const y = chin - headMm * pxPerMm;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }
  ctx.strokeStyle = 'rgba(173,48,40,.9)';
  ctx.beginPath(); ctx.moveTo(0, chin); ctx.lineTo(canvas.width, chin); ctx.stroke();
  return canvas;
}

async function makePrint(bitmap, spec, found) {
  if (found.hairCut) throw new Error('The top of your head is cut off at the edge of the photo. Use a photo with space above your head.');
  const crownY = estimateCrown(found, spec.head_basis);
  const crop = computeCrop(spec, { chinY: found.chinY, crownY, centerX: found.centerX }, bitmap.width, bitmap.height);
  const checks = [];
  if (!crop.fits) {
    const sides = Object.entries(crop.missing).filter(([, value]) => value > 0.5).map(([side]) => side);
    throw new Error(`There is not enough photo around your head to make a ${spec.photo_label} photo (short on the ${sides.join(' and ')}). Take the photo from a little further away, with space above your head and your shoulders in view.`);
  }
  const [width, height] = spec.photo_px;
  const photo = document.createElement('canvas'); photo.width = width; photo.height = height;
  const pctx = photo.getContext('2d');
  pctx.imageSmoothingQuality = 'high';
  pctx.drawImage(bitmap, crop.sx, crop.sy, crop.sw, crop.sh, 0, 0, width, height);
  checks.push({ ok: true, text: `Cropped to ${spec.photo_label} with the head about ${crop.headMm} mm tall (allowed ${spec.head_label}). This uses an automatic estimate of the top of your head, so check the print with a ruler.` });
  checks.push(crop.upscale > 1.35
    ? { ok: false, text: 'Your face is small in this photo, so the print will be enlarged and may look soft. Move closer or use a higher-resolution photo.' }
    : { ok: true, text: 'The photo has enough resolution for a sharp 300 dpi print.' });
  if (spec.head_basis === 'skull' && Number.isFinite(found.hairTop) && found.hairTop < crop.sy) {
    checks.push({ ok: false, text: 'The top of your hair falls outside the photo. Make sure your whole head is visible before printing.' });
  }
  const sheet = document.createElement('canvas');
  [sheet.width, sheet.height] = spec.sheet.px;
  const sctx = sheet.getContext('2d');
  sctx.fillStyle = '#fff'; sctx.fillRect(0, 0, sheet.width, sheet.height);
  sctx.strokeStyle = '#b8b8b8'; sctx.lineWidth = 1;
  for (const [x, y] of sheetLayout(spec).positions) {
    sctx.drawImage(photo, x, y);
    if (spec.sheet.gap_px) sctx.strokeRect(x - 1.5, y - 1.5, width + 3, height + 3);
  }
  return { checks, preview: previewWithGuides(photo, spec), photoBlob: await jpeg300(photo), sheetBlob: await jpeg300(sheet) };
}

function onlineChecks(bitmap, spec, found) {
  const checks = [];
  const height = bitmap.height;
  const crownY = estimateCrown(found, 'hair');
  const headShare = (found.chinY - crownY) / height;
  checks.push(found.hairCut
    ? { ok: false, text: 'The top of your head touches the top edge. Leave space above your head.' }
    : { ok: true, text: 'Your whole head is in the photo.' });
  checks.push(height - found.chinY < height * 0.18 || headShare > 0.6
    ? { ok: false, text: 'The photo is too close-up. Include your shoulders and upper body; the passport service crops the photo itself.' }
    : { ok: true, text: 'Head and shoulders are in view, as the online service expects.' });
  checks.push(Math.abs(found.centerX - bitmap.width / 2) > bitmap.width * 0.15
    ? { ok: false, text: 'Your face is well off-centre. Stand in the middle of the frame.' }
    : { ok: true, text: 'Your face is near the centre of the frame.' });
  return checks;
}

form?.addEventListener('submit', async event => {
  event.preventDefault();
  clearOutput();
  const spec = JSON.parse(form.dataset.spec);
  const mode = form.querySelector('input[name="passport-mode"]:checked')?.value || 'print';
  const file = $('passport-file').files[0];
  if (!file) return setStatus('Choose a photo first.', true);
  if (file.size > 15 * 1024 * 1024) return setStatus('Choose a photo under 15 MB.', true);
  const button = form.querySelector('[type=submit]');
  button.disabled = true;
  let bitmap;
  try {
    const format = FORMATS[file.type] || (/\.(heic|heif)$/i.test(file.name) ? 'HEIC' : file.type || 'unknown');
    try {
      bitmap = await createImageBitmap(file, { imageOrientation: 'from-image' });
    } catch {
      throw new Error(format === 'HEIC' || format === 'HEIF'
        ? 'This browser cannot read HEIC photos. Export the photo as JPG, or open this page in Safari.'
        : 'This file could not be read as a photo. Use a JPG or PNG.');
    }
    if (bitmap.width * bitmap.height > 40_000_000) throw new Error('Choose a photo under 40 megapixels.');
    const checks = [];
    if (mode === 'online' && spec.online) {
      const issues = fileIssues(spec.online, { size: file.size, width: bitmap.width, height: bitmap.height, format });
      checks.push(...(issues.length ? issues.map(text => ({ ok: false, text })) : [{ ok: true, text: `File type, size and dimensions meet the ${spec.online.label.toLowerCase()} rules.` }]));
    }
    setStatus('Loading the face model… (first use downloads about 4 MB)');
    const found = await analyse(bitmap).catch(error => {
      if (/fetch|network|import|load/i.test(String(error))) throw new Error('The face model could not load. Check your connection and try again.');
      throw error;
    });
    if (found.faceCount === 0) throw new Error('No face was found. Use a clear, front-facing photo with your whole face visible.');
    if (found.faceCount > 1) throw new Error('More than one face was found. Use a photo of just you.');
    setStatus('Checking the photo…');
    const pose = poseIssues(found.pose);
    const background = backgroundIssues(found.background, spec.background_kind);
    let result = null;
    if (mode === 'online') checks.push(...onlineChecks(bitmap, spec, found));
    else result = await makePrint(bitmap, spec, found);
    if (result) checks.unshift(...result.checks);
    checks.push(...(pose.length ? pose.map(text => ({ ok: false, text })) : [{ ok: true, text: 'Eyes open, mouth closed and facing the camera.' }]));
    checks.push(...(background.length ? background.map(text => ({ ok: false, text })) : [{ ok: true, text: 'The background looks plain and light.' }]));
    renderChecks(checks);
    const preview = $('passport-preview');
    if (result) {
      const previewUrl = URL.createObjectURL(await canvasBlob(result.preview));
      const photoUrl = URL.createObjectURL(result.photoBlob);
      const sheetUrl = URL.createObjectURL(result.sheetBlob);
      urls.push(previewUrl, photoUrl, sheetUrl);
      preview.src = previewUrl; preview.hidden = false;
      $('passport-photo-download').href = photoUrl;
      $('passport-sheet-download').href = sheetUrl;
      $('passport-downloads').hidden = false;
    } else {
      preview.hidden = true;
    }
    $('passport-output').hidden = false;
    const warnings = checks.filter(item => !item.ok).length;
    setStatus(mode === 'online'
      ? (warnings ? `${warnings} issue${warnings === 1 ? '' : 's'} to fix before you upload.` : 'No problems found. Upload the original file you selected.')
      : (warnings ? `Photo ready, with ${warnings} thing${warnings === 1 ? '' : 's'} to check.` : 'Photo ready. Check the preview, then download.'));
  } catch (error) {
    setStatus(error.message || 'The photo could not be processed.', true);
  } finally {
    bitmap?.close?.();
    button.disabled = false;
  }
});

form?.querySelector('#passport-file')?.addEventListener('change', clearOutput);
window.addEventListener('pagehide', clearOutput);
