"""Check published translations as a reciprocal, functional URL set."""

import unittest
from xml.etree import ElementTree

from app import app
from guides import GUIDES
from image_tools import IMAGE_TOOLS
from localized_pages import LANGUAGE_UI, PUBLISHED_SLUGS, alternates
from public_pages import PAGES
from tools import TOOLS


class LocalizedPagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_every_published_page_has_working_form_and_reciprocal_metadata(self):
        for lang in LANGUAGE_UI:
            for slug in (None, *PUBLISHED_SLUGS):
                path = f"/{lang}" + (f"/{slug}" if slug else "")
                with self.subTest(path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    html = response.get_data(as_text=True)
                    self.assertIn(f'<html lang="{lang}">', html)
                    self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{path}">', html)
                    self.assertIn('id="download-form"', html)
                    self.assertIn('id="result"', html)
                    self.assertIn(f'data-lang="{lang}"', html)
                    self.assertIn(f'data-tool="{slug or "universal-video-downloader"}"', html)
                    self.assertIn('src="/static/js/site.js"', html)
                    for language, url in alternates("https://savefromnet.fun", slug):
                        self.assertIn(f'hreflang="{language}" href="{url}"', html)

    def test_sitemap_has_exact_published_routes_and_alternates(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        root = ElementTree.fromstring(response.data)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
              "x": "http://www.w3.org/1999/xhtml"}
        entries = {item.findtext("s:loc", namespaces=ns): item for item in root.findall("s:url", ns)}
        expected_count = 3 + len(TOOLS) + len(IMAGE_TOOLS) + len(GUIDES) + len(PAGES)
        expected_count += len(LANGUAGE_UI) * (1 + len(PUBLISHED_SLUGS))
        self.assertEqual(len(entries), expected_count)
        for slug in (None, *PUBLISHED_SLUGS):
            expected = dict(alternates("https://savefromnet.fun", slug))
            for url in set(expected.values()):
                with self.subTest(url=url):
                    self.assertIn(url, entries)
                    links = {item.get("hreflang"): item.get("href")
                             for item in entries[url].findall("x:link", ns)}
                    self.assertEqual(links, expected)

    def test_unsupported_translation_is_not_a_thin_page(self):
        self.assertEqual(self.client.get("/es/nonexistent-downloader").status_code, 404)
        self.assertEqual(self.client.get("/fr/youtube-to-transcript").status_code, 404)


if __name__ == "__main__":
    unittest.main()
