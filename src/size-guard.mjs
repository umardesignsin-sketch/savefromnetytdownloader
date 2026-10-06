const MAX_BYTES = 512 * 1024 * 1024;

// Older container images can report only the audio stream's size for a merged
// video. Reject clearly oversized options and label any corrected size as an
// estimate rather than presenting that partial number as the finished file.
export function guardAnalysis(result) {
  if (!Array.isArray(result?.formats)) return result;
  const duration = Number(result.duration);
  const sharedSizes = new Map();
  for (const format of result.formats) {
    if (format.type !== "video" || !Number(format.filesize)) continue;
    const key = `${format.extension}:${format.filesize}`;
    if (!sharedSizes.has(key)) sharedSizes.set(key, new Set());
    sharedSizes.get(key).add(format.quality);
  }
  return {
    ...result,
    formats: result.formats.flatMap((format) => {
      if (format.type !== "video") return [format];
      const reported = Number(format.filesize);
      const bitrate = Number(format.bitrate);
      const rough = Number.isFinite(duration) && duration > 0 && Number.isFinite(bitrate) && bitrate > 0
        ? Math.round(bitrate * 125 * duration) : null;
      const repeatedAcrossQualities = sharedSizes.get(`${format.extension}:${format.filesize}`)?.size > 1;
      if (reported > MAX_BYTES) return [];
      if (repeatedAcrossQualities || (rough && (!reported || rough > reported * 8))) {
        if (rough > MAX_BYTES * 1.25) return [];
        if (!rough || !reported) return [{ ...format, filesize: null }];
        const estimate = rough + reported;
        if (estimate > MAX_BYTES) return [];
        return [{ ...format, filesize: estimate, filesize_estimated: true }];
      }
      return [format];
    }),
  };
}
