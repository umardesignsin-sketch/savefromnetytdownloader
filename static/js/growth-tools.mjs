import { evaluateExpression, formatResult } from './calculator-core.mjs';

const $ = id => document.getElementById(id);
const errorMessage = error => error instanceof Error ? error.message : 'The request failed. Please try again.';

function bindCalculator() {
  const input = $('calculator-expression');
  if (!input) return;
  const result = $('calculator-result');
  const calculate = () => {
    try { result.textContent = formatResult(evaluateExpression(input.value)); result.classList.remove('error'); }
    catch (error) { result.textContent = errorMessage(error); result.classList.add('error'); }
  };
  input.addEventListener('keydown', event => { if (event.key === 'Enter') { event.preventDefault(); calculate(); } });
  document.querySelectorAll('.calculator-keys button').forEach(button => button.addEventListener('click', () => {
    const key = button.dataset.key;
    if (key === 'clear') { input.value = ''; result.textContent = 'Result will appear here.'; result.classList.remove('error'); }
    else if (key === 'equals') calculate();
    else { input.setRangeText(key, input.selectionStart, input.selectionEnd, 'end'); input.focus(); }
  }));
}

async function postJson(path, body) {
  const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || 'The service is unavailable. Please try again.');
  return data;
}

function bindTranslator() {
  const form = $('translator-form');
  if (!form) return;
  const source = $('translation-source');
  const target = $('translation-target');
  if (form.dataset.preset === 'en-es') { source.value = 'en'; target.value = 'es'; }
  else { source.value = 'en'; target.value = 'fr'; }
  $('translation-swap').addEventListener('click', () => { [source.value, target.value] = [target.value, source.value]; });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const status = $('translation-status');
    const output = $('translation-output');
    status.classList.remove('error'); output.hidden = true;
    const text = $('translation-text').value.trim();
    if (!text || text.length > 500 || source.value === target.value) { status.textContent = 'Enter up to 500 characters and choose two different languages.'; status.classList.add('error'); return; }
    const button = form.querySelector('[type=submit]'); button.disabled = true; status.textContent = 'Translating…';
    try {
      const data = await postJson('/api/translate', { text, source: source.value, target: target.value });
      $('translation-result').textContent = data.translation;
      output.hidden = false; status.textContent = 'Translation ready.';
    } catch (error) { status.textContent = errorMessage(error); status.classList.add('error'); }
    finally { button.disabled = false; }
  });
  $('translation-copy').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText($('translation-result').textContent); $('translation-status').textContent = 'Copied to clipboard.'; }
    catch { $('translation-status').textContent = 'Select the translation to copy it.'; }
  });
}

function bindWeather() {
  const form = $('weather-form');
  if (!form) return;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const status = $('weather-status'); const output = $('weather-output');
    status.classList.remove('error'); output.hidden = true;
    const zip = $('weather-zip').value.trim();
    if (!/^\d{5}$/.test(zip)) { status.textContent = 'Enter a five-digit US ZIP code.'; status.classList.add('error'); return; }
    const button = form.querySelector('[type=submit]'); button.disabled = true; status.textContent = 'Checking the latest forecast…';
    try {
      const data = await postJson('/api/weather/us', { zip });
      $('weather-location').textContent = `${data.location} forecast`;
      $('weather-updated').textContent = data.updated ? `Updated ${new Date(data.updated).toLocaleString()}` : 'Latest available NWS forecast';
      const periods = $('weather-periods'); periods.replaceChildren();
      for (const period of data.periods) {
        const card = document.createElement('article'); card.className = 'weather-period';
        const heading = document.createElement('h3'); heading.textContent = period.name;
        const temp = document.createElement('p'); temp.textContent = `${period.temperature}°${period.temperature_unit} · ${period.short_forecast}`;
        const wind = document.createElement('p'); wind.textContent = `Wind: ${period.wind_speed} ${period.wind_direction}`;
        const details = document.createElement('p'); details.textContent = period.detailed_forecast;
        card.append(heading, temp, wind, details); periods.append(card);
      }
      $('weather-source').href = data.source_url;
      output.hidden = false; status.textContent = 'Forecast ready.';
    } catch (error) { status.textContent = errorMessage(error); status.classList.add('error'); }
    finally { button.disabled = false; }
  });
}

