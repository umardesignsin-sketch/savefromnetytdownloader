import assert from "node:assert/strict";
import test from "node:test";
import { guardAnalysis } from "../src/size-guard.mjs";

test("rejects the reported 23.9 MB 2160p option for a 25-minute video", () => {
  const result = guardAnalysis({ duration: 1549, formats: [
    { id: "v0", type: "video", quality: "2160p", bitrate: 19027, filesize: 25_077_688 },
    { id: "v1", type: "video", quality: "720p", bitrate: 2000, filesize: 25_077_688 },
    { id: "a-source", type: "audio", filesize: 25_077_688 },
  ] });
  assert.deepEqual(result.formats.map((item) => item.id), ["v1", "a-source"]);
  assert.equal(result.formats[0].filesize_estimated, true);
  assert.ok(result.formats[0].filesize > 25_077_688);
});

test("keeps a consistent reported total and leaves unknown size unknown", () => {
  const result = guardAnalysis({ duration: 100, formats: [
    { id: "v0", type: "video", bitrate: 1000, filesize: 12_000_000 },
    { id: "v1", type: "video", bitrate: null, filesize: null },
  ] });
  assert.equal(result.formats[0].filesize, 12_000_000);
  assert.equal(result.formats[1].filesize, null);
});

test("does not reuse one audio size for different video resolutions", () => {
  const result = guardAnalysis({ duration: 1549, formats: [
    { id: "v360", type: "video", extension: "mp4", quality: "360p", bitrate: 803, filesize: 25_078_552 },
    { id: "v240", type: "video", extension: "mp4", quality: "240p", bitrate: 317, filesize: 25_078_552 },
  ] });
  assert.ok(result.formats.every((item) => item.filesize > 25_078_552));
  assert.ok(result.formats.every((item) => item.filesize_estimated));
});
