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

if (typeof document !== 'undefined') {
  const form = document.getElementById('size-estimator');
  const result = document.getElementById('size-estimate-result');
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const minutes = Number(data.get('minutes'));
    const seconds = Number(data.get('seconds'));
    const videoKbps = Number(data.get('videoKbps'));
    const audioKbps = Number(data.get('audioKbps'));
    if (!Number.isInteger(minutes) || minutes < 0 || !Number.isInteger(seconds) || seconds < 0 || seconds > 59 || !Number.isFinite(videoKbps) || !Number.isFinite(audioKbps)) {
      result.textContent = 'Enter a valid runtime and bitrates in kbps.';
      result.hidden = false;
      return;
    }
    try {
      const { mb, mib, overLimit } = formatEstimate(estimateBytes(minutes * 60 + seconds, videoKbps, audioKbps));
      result.textContent = `Estimated size: ${mb} MB (${mib} MiB). ${overLimit ? 'This estimate exceeds SaveFromNet’s 512 MiB processing limit. Try a lower bitrate or shorter file.' : 'The actual finished file may differ.'}`;
    } catch (error) {
      result.textContent = error.message;
    }
    result.hidden = false;
  });
}
