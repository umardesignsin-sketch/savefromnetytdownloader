"""Security, route, and real-format contract checks without hitting source sites."""

import csv
import json
import os
import re
import tempfile
import unittest
from html import escape
from pathlib import Path
from urllib.parse import urlsplit
from unittest.mock import patch
from xml.etree import ElementTree
from markupsafe import escape as template_escape

_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = str(Path(_tmp.name) / "test.db")
os.environ["DOWNLOAD_DIR"] = str(Path(_tmp.name) / "downloads")

from app import _signed_link, app  # noqa: E402
import db  # noqa: E402
from downloader import file_path  # noqa: E402
from extractors.detect import DetectError, detect_url  # noqa: E402
from extractors.service import _yt_formats  # noqa: E402
from guides import GUIDES  # noqa: E402
from image_tools import IMAGE_TOOLS  # noqa: E402
from localized_pages import LANGUAGE_UI, PUBLISHED_SLUGS  # noqa: E402
from public_pages import PAGES, TOOL_GROUPS  # noqa: E402
from tools import TOOLS, TOOL_SECTIONS, TOOL_SEO_LINKS  # noqa: E402


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

    def test_reddit_permalinks_and_short_links_route_to_one_post(self):
        cases = (
            ("https://www.reddit.com/r/aww/comments/1aoccwo/title/?utm_source=share",
             "https://www.reddit.com/r/aww/comments/1aoccwo/"),
            ("https://redd.it/1aoccwo", "https://redd.it/1aoccwo"),
            ("https://www.reddit.com/user/creator/comments/1aoccwo/title/",
             "https://www.reddit.com/user/creator/comments/1aoccwo/"),
        )
        for url, normalized in cases:
            with self.subTest(url=url):
                detected = detect_url(url)
                self.assertEqual((detected.platform, detected.content_type, detected.normalized_url),
                                 ("reddit", "post", normalized))
        with self.assertRaises(DetectError):
            detect_url("https://www.reddit.com/r/aww/")


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

    def test_missing_video_size_never_displays_audio_size_as_total(self):
        found = _yt_formats({"formats": [
            {"format_id": "v", "ext": "mp4", "vcodec": "av1", "acodec": "none", "height": 720},
            {"format_id": "a", "ext": "m4a", "vcodec": "none", "acodec": "aac", "filesize": 25_077_688},
        ]})
        video = next(item for item in found if item["type"] == "video")
        self.assertIsNone(video["filesize"])

    def test_oversized_2160p_estimate_is_not_offered(self):
        found = _yt_formats({"duration": 1549, "formats": [
            {"format_id": "v2160", "ext": "mp4", "vcodec": "av1", "acodec": "none",
             "height": 2160, "tbr": 19027},
            {"format_id": "v720", "ext": "mp4", "vcodec": "h264", "acodec": "none",
             "height": 720, "filesize": 120_000_000},
            {"format_id": "a", "ext": "m4a", "vcodec": "none", "acodec": "aac",
             "filesize": 25_077_688, "abr": 129},
        ]})
        videos = [item for item in found if item["type"] == "video"]
        self.assertEqual([item["quality"] for item in videos], ["720p"])
        self.assertEqual(videos[0]["filesize"], 145_077_688)


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_legacy_search_redirects_point_to_indexable_pages(self):
        redirects = Path(__file__).resolve().parents[1] / "_redirects"
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        for line in redirects.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            source, target, status = line.split()
            with self.subTest(source=source):
                self.assertEqual(status, "301")
                self.assertNotIn(f"<loc>https://savefromnet.fun{source}</loc>", sitemap)
                self.assertEqual(self.client.get(target).status_code, 200)
                self.assertIn(f"<loc>https://savefromnet.fun{target}</loc>", sitemap)

    def test_youtube_help_navigation_and_guide_are_reachable(self):
        for slug in ("youtube-downloader", "youtube-video-downloader", "youtube-shorts-downloader", "youtube-to-mp3"):
            with self.subTest(slug=slug):
                html = self.client.get("/" + slug).get_data(as_text=True)
                self.assertIn('aria-label="On this page"', html)
                for anchor in ("how-it-works", "supported-links", "format-guide", "faq"):
                    self.assertIn(f'href="#{anchor}"', html)
                    self.assertIn(f'id="{anchor}"', html)
                self.assertIn('href="/guides/how-to-copy-a-youtube-link"', html)
        guide = self.client.get("/guides/how-to-copy-a-youtube-link")
        self.assertEqual(guide.status_code, 200)
        self.assertIn('rel="canonical" href="https://savefromnet.fun/guides/how-to-copy-a-youtube-link"', guide.get_data(as_text=True))
        self.assertIn('/guides/how-to-copy-a-youtube-link', self.client.get('/sitemap.xml').get_data(as_text=True))

    def test_all_tool_routes_have_metadata_and_schema(self):
        self.assertEqual(len(TOOLS), 26)
        for tool in TOOLS:
            with self.subTest(slug=tool.slug):
                response = self.client.get(tool.path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{tool.path}">', html)
                self.assertIn(f'<h1 id="download-heading">{escape(tool.heading)}</h1>', html)
                schemas = [json.loads(block.split('</script>')[0]) for block in html.split('<script type="application/ld+json">')[1:]]
                self.assertEqual({s["@type"] for s in schemas}, {"WebApplication", "FAQPage", "BreadcrumbList"})
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        self.assertEqual(sitemap.count("<url>"), 29 + len(GUIDES) + len(PAGES) + len(IMAGE_TOOLS) + len(LANGUAGE_UI) * (1 + len(PUBLISHED_SLUGS)))
        home = self.client.get("/").get_data(as_text=True)
        self.assertIn("<h1 id=\"download-heading\">Video Downloader <em>&amp; Converter</em></h1>", home)
        self.assertIn('href="/guides"', home)

    def test_priority_youtube_intents_keep_existing_canonicals(self):
        home = self.client.get("/").get_data(as_text=True)
        self.assertIn("<title>SaveFromNet | Video Downloader &amp; Converter</title>", home)
        self.assertIn('href="/youtube-video-downloader">YouTube Video Downloader</a>', home)
        home_schemas = [json.loads(block.split('</script>')[0]) for block in home.split('<script type="application/ld+json">')[1:]]
        self.assertEqual(next(schema for schema in home_schemas if schema["@type"] == "WebSite")["url"], "https://savefromnet.fun/")
        targets = (
            ("/youtube-downloader", "YouTube Downloader & Converter", "Choose video or audio in the YouTube converter"),
            ("/youtube-video-downloader", "YouTube Video Downloader", "Download a YouTube video with SaveFromNet"),
            ("/youtube-to-mp3", "YouTube to MP3 Converter", "Get a YouTube MP3 download from a public link"),
        )
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        for path, heading, section in targets:
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{path}">', html)
                self.assertIn(f'<h1 id="download-heading">{escape(heading)}</h1>', html)
                self.assertIn(f'<h2>{escape(section)}</h2>', html)
                self.assertEqual(sitemap.count(f'<loc>https://savefromnet.fun{path}</loc>'), 1)

    def test_reddit_downloader_has_one_canonical_and_a_real_video_api(self):
        path = "/reddit-video-downloader"
        page = self.client.get(path).get_data(as_text=True)
        self.assertIn("<title>Reddit Video Downloader | SaveFromNet</title>", page)
        self.assertIn('<link rel="canonical" href="https://savefromnet.fun/reddit-video-downloader">', page)
        self.assertIn('<h1 id="download-heading">Reddit Video Downloader</h1>', page)
        self.assertIn("Paste a Reddit post URL", page)
        for heading in ("How to download a Reddit video", "Reddit video download with sound",
                        "Which Reddit video links work?", "When the Reddit downloader cannot access a post"):
            self.assertIn(f"<h2>{heading}</h2>", page)
        self.assertIn('href="/reddit-video-downloader"', self.client.get("/").get_data(as_text=True))
        self.assertEqual(self.client.get("/sitemap.xml").get_data(as_text=True).count(
            "<loc>https://savefromnet.fun/reddit-video-downloader</loc>"), 1)

        media = {"platform": "reddit", "type": "post", "title": "Public test post",
                 "author": "creator", "thumbnail": None, "duration": 12,
                 "formats": [{"id": "v0", "type": "video", "extension": "mp4", "quality": "640p"},
                             {"id": "a-source", "type": "audio", "extension": "m4a", "quality": "Original audio"}]}
        with patch("app.analyze", return_value=media):
            response = self.client.post("/api/analyze", json={"tool": "reddit-video-downloader",
                "url": "https://www.reddit.com/r/aww/comments/1aoccwo/"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["platform"], "reddit")
        self.assertEqual([item["type"] for item in data["formats"]], ["video"])

    def test_editorial_tool_sections_are_distinct_and_link_to_real_pages(self):
        self.assertGreaterEqual(len(TOOL_SECTIONS), 15)
        self.assertEqual(set(TOOL_SECTIONS), set(TOOL_SEO_LINKS))
        headings = []
        for tool in TOOLS:
            if not tool.seo_sections:
                continue
            with self.subTest(slug=tool.slug):
                self.assertGreaterEqual(len(tool.seo_sections), 2)
                html = self.client.get(tool.path).get_data(as_text=True)
                guide_label = 'YOUTUBE TRANSCRIPT GUIDE' if tool.slug == 'youtube-to-transcript' else f'{tool.platform.upper()} DOWNLOAD GUIDE'
                self.assertIn(guide_label, html)
                for heading, paragraphs in tool.seo_sections:
                    headings.append(heading)
                    self.assertIn(f'<h2>{template_escape(heading)}</h2>', html)
                    self.assertTrue(all(len(paragraph.split()) >= 20 for paragraph in paragraphs))
                for path, label in tool.seo_links:
                    self.assertIn(f'href="{path}">{escape(label)}</a>', html)
                    self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(len(headings), len(set(headings)))

    def test_guides_have_unique_content_working_forms_and_sitemap_urls(self):
        self.assertEqual(len({guide.slug for guide in GUIDES}), len(GUIDES))
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        hub = self.client.get("/guides").get_data(as_text=True)
        self.assertIn('<link rel="canonical" href="https://savefromnet.fun/guides">', hub)
        for guide in GUIDES:
            with self.subTest(slug=guide.slug):
                response = self.client.get(guide.path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{guide.path}">', html)
                self.assertIn(f'<h1 id="download-heading">{escape(guide.title)}</h1>', html)
                self.assertIn('id="download-form"', html)
                self.assertIn(f'href="{guide.path}"', hub)
                self.assertIn(f'<loc>https://savefromnet.fun{guide.path}</loc>', sitemap)
                self.assertGreaterEqual(len(guide.sections), 3)
                self.assertTrue(all(len(text.split()) >= 30 for _, text in guide.sections))
                schemas = [json.loads(block.split('</script>')[0]) for block in html.split('<script type="application/ld+json">')[1:]]
                self.assertEqual({schema["@type"] for schema in schemas}, {"Article", "FAQPage", "BreadcrumbList"})
        self.assertEqual(self.client.get("/guides/not-a-guide").status_code, 404)
        missing = self.client.get("/not-a-real-tool")
        self.assertEqual(missing.status_code, 404)
        self.assertIn('<meta name="robots" content="noindex,follow">', missing.get_data(as_text=True))

    def test_new_guides_use_working_tools_and_are_discoverable(self):
        new = {"tiktok-photo-posts", "facebook-reels", "pinterest-images",
               "video-file-size-estimates", "temporary-download-links", "video-with-no-sound"}
        guide_by_slug = {guide.slug: guide for guide in GUIDES}
        self.assertTrue(new <= guide_by_slug.keys())
        directory = self.client.get("/tools").get_data(as_text=True)
        for slug in new:
            with self.subTest(slug=slug):
                guide = guide_by_slug[slug]
                html = self.client.get(guide.path).get_data(as_text=True)
                self.assertIn(f'data-tool="{guide.tool_slug}"', html)
                self.assertIn(f'href="{guide.path}"', directory)
                for related_slug in guide.related:
                    self.assertIn(f'href="/guides/{related_slug}"', html)
        examples = (
            ("tiktok-photo-posts", "https://www.tiktok.com/@creator/photo/1234567890", "photo"),
            ("facebook-reels", "https://www.facebook.com/reel/1234567890", "video"),
            ("pinterest-images", "https://www.pinterest.com/pin/809522101770089198/", "pin"),
        )
        tools = {tool.slug: tool for tool in TOOLS}
        for slug, url, kind in examples:
            with self.subTest(url=url):
                detected = detect_url(url)
                self.assertEqual(detected.content_type, kind)
                tool = tools[guide_by_slug[slug].tool_slug]
                self.assertEqual(detected.platform, tool.platform)
                self.assertIn(kind, tool.content_types)

    def test_format_guide_and_size_calculator_are_linked_to_working_tools(self):
        image_guide = self.client.get("/image-format-guide")
        self.assertEqual(image_guide.status_code, 200)
        image_html = image_guide.get_data(as_text=True)
        self.assertIn('href="/image-compressor"', image_html)
        self.assertIn('href="/heic-to-jpg"', image_html)
        self.assertIn('href="/image-resizer"', image_html)
        self.assertIn('href="/image-format-guide"', self.client.get("/tools").get_data(as_text=True))
        self.assertIn('href="/image-format-guide"', self.client.get("/png-to-heic").get_data(as_text=True))

        size_html = self.client.get("/guides/video-file-size-estimates").get_data(as_text=True)
        self.assertIn('id="size-estimator"', size_html)
        self.assertIn('name="videoKbps"', size_html)
        self.assertIn('name="audioKbps"', size_html)
        self.assertIn('id="size-share-link"', size_html)
        self.assertIn('id="size-share-copy"', size_html)
        self.assertIn('id="size-reference-heading"', size_html)
        self.assertIn('<th scope="row">20 Mbps</th><td>3.75 GB</td><td>9.00 GB</td>', size_html)
        self.assertIn('src="/static/js/size-estimator.mjs"', size_html)
        self.assertIn('href="/guides/video-file-size-estimates"', self.client.get("/").get_data(as_text=True))

    def test_public_navigation_and_sitemap_resolve(self):
        paths = ["/", "/guides", "/batch-image-converter"] + [tool.path for tool in TOOLS] + [tool.path for tool in IMAGE_TOOLS] + [guide.path for guide in GUIDES] + [page.path for page in PAGES]
        paths += [f"/{lang}" for lang in LANGUAGE_UI]
        paths += [f"/{lang}/{slug}" for lang in LANGUAGE_UI for slug in PUBLISHED_SLUGS]
        sitemap = ElementTree.fromstring(self.client.get("/sitemap.xml").data)
        locs = [node.text for node in sitemap.findall(".//{*}loc")]
        self.assertEqual(set(locs), {"https://savefromnet.fun" + path for path in paths})
        self.assertEqual(len(locs), len(paths))
        inventory = Path(__file__).resolve().parents[1] / "growth" / "savefromnet-url-inventory.csv"
        with inventory.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual({row["url"] for row in rows}, set(locs))
        self.assertTrue(all(row["canonical"] == row["url"] and row["robots"] == "indexable"
                            for row in rows))
        titles = set()
        descriptions = set()
        for path in paths:
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                title = re.search(r"<title>(.*?)</title>", html)
                description = re.search(r'<meta name="description" content="([^"]+)"', html)
                self.assertIsNotNone(title)
                self.assertIsNotNone(description)
                titles.add(title.group(1))
                descriptions.add(description.group(1))
                links = {urlsplit(link).path or "/" for link in re.findall(r'href="(/[^"]*)"', html)}
                for link in links:
                    if link == "/developers":  # Served by the Cloudflare Worker, not Flask.
                        continue
                    response = self.client.get(link)
                    try:
                        self.assertEqual(response.status_code, 200, f"Broken link {link} on {path}")
                    finally:
                        response.close()
        self.assertEqual(len(titles), len(paths))
        self.assertEqual(len(descriptions), len(paths))

    def test_directory_resource_and_trust_pages_are_unique_and_indexable(self):
        self.assertEqual(len(PAGES), 15)
        self.assertEqual(len({page.title for page in PAGES}), len(PAGES))
        for page in PAGES:
            with self.subTest(page=page.slug):
                response = self.client.get(page.path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{page.path}">', html)
                self.assertIn(f"<h1>{escape(page.heading)}</h1>", html)
                self.assertNotIn('id="download-form"', html)
                self.assertIn('href="/privacy-policy"', html)
                self.assertIn('href="/terms"', html)
        directory = self.client.get("/tools").get_data(as_text=True)
        self.assertEqual({slug for _name, slugs in TOOL_GROUPS for slug in slugs}, {tool.slug for tool in TOOLS})
        for _name, slugs in TOOL_GROUPS:
            for slug in slugs:
                self.assertIn(f'href="/{slug}"', directory)

    def test_aggregate_events_accept_real_tool_context_only(self):
        accepted = self.client.post("/api/event", json={"event": "tool_page_view", "platform": "youtube", "tool": "youtube-to-mp3"})
        self.assertEqual(accepted.status_code, 200)
        failure = self.client.post("/api/event", json={"event": "download_failed", "platform": "youtube", "tool": "youtube-to-mp3", "format": "mp3"})
        self.assertEqual(failure.status_code, 200)
        wrong = self.client.post("/api/event", json={"event": "tool_page_view", "platform": "tiktok", "tool": "youtube-to-mp3"})
        self.assertEqual(wrong.status_code, 400)

    def test_former_ad_worker_is_inert_and_pages_have_no_monetag(self):
        response = self.client.get("/sw.js")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "application/javascript")
            self.assertEqual(response.data, (Path(__file__).resolve().parents[1] / "sw.js").read_bytes())
            self.assertIn(b"self.registration.unregister()", response.data)
            self.assertNotIn(b"importScripts", response.data)
        finally:
            response.close()
        for path in ("/", "/youtube-to-mp3", "/batch-image-converter"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertNotIn("quge5.com", html)
            self.assertNotIn("data-zone=", html)

    def test_ad_units_are_below_the_downloader(self):
        ad_script = "https://bellnewyork.org/22/8096c015c04997e3612febc8ea789e67"
        ad_container = 'class="container sponsor-banner"'
        for path in ("/", "/youtube-to-mp3", "/batch-image-converter"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertEqual(html.count(ad_script), 1)
            self.assertEqual(html.count(ad_container), 1)
            self.assertEqual(html.count("/14/ba51614fef660ec06fedd8ab0bcef557"), 1)
            self.assertLess(html.index("</form>"), html.index(ad_container))

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