let backgroundUrl = null;
let imageSegmenterPromise = null;
async function getSegmenter() {
  if (!imageSegmenterPromise) imageSegmenterPromise = (async () => {
    const { FilesetResolver, ImageSegmenter } = await import('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21/vision_bundle.mjs');
    const vision = await FilesetResolver.forVisionTasks('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21/wasm');
    return ImageSegmenter.createFromOptions(vision, {
      baseOptions: { modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/1/selfie_segmenter.tflite' },
      runningMode: 'IMAGE', outputConfidenceMasks: true, outputCategoryMask: false,
    });
  })().catch(error => { imageSegmenterPromise = null; throw error; });
  return imageSegmenterPromise;
}

function bindBackground() {
  const form = $('background-form');
  if (!form) return;
  const status = $('background-status');
  const output = $('background-output');
  const clear = () => { if (backgroundUrl) URL.revokeObjectURL(backgroundUrl); backgroundUrl = null; output.hidden = true; };
  $('background-file').addEventListener('change', clear);
  window.addEventListener('pagehide', clear);
  form.addEventListener('submit', async event => {
    event.preventDefault(); clear(); status.classList.remove('error');
    const file = $('background-file').files[0];
    if (!file || !['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > 8 * 1024 * 1024) { status.textContent = 'Choose a JPG, PNG or WebP photo under 8 MB.'; status.classList.add('error'); return; }
    const button = form.querySelector('[type=submit]'); button.disabled = true;
    let bitmap;
    try {
      status.textContent = 'Loading the portrait model…';
      const segmenter = await getSegmenter().catch(() => { throw new Error('The portrait model could not load. Check your connection and try again.'); });
      bitmap = await createImageBitmap(file);
      if (bitmap.width * bitmap.height > 20_000_000 || bitmap.width > 8192 || bitmap.height > 8192) throw new Error('Choose a photo under 20 megapixels and 8192 pixels per side.');
      const scale = Math.min(1, 1600 / Math.max(bitmap.width, bitmap.height));
      const width = Math.max(1, Math.round(bitmap.width * scale));
      const height = Math.max(1, Math.round(bitmap.height * scale));
      const canvas = document.createElement('canvas'); canvas.width = width; canvas.height = height;
      const ctx = canvas.getContext('2d', { willReadFrequently: true }); ctx.drawImage(bitmap, 0, 0, width, height);
      status.textContent = 'Removing the background…';
      const segmentation = segmenter.segment(canvas);
      // selfie_segmenter returns one mask labelled "selfie" (person confidence).
      // Multi-class models put background first, so use the last mask there.
      const masks = segmentation.confidenceMasks || [];
      const mask = masks[masks.length - 1];
      if (!mask) throw new Error('No person could be isolated from this photo.');
      const confidence = mask.getAsFloat32Array();
      if (!confidence.some(value => value > 0.35)) throw new Error('No person could be isolated from this photo.');
      const maskCanvas = document.createElement('canvas'); maskCanvas.width = mask.width; maskCanvas.height = mask.height;
      const maskContext = maskCanvas.getContext('2d');
      const pixels = maskContext.createImageData(mask.width, mask.height);
      for (let i = 0; i < confidence.length; i++) {
        const alpha = Math.max(0, Math.min(1, (confidence[i] - 0.18) / 0.64));
        const index = i * 4; pixels.data[index] = 255; pixels.data[index + 1] = 255; pixels.data[index + 2] = 255; pixels.data[index + 3] = Math.round(alpha * 255);
      }
      maskContext.putImageData(pixels, 0, 0);
      ctx.globalCompositeOperation = 'destination-in'; ctx.drawImage(maskCanvas, 0, 0, width, height);
      segmentation.confidenceMasks?.forEach(item => item.close?.());
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
      if (!blob) throw new Error('The PNG could not be created. Try another photo.');
      backgroundUrl = URL.createObjectURL(blob);
      $('background-preview').src = backgroundUrl; $('background-download').href = backgroundUrl;
      output.hidden = false; status.textContent = 'Cutout ready. Check the edges before saving.';
    } catch (error) { status.textContent = errorMessage(error); status.classList.add('error'); }
    finally { bitmap?.close?.(); button.disabled = false; }
  });
}

bindCalculator(); bindTranslator(); bindWeather(); bindBackground();
