"""Security, route, and real-format contract checks without hitting source sites."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = str(Path(_tmp.name) / "test.db")
os.environ["DOWNLOAD_DIR"] = str(Path(_tmp.name) / "downloads")

from app import _signed_link, app  # noqa: E402
import db  # noqa: E402
from downloader import file_path  # noqa: E402
from extractors.detect import DetectError, detect_url  # noqa: E402
from extractors.service import _yt_formats  # noqa: E402
from tools import TOOLS  # noqa: E402


class DetectorTests(unittest.TestCase):
    def test_recognizes_every_platform(self):
        cases = {
            "youtube": "https://youtu.be/aqz-KE-bpKQ",
            "instagram": "https://www.instagram.com/p/AbCdEf12/",
            "tiktok": "https://www.tiktok.com/@owner/video/1234567890",
            "facebook": "https://www.facebook.com/watch/?v=1234567890",
            "pinterest": "https://www.pinterest.com/pin/809522101770089198/",
            "reddit": "https://www.reddit.com/r/videos/comments/abc123/title/",
            "threads": "https://www.threads.com/@owner/post/AbCdEf12",
            "dailymotion": "https://www.dailymotion.com/video/x9yfz8u",
        }
        for platform, url in cases.items():
            with self.subTest(platform=platform):
                self.assertEqual(detect_url(url).platform, platform)

    def test_rejects_host_tricks_and_private_urls(self):
        bad = ["http://127.0.0.1/", "http://10.0.0.1/", "https://youtube.com.evil.test/watch?v=aqz-KE-bpKQ",
               "https://evil.test@youtube.com:444/watch?v=aqz-KE-bpKQ",
               "file:///etc/passwd", "https://www.youtube.com/playlist?list=abc",
               "https://www.instagram.com/../", "https://www.threads.com/@../post/abc123",
               "https://www.tiktok.com/@../../video/123", "https://www.reddit.com/r/../comments/abc123/"]
        for url in bad:
            with self.subTest(url=url), self.assertRaises(DetectError):
                detect_url(url)

    def test_normalization_drops_tracking_parameters(self):
        found = detect_url("https://www.youtube.com/watch?v=aqz-KE-bpKQ&utm_source=test")
        self.assertEqual(found.normalized_url, "https://www.youtube.com/watch?v=aqz-KE-bpKQ")


class FormatTests(unittest.TestCase):
    def test_only_returns_real_heights_and_audio(self):
        info = {"formats": [
            {"format_id": "v720", "ext": "mp4", "vcodec": "h264", "acodec": "none", "height": 720, "width": 1280},
            {"format_id": "a1", "ext": "m4a", "vcodec": "none", "acodec": "aac", "abr": 128},
            {"format_id": "v480", "ext": "mp4", "vcodec": "h264", "acodec": "aac", "height": 480, "width": 854},
        ]}
        found = _yt_formats(info)
        self.assertEqual({f["quality"] for f in found if f["type"] == "video"}, {"720p", "480p"})
        self.assertTrue(any(f["extension"] == "mp3" for f in found))
        self.assertEqual(next(f for f in found if f["quality"] == "720p")["_spec"]["selector"], "v720+a1")

    def test_no_audio_does_not_offer_conversion_or_video_only_file(self):
        found = _yt_formats({"formats": [{"format_id": "v", "ext": "mp4", "vcodec": "h264",
                                           "acodec": "none", "height": 1080}]})
        self.assertEqual(found, [])


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_all_tool_routes_have_metadata_and_schema(self):
        self.assertEqual(len(TOOLS), 25)
        for tool in TOOLS:
            with self.subTest(slug=tool.slug):
                response = self.client.get(tool.path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{tool.path}">', html)
                self.assertIn(f'<h1>{tool.name}</h1>', html)
                schemas = [json.loads(block.split('</script>')[0]) for block in html.split('<script type="application/ld+json">')[1:]]
                self.assertEqual({s["@type"] for s in schemas}, {"WebApplication", "FAQPage", "BreadcrumbList"})
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        self.assertEqual(sitemap.count("<url>"), 26)

    def test_invalid_url_and_cross_browser_signed_file_denial(self):
        response = self.client.post("/api/analyze", json={"url": "http://127.0.0.1/"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["code"], "invalid_url")
        owner = "x" * 43
        self.client.set_cookie("client_id", owner)
        link = _signed_link("a" * 32, owner)
        outsider = app.test_client().get(link)
        self.assertEqual(outsider.status_code, 403)
        self.assertEqual(self.client.get(link.replace("sig=", "sig=0")).status_code, 403)

    def test_file_path_refuses_traversal(self):
        self.assertIsNone(file_path("a" * 32, "../../outside.txt"))

    def test_expired_file_record_is_cleared(self):
        job_id = "b" * 32
        db.insert_job(job_id, "https://www.youtube.com/watch?v=aqz-KE-bpKQ", "MP3", "x" * 43)
        db.finish_job(job_id, "done", filename="test.mp3", filesize=123)
        with db.get_db() as conn:
            conn.execute("UPDATE downloads SET finished_at = datetime('now', '-2 hours') WHERE job_id = ?", (job_id,))
        self.assertIn(job_id, db.expired_files())
        self.assertIsNone(db.get_job(job_id, "x" * 43)["filename"])


if __name__ == "__main__":
    try:
        unittest.main()
    finally:
        _tmp.cleanup()
