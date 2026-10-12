import os
import tempfile
import unittest


_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = os.path.join(_tmp.name, "ads-test.db")
os.environ["DOWNLOAD_DIR"] = os.path.join(_tmp.name, "downloads")

from app import app  # noqa: E402

PAGES = ("/", "/youtube-to-mp3", "/youtube-to-mp4", "/batch-image-converter", "/youtube-to-transcript",
         "/guides/youtube-video-formats", "/guides/video-file-size-estimates", "/tools", "/es/youtube-downloader")


class NoThirdPartyAdsTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pages_load_no_adsterra_scripts(self):
        for path in PAGES:
            html = self.client.get(path).get_data(as_text=True)
            self.assertNotIn("bellnewyork.org", html, path)
            self.assertNotIn("atOptions", html, path)
            self.assertNotIn("ADVERTISEMENT", html, path)

    def test_privacy_page_says_no_ad_scripts(self):
        page = self.client.get("/privacy-policy").get_data(as_text=True)
        self.assertNotIn("bellnewyork.org", page)
        self.assertIn("does not load third-party advertising scripts", page)

    def test_house_promo_and_sponsor_contact_stay_below_the_tool(self):
        for path in ("/", "/youtube-to-mp3", "/batch-image-converter"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertEqual(html.count('class="sponsor-section"'), 1, path)
            self.assertIn("mailto:umarisaloneenough@gmail.com?subject=SaveFromNet%20sponsorship", html)
            self.assertLess(html.index("</form>"), html.index('class="sponsor-section"'))


if __name__ == "__main__":
    unittest.main()
