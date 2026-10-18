"""Check published translations as a reciprocal, functional URL set."""

import html
import json
import re
import unittest
from xml.etree import ElementTree

from markupsafe import escape

from app import app
from extractors.detect import detect_url
from guides import GUIDES
from image_tools import IMAGE_TOOLS
from localized_pages import LANGUAGE_UI, LOCALIZED_GUIDES, LOCALIZED_TOOLS, PUBLISHED_SLUGS, alternates
from public_pages import PAGES
from tools import BY_SLUG, PLATFORMS, TOOLS

# Reported by Search Console as "Crawled - currently not indexed" on 2026-10-18.
THIN_PAGES = (
    "/es/youtube-shorts-downloader", "/es/instagram-reels-downloader", "/es/pinterest-video-downloader",
    "/es/facebook-video-downloader", "/es/youtube-video-downloader",
    "/fr/instagram-reels-downloader", "/fr/pinterest-video-downloader", "/fr/facebook-video-downloader",
    "/fr/youtube-shorts-downloader", "/fr/youtube-downloader",
)
SAMPLE_ID = "12345678901"  # numeric and 11 characters: a valid ID shape on every platform


def visible_words(page):
    page = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", " ", page)
    return len(re.findall(r"\w[\w'’.-]*", html.unescape(re.sub(r"<[^>]+>", " ", page))))


def faq_schema_questions(page):
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        data = json.loads(block)
        if data.get("@type") == "FAQPage":
            return [item["name"] for item in data["mainEntity"]]
    return []


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

    def test_sitemap_lists_every_language_version_as_a_plain_url_list(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Robots-Tag"], "noindex")
        text = response.get_data(as_text=True)
        self.assertNotIn("xhtml", text)  # plain sitemap: browsers show it as an XML tree
        root = ElementTree.fromstring(response.data)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        entries = [item.findtext("s:loc", namespaces=ns) for item in root.findall("s:url", ns)]
        self.assertTrue(all(len(item) == 1 for item in root.findall("s:url", ns)))
        expected_count = 3 + len(TOOLS) + len(IMAGE_TOOLS) + len(GUIDES) + len(PAGES)
        expected_count += len(LANGUAGE_UI) * (1 + len(PUBLISHED_SLUGS))
        self.assertEqual(len(entries), expected_count)
        self.assertEqual(len(set(entries)), len(entries))
        self.assertEqual(len(text.splitlines()), expected_count + 3)  # one entry per line
        for slug in (None, *PUBLISHED_SLUGS):
            for _, url in alternates("https://savefromnet.fun", slug):
                self.assertIn(url, entries)

    def test_english_pages_declare_their_language_alternates(self):
        for slug in (None, *PUBLISHED_SLUGS):
            path = "/" + (slug or "")
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                for language, url in alternates("https://savefromnet.fun", slug):
                    self.assertIn(f'hreflang="{language}" href="{url}"', html)

    def test_pages_search_console_found_thin_now_carry_a_full_guide(self):
        for path in THIN_PAGES:
            _, lang, slug = path.split("/")
            self.assertIn(slug, LOCALIZED_GUIDES[lang])
        for lang, guides in LOCALIZED_GUIDES.items():
            self.assertEqual(set(guides), set(PUBLISHED_SLUGS))
            ui = LANGUAGE_UI[lang]
            for slug, guide in guides.items():
                with self.subTest(lang=lang, slug=slug):
                    page = self.client.get(f"/{lang}/{slug}").get_data(as_text=True)
                    for anchor in ('id="steps"', 'id="supported-links"', 'id="format-guide"', 'id="faq"'):
                        self.assertIn(anchor, page)
                        self.assertIn(f'href="#{anchor[4:-1]}"', page)
                    for text in (ui["steps_title"], ui["links_title"], ui["guide_title"], *guide.steps):
                        self.assertIn(str(escape(text)), page)
                    for label, value in guide.facts:
                        self.assertIn(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>", page)
                    for shape, note in guide.links:
                        self.assertIn(f"<dt><code>{escape(shape)}</code></dt><dd>{escape(note)}</dd>", page)
                    for heading, paragraphs in guide.sections:
                        self.assertIn(f"<h3>{escape(heading)}</h3>", page)
                        for paragraph in paragraphs:
                            self.assertIn(f"<p>{escape(paragraph)}</p>", page)
                    questions = [LOCALIZED_TOOLS[lang][slug].question, *(q for q, _ in guide.faq),
                                 ui["faq_availability_question"]]
                    self.assertEqual(faq_schema_questions(page), questions)
                    for question, answer in guide.faq:
                        self.assertIn(f"<summary>{escape(question)}</summary><p>{escape(answer)}</p>", page)
                    for target, label in guide.see_also:
                        self.assertIn(target, PUBLISHED_SLUGS)
                        self.assertNotEqual(target, slug)
                        self.assertIn(f'<a href="/{lang}/{target}">{escape(label)} ', page)
                    # The English tool pages carry 760-990 visible words; these were about 300.
                    self.assertGreaterEqual(visible_words(page), 800)

    def test_guide_link_shapes_are_accepted_by_that_tool(self):
        for lang, guides in LOCALIZED_GUIDES.items():
            for slug, guide in guides.items():
                tool = BY_SLUG[slug]
                for shape, _ in guide.links:
                    with self.subTest(lang=lang, slug=slug, shape=shape):
                        detection = detect_url(re.sub(r"\bID\b", SAMPLE_ID, shape))
                        self.assertIn(detection.platform, PLATFORMS if tool.platform == "universal" else (tool.platform,))
                        self.assertIn(detection.content_type, tool.content_types)

    def test_guides_send_other_link_types_to_the_tool_that_accepts_them(self):
        shorts, videos, reels = (BY_SLUG[slug] for slug in (
            "youtube-shorts-downloader", "youtube-video-downloader", "instagram-reels-downloader"))
        self.assertNotIn(detect_url("https://youtu.be/aqz-KE-bpKQ").content_type, shorts.content_types)
        self.assertNotIn(detect_url("https://www.youtube.com/shorts/aqz-KE-bpKQ").content_type, videos.content_types)
        self.assertIn(detect_url("https://www.youtube.com/shorts/aqz-KE-bpKQ").content_type, BY_SLUG["youtube-downloader"].content_types)
        self.assertIn(detect_url("https://www.youtube.com/shorts/aqz-KE-bpKQ").content_type, BY_SLUG["youtube-to-mp3"].content_types)
        self.assertNotIn(detect_url("https://www.instagram.com/p/C1a2B3c4D5e/").content_type, reels.content_types)
        self.assertIn(detect_url("https://www.instagram.com/p/C1a2B3c4D5e/").content_type, BY_SLUG["instagram-downloader"].content_types)

    def test_english_tool_pages_link_to_their_translations_in_context(self):
        for slug in PUBLISHED_SLUGS:
            with self.subTest(slug=slug):
                page = self.client.get(f"/{slug}").get_data(as_text=True)
                for lang in LANGUAGE_UI:
                    heading = escape(LOCALIZED_TOOLS[lang][slug].heading)
                    self.assertIn(f'<a href="/{lang}/{slug}" hreflang="{lang}" lang="{lang}">{heading}</a>', page)

    def test_unsupported_translation_is_not_a_thin_page(self):
        self.assertEqual(self.client.get("/es/nonexistent-downloader").status_code, 404)
        self.assertEqual(self.client.get("/fr/youtube-to-transcript").status_code, 404)


if __name__ == "__main__":
    unittest.main()
