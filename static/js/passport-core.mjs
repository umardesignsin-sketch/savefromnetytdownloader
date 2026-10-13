// Pure geometry and checks for the passport photo tools. No DOM or network access,
// so the rules can be unit-tested in Node.

// The face mesh's forehead point (landmark 10) sits near the hairline. The top of
// the skull is estimated by extending the chin-to-forehead distance by this factor.
export const SKULL_FACTOR = 1.25;

export function estimateCrown({ chinY, foreheadY, hairTop }, basis) {
  const skull = chinY - (chinY - foreheadY) * SKULL_FACTOR;
  const hair = Number.isFinite(hairTop) ? hairTop : null;
  if (basis === 'hair') return hair ?? skull;
  // Hair can sit above the skull, never below it; trust the segmented top only when it is lower.
  return hair !== null && hair > skull ? hair : skull;
}

export function computeCrop(spec, { chinY, crownY, centerX }, imageWidth, imageHeight) {
  const headPx = chinY - crownY;
  if (!(headPx > 0)) return { fits: false, reason: 'no-head' };
  const [widthMm, heightMm] = spec.photo_mm;
  const pxPerMm = headPx / spec.target_head_mm;
  const sw = widthMm * pxPerMm;
  const sh = heightMm * pxPerMm;
  const topMarginMm = (heightMm - spec.target_head_mm) * spec.top_ratio;
  const sx = centerX - sw / 2;
  const sy = crownY - topMarginMm * pxPerMm;
  const tolerance = 0.5;
  const missing = {
    left: Math.max(0, -sx), top: Math.max(0, -sy),
    right: Math.max(0, sx + sw - imageWidth), bottom: Math.max(0, sy + sh - imageHeight),
  };
  const fits = Object.values(missing).every(value => value <= tolerance);
  const outputHeadPx = spec.target_head_mm * spec.photo_px[1] / heightMm;
  return { fits, sx, sy, sw, sh, pxPerMm, headMm: spec.target_head_mm, topMarginMm,
    sourceHeadPx: headPx, outputHeadPx, upscale: outputHeadPx / headPx, missing };
}

export function sheetLayout(spec) {
  const [sheetWidth, sheetHeight] = spec.sheet.px;
  const [photoWidth, photoHeight] = spec.photo_px;
  const gap = spec.sheet.gap_px;
  const cols = Math.floor((sheetWidth - gap) / (photoWidth + gap));
  const rows = Math.floor((sheetHeight - gap) / (photoHeight + gap));
  const usedWidth = cols * photoWidth + (cols - 1) * gap;
  const usedHeight = rows * photoHeight + (rows - 1) * gap;
  const left = Math.round((sheetWidth - usedWidth) / 2);
  const top = Math.round((sheetHeight - usedHeight) / 2);
  const positions = [];
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) positions.push([left + col * (photoWidth + gap), top + row * (photoHeight + gap)]);
  }
  return { cols, rows, positions };
}

// stats: meanL (0-255 luminance), stdL, meanChroma (max-min RGB), fraction of pixels that are background.
export function backgroundIssues(stats, kind) {
  if (!stats || stats.fraction < 0.03) return ['Too little background is visible to check it.'];
  const issues = [];
  if (stats.meanL < 170) issues.push('The background looks too dark. Use a plain light wall and even light.');
  if (stats.stdL > 30) issues.push('The background does not look plain. Avoid patterns, objects and shadows behind you.');
  if (kind === 'white' && stats.meanL >= 170 && (stats.meanL < 200 || stats.meanChroma > 22)) {
    issues.push('The background should be white or off-white. It looks grey or coloured.');
  }
  return issues;
}

export function fileIssues(online, file) {
  const issues = [];
  const kb = file.size / 1024;
  if (kb < online.min_kb) issues.push(`The file is ${kb.toFixed(0)} KB. The minimum is ${online.min_kb} KB, so use the original photo rather than a compressed copy.`);
  if (kb > online.max_kb) issues.push(`The file is ${(kb / 1024).toFixed(1)} MB. The maximum is ${online.max_kb / 1024} MB.`);
  if (online.min_px && Number.isFinite(file.width)) {
    const [minWidth, minHeight] = online.min_px;
    if (file.width < minWidth || file.height < minHeight) issues.push(`The photo is ${file.width} × ${file.height} pixels. It must be at least ${minWidth} × ${minHeight}.`);
  }
  if (online.formats && file.format && !online.formats.includes(file.format)) {
    issues.push(`${file.format} files are not listed as accepted. Accepted: ${online.formats.join(', ')}.`);
  }
  return issues;
}

export function poseIssues({ leftEye, rightEye, nose, blinkLeft = 0, blinkRight = 0, jawOpen = 0 }) {
  const issues = [];
  const roll = Math.atan2(rightEye.y - leftEye.y, rightEye.x - leftEye.x) * 180 / Math.PI;
  if (Math.abs(roll) > 4) issues.push(`Your head is tilted by about ${Math.abs(roll).toFixed(0)}°. Keep it level.`);
  const eyeSpan = Math.hypot(rightEye.x - leftEye.x, rightEye.y - leftEye.y);
  const midX = (leftEye.x + rightEye.x) / 2;
  if (eyeSpan > 0 && Math.abs(nose.x - midX) / eyeSpan > 0.12) issues.push('Your face seems turned to one side. Face the camera directly.');
  if (blinkLeft > 0.5 || blinkRight > 0.5) issues.push('Your eyes look closed. Keep both eyes open.');
  if (jawOpen > 0.25) issues.push('Your mouth looks open. Keep it closed with a neutral expression.');
  return issues;
}

// Mark a canvas JPEG as 300 dpi so printers place it at its true physical size.
export function setJpegDpi(bytes, dpi) {
  const isJfif = bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff && bytes[3] === 0xe0 &&
    bytes[6] === 0x4a && bytes[7] === 0x46 && bytes[8] === 0x49 && bytes[9] === 0x46 && bytes[10] === 0;
  if (!isJfif) return bytes;
  bytes[13] = 1;
  bytes[14] = dpi >> 8; bytes[15] = dpi & 255;
  bytes[16] = dpi >> 8; bytes[17] = dpi & 255;
  return bytes;
}
