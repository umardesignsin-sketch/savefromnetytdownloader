import os
import tempfile
import unittest


_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = os.path.join(_tmp.name, "ads-test.db")
os.environ["DOWNLOAD_DIR"] = os.path.join(_tmp.name, "downloads")

from app import app  # noqa: E402

PAGES = ("/", "/youtube-to-mp3", "/youtube-to-mp4", "/batch-image-converter", "/youtube-to-transcript",
         "/guides/youtube-video-formats", "/guides/video-file-size-estimates", "/tools", "/es/youtube-downloader")
VIGNETTE = "s.dataset.zone='12145676',s.src='https://n6wxm.com/vignette.min.js'"


class AdTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_pages_load_no_adsterra_scripts(self):
        for path in PAGES:
            html = self.client.get(path).get_data(as_text=True)
            self.assertNotIn("bellnewyork.org", html, path)
            self.assertNotIn("atOptions", html, path)
            self.assertNotIn("ADVERTISEMENT", html, path)

    def test_monetag_vignette_is_the_first_thing_in_head(self):
        for path in PAGES + ("/privacy-policy",):
            html = self.client.get(path).get_data(as_text=True)
            self.assertEqual(html.count(VIGNETTE), 1, path)
            head = html[html.index("<head>") + len("<head>"):].lstrip()
            self.assertTrue(head.startswith("<script>(function(s){" + VIGNETTE), path)

    def test_privacy_page_names_the_ad_network(self):
        page = self.client.get("/privacy-policy").get_data(as_text=True)
        self.assertNotIn("bellnewyork.org", page)
        self.assertNotIn("does not load third-party advertising scripts", page)
        self.assertIn("SaveFromNet shows ads from Monetag", page)
        self.assertIn("https://monetag.com/privacy/", page)

    def test_house_promo_and_sponsor_contact_stay_below_the_tool(self):
        for path in ("/", "/youtube-to-mp3", "/batch-image-converter"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertEqual(html.count('class="sponsor-section"'), 1, path)
            self.assertIn("mailto:umarisaloneenough@gmail.com?subject=SaveFromNet%20sponsorship", html)
            self.assertLess(html.index("</form>"), html.index('class="sponsor-section"'))


if __name__ == "__main__":
    unittest.main()
