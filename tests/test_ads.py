import os
import tempfile
import unittest


_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = os.path.join(_tmp.name, "ads-test.db")
os.environ["DOWNLOAD_DIR"] = os.path.join(_tmp.name, "downloads")

from app import app  # noqa: E402


class AdPlacementTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_both_sidebar_sizes_are_used_on_guides(self):
        short = self.client.get("/guides/youtube-video-formats").get_data(as_text=True)
        long = self.client.get("/guides/video-file-size-estimates").get_data(as_text=True)
        self.assertIn("/22/855c420cee139d00994f3237efb192df", short)
        self.assertNotIn("/22/335372e9de43bf2826e2c791db0b34a8", short)
        self.assertIn("/22/335372e9de43bf2826e2c791db0b34a8", long)

    def test_privacy_page_names_ad_host(self):
        page = self.client.get("/privacy-policy").get_data(as_text=True)
        self.assertIn("advertising scripts served from bellnewyork.org", page)

    def test_supplied_native_unit_is_present_once_below_the_tool(self):
        script = "https://bellnewyork.org/21/d765f412daaaa7ed73d4fc75d6e176b9"
        container = 'id="container-d765f412daaaa7ed73d4fc75d6e176b9"'
        for path in ("/", "/youtube-to-mp3", "/batch-image-converter"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertEqual(html.count(script), 1)
            self.assertEqual(html.count(container), 1)
            self.assertLess(html.index("</form>"), html.index(container))


if __name__ == "__main__":
    unittest.main()
