import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image


_temp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = str(Path(_temp.name) / "utility-test.db")
os.environ["DOWNLOAD_DIR"] = str(Path(_temp.name) / "downloads")

from app import app  # noqa: E402
from utility_pages import UTILITY_TOOLS  # noqa: E402


class MockThumbnailResponse:
    status_code = 200
    headers = {"Content-Type": "image/jpeg"}

    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def iter_content(self, _size):
        yield self.data


class UtilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.video = Path(_temp.name) / "sample.mp4"
        command = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "lavfi",
                   "-i", "color=c=red:s=160x90:r=10:d=2", "-f", "lavfi",
                   "-i", "sine=frequency=440:duration=2", "-c:v", "libx264", "-c:a", "aac",
                   "-shortest", str(cls.video)]
        subprocess.run(command, check=True, capture_output=True, timeout=20)
        cls.audio = Path(_temp.name) / "sample.wav"
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", str(cls.video),
                        "-vn", str(cls.audio)], check=True, capture_output=True, timeout=20)

    def post_media(self, slug, path, **fields):
        return app.test_client().post("/api/media/process", data={
            "tool": slug, "media": (io.BytesIO(path.read_bytes()), path.name), **fields,
        })

    def test_pages_have_working_forms_and_directory_links(self):
        client = app.test_client()
        directory = client.get("/tools").get_data(as_text=True)
        sitemap = client.get("/sitemap.xml").get_data(as_text=True)
        for tool in UTILITY_TOOLS:
            with self.subTest(tool=tool.slug):
                page = client.get("/" + tool.slug)
                self.assertEqual(page.status_code, 200)
                html = page.get_data(as_text=True)
                self.assertIn('id="utility-form"', html)
                self.assertIn('href="/' + tool.slug + '"', directory)
                self.assertIn("https://savefromnet.fun/" + tool.slug, sitemap)

    def test_real_ffmpeg_outputs(self):
        cases = (
            ("video-to-gif", self.video, {"start": "0", "end": "1"}, b"GIF8"),
            ("mp4-to-mp3", self.video, {}, b"ID3"),
            ("video-trimmer", self.video, {"start": "0.2", "end": "1.3"}, b"ftyp"),
            ("audio-cutter", self.audio, {"start": "0.1", "end": "1.1"}, b"ID3"),
        )
        for slug, source, fields, marker in cases:
            with self.subTest(tool=slug):
                response = self.post_media(slug, source, **fields)
                self.assertEqual(response.status_code, 200, response.data[:200])
                self.assertIn(marker, response.data[:24])
                self.assertEqual(int(response.headers["X-SFN-Output-Bytes"]), len(response.data))

    def test_invalid_media_and_times_are_rejected(self):
        bad = app.test_client().post("/api/media/process", data={
            "tool": "mp4-to-mp3", "media": (io.BytesIO(b"not video"), "fake.mp4"),
        })
        self.assertEqual(bad.status_code, 422)
        times = self.post_media("video-trimmer", self.video, start="1.5", end="0.5")
        self.assertEqual(times.status_code, 422)

    def test_thumbnail_only_fetches_validated_youtube_image(self):
        image = io.BytesIO()
        Image.new("RGB", (480, 360), "blue").save(image, format="JPEG")
        with patch("youtube_thumbnails.requests.get", return_value=MockThumbnailResponse(image.getvalue())) as get:
            response = app.test_client().post("/api/thumbnail", json={"url": "https://youtu.be/dQw4w9WgXcQ"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Image.open(io.BytesIO(response.data)).size, (480, 360))
        self.assertEqual(get.call_args.args[0], "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg")
        with patch("youtube_thumbnails.requests.get") as get:
            invalid = app.test_client().post("/api/thumbnail", json={"url": "http://127.0.0.1/internal"})
        self.assertEqual(invalid.status_code, 422)
        get.assert_not_called()


if __name__ == "__main__":
    unittest.main()
