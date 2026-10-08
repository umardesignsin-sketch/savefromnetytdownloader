export function estimateBytes(durationSeconds, videoKbps, audioKbps = 0) {
  const numbers = [durationSeconds, videoKbps, audioKbps];
  if (numbers.some((value) => !Number.isFinite(value)) || durationSeconds <= 0 || videoKbps <= 0 || audioKbps < 0) {
    throw new RangeError('Enter a positive runtime and video bitrate. Audio bitrate can be zero.');
  }
  return durationSeconds * (videoKbps + audioKbps) * 1000 / 8;
}

export function formatEstimate(bytes) {
  return {
    mb: (bytes / 1_000_000).toLocaleString('en-US', { maximumFractionDigits: 1 }),
    mib: (bytes / (1024 * 1024)).toLocaleString('en-US', { maximumFractionDigits: 1 }),
    overLimit: bytes > 512 * 1024 * 1024,
  };
}

export function parseEstimateQuery(search) {
  const params = new URLSearchParams(search);
  const names = ['minutes', 'seconds', 'videoKbps', 'audioKbps'];
  if (!names.every((name) => params.has(name))) return null;
  const values = Object.fromEntries(names.map((name) => [name, Number(params.get(name))]));
  const { minutes, seconds, videoKbps, audioKbps } = values;
  if (!Number.isInteger(minutes) || minutes < 0 || minutes > 10000 ||
      !Number.isInteger(seconds) || seconds < 0 || seconds > 59 ||
      minutes * 60 + seconds === 0 ||
      !Number.isFinite(videoKbps) || videoKbps <= 0 || videoKbps > 1000000 ||
      !Number.isFinite(audioKbps) || audioKbps < 0 || audioKbps > 100000) return null;
  return values;
}

export function estimateUrl(baseUrl, values) {
  const url = new URL(baseUrl);
  url.search = new URLSearchParams(Object.entries(values).map(([name, value]) => [name, String(value)])).toString();
  url.hash = '';
  return url.toString();
}

if (typeof document !== 'undefined') {
  const form = document.getElementById('size-estimator');
  const result = document.getElementById('size-estimate-result');
  const share = document.getElementById('size-calculator-share');
  const shareLink = document.getElementById('size-share-link');
  const shareButton = document.getElementById('size-share-copy');
  const shareStatus = document.getElementById('size-share-status');
  const calculate = () => {
    const data = new FormData(form);
    const values = Object.fromEntries(['minutes', 'seconds', 'videoKbps', 'audioKbps']
      .map((name) => [name, Number(data.get(name))]));
    if (!parseEstimateQuery(new URLSearchParams(values).toString())) {
      result.textContent = 'Enter a valid runtime and bitrates in kbps.';
      result.hidden = false;
      share.hidden = true;
      return;
    }
    try {
      const { minutes, seconds, videoKbps, audioKbps } = values;
      const { mb, mib, overLimit } = formatEstimate(estimateBytes(minutes * 60 + seconds, videoKbps, audioKbps));
      result.textContent = `Estimated size: ${mb} MB (${mib} MiB). ${overLimit ? 'This estimate exceeds SaveFromNet’s 512 MiB processing limit. Try a lower bitrate or shorter file.' : 'The actual finished file may differ.'}`;
      shareLink.value = estimateUrl(window.location.origin + window.location.pathname, values);
      share.hidden = false;
      shareStatus.textContent = '';
    } catch (error) {
      result.textContent = error.message;
      share.hidden = true;
    }
    result.hidden = false;
  };
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    calculate();
  });
  const sharedValues = parseEstimateQuery(window.location.search);
  if (form && sharedValues) {
    for (const [name, value] of Object.entries(sharedValues)) form.elements.namedItem(name).value = value;
    calculate();
  }
  shareButton?.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(shareLink.value);
      shareStatus.textContent = 'Estimate link copied.';
    } catch {
      shareLink.focus();
      shareLink.select();
      shareStatus.textContent = 'Copy the selected link to share this estimate.';
    }
  });
}
