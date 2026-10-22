"""Pages strengthened from Search Console query data (October 2026)."""
import json
import os
import re
import tempfile
import unittest
from html import unescape
from pathlib import Path

_tmp = tempfile.TemporaryDirectory()
os.environ.setdefault("DB_PATH", str(Path(_tmp.name) / "test.db"))
os.environ.setdefault("DOWNLOAD_DIR", str(Path(_tmp.name) / "downloads"))

from app import _filter_formats, app  # noqa: E402
from tools import BY_SLUG  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def faq_questions(page):
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        data = json.loads(block)
        if data.get("@type") == "FAQPage":
            return {item["name"]: item["acceptedAnswer"]["text"] for item in data["mainEntity"]}
    return {}


class Y2MateAlternativeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_page_is_a_working_downloader_that_states_it_is_independent(self):
        response = self.client.get("/y2mate-alternative")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("<title>Y2Mate Alternative – YouTube to MP3 &amp; MP4 Downloader | SaveFromNet</title>", page)
        self.assertIn('<link rel="canonical" href="https://savefromnet.fun/y2mate-alternative">', page)
        self.assertIn('<h1 id="download-heading">Y2Mate Alternative: YouTube to MP3 &amp; MP4</h1>', page)
        self.assertIn('id="download-form"', page)
        self.assertIn('data-tool="y2mate-alternative"', page)
        faq = faq_questions(page)
        self.assertIn("not affiliated with Y2Mate", faq["Is SaveFromNet the same as Y2Mate?"])
        self.assertIn("not affiliated with Y2Mate", unescape(page))
        for heading in ("A Y2Mate alternative that shows real formats first", "YouTube to MP3 and MP4 in one place",
                        "What to check in any YouTube downloader"):
            self.assertIn(f"<h2>{heading}</h2>", page)

    def test_it_offers_both_video_and_mp3_from_the_real_analysis(self):
        media = {"platform": "youtube", "type": "video", "formats": [
            {"id": "v0", "type": "video", "extension": "mp4", "quality": "720p"},
            {"id": "a-mp3", "type": "audio", "extension": "mp3", "quality": "Converted MP3"},
        ]}
        filtered = _filter_formats(BY_SLUG["y2mate-alternative"], dict(media, formats=list(media["formats"])))
        self.assertEqual([item["extension"] for item in filtered["formats"]], ["mp4", "mp3"])
        short = dict(media, type="short", formats=list(media["formats"]))
        self.assertEqual(len(_filter_formats(BY_SLUG["y2mate-alternative"], short)["formats"]), 2)

    def test_it_is_discoverable_and_old_y2mate_urls_point_to_it(self):
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        self.assertEqual(sitemap.count("<loc>https://savefromnet.fun/y2mate-alternative</loc>"), 1)
        self.assertIn('href="/y2mate-alternative"', self.client.get("/tools").get_data(as_text=True))
        self.assertIn('href="/y2mate-alternative"', self.client.get("/youtube-downloader").get_data(as_text=True))
        rules = [line.split() for line in (ROOT / "_redirects").read_text(encoding="utf-8").splitlines()
                 if line and not line.startswith("#")]
        self.assertNotIn("/y2mate-alternative", [source for source, _, _ in rules])
        self.assertIn(["/compare/y2mate", "/y2mate-alternative", "301"], rules)


class SnippetTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_youtube_video_downloader_targets_its_main_query(self):
        page = self.client.get("/youtube-video-downloader").get_data(as_text=True)
        self.assertIn("<title>YouTube Video Downloader – Free MP4 in HD | SaveFromNet</title>", page)
        self.assertIn("<h2>How to choose a YouTube video downloader</h2>", page)
        description = re.search(r'<meta name="description" content="(.*?)">', page).group(1)
        self.assertLessEqual(len(unescape(description)), 160)

    def test_facebook_snippet_names_videos_and_reels(self):
        page = self.client.get("/facebook-video-downloader").get_data(as_text=True)
        self.assertIn("<title>Facebook Video Downloader – Save FB Videos &amp; Reels | SaveFromNet</title>", page)
        self.assertIn("choose HD or SD when Facebook offers both", page)


if __name__ == "__main__":
    unittest.main()
