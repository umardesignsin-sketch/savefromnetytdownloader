"""Google Analytics loads only through the consent script."""
import os
import tempfile
import unittest
from html import unescape
from pathlib import Path

_tmp = tempfile.TemporaryDirectory()
os.environ.setdefault("DB_PATH", str(Path(_tmp.name) / "test.db"))
os.environ.setdefault("DOWNLOAD_DIR", str(Path(_tmp.name) / "downloads"))

from app import app  # noqa: E402

PAGES = ("/", "/youtube-to-mp3", "/tools", "/uk-vat-calculator", "/privacy-policy",
         "/guides/youtube-video-formats", "/png-to-jpg", "/es/youtube-downloader", "/fr")


class ConsentTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_analytics_tag_is_not_loaded_before_consent(self):
        for path in PAGES:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                page = response.get_data(as_text=True)
                self.assertNotIn("googletagmanager.com", page)
                self.assertNotIn("gtag('config'", page)
                self.assertEqual(page.count("/static/js/consent.js"), 1)
                self.assertIn("data-cookie-settings", page)

    def test_consent_script_gates_the_tag_and_offers_equal_choices(self):
        script = (Path(__file__).resolve().parents[1] / "static" / "js" / "consent.js").read_text(encoding="utf-8")
        self.assertIn("/api/consent-region", script)
        self.assertIn("googletagmanager.com/gtag/js", script)
        self.assertIn("'cookie-accept'", script)
        self.assertIn("'cookie-reject'", script)
        self.assertIn("return true; // when the region is unknown", script)

    def test_privacy_policy_explains_the_choice(self):
        page = unescape(self.client.get("/privacy-policy").get_data(as_text=True))
        self.assertIn("Visitors in the UK, the EU and the wider EEA are asked first", page)
        self.assertIn("Cookie settings", page)


if __name__ == "__main__":
    unittest.main()
