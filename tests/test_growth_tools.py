"""Routes, SEO metadata, validation and guarded upstream integrations."""

import html
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = str(Path(_tmp.name) / "growth-test.db")
os.environ["DOWNLOAD_DIR"] = str(Path(_tmp.name) / "downloads")

from app import _limits, app  # noqa: E402
from growth_services import GrowthServiceError, _public_nws_url, us_forecast  # noqa: E402
from growth_tools import GROWTH_TOOLS  # noqa: E402


class Response:
    def __init__(self, data=None, status=200):
        self.data = data
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            import requests
            raise requests.HTTPError("upstream error")

    def json(self):
        return self.data


class GrowthToolTests(unittest.TestCase):
    def setUp(self):
        _limits.clear()
        self.client = app.test_client()

    def test_pages_have_unique_meta_schema_forms_and_links(self):
        sitemap = ElementTree.fromstring(self.client.get("/sitemap.xml").data)
        urls = {entry.text for entry in sitemap.findall(".//{*}loc")}
        directory = self.client.get("/tools").get_data(as_text=True)
        home = self.client.get("/").get_data(as_text=True)
        titles = set()
        descriptions = set()
        for tool in GROWTH_TOOLS:
            with self.subTest(tool=tool.slug):
                response = self.client.get(tool.path)
                self.assertEqual(response.status_code, 200)
                page = response.get_data(as_text=True)
                title = re.search(r"<title>(.*?)</title>", page).group(1)
                description = re.search(r'<meta name="description" content="(.*?)">', page).group(1)
                self.assertNotIn(title, titles)
                self.assertNotIn(description, descriptions)
                titles.add(title)
                descriptions.add(description)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{tool.path}">', page)
                self.assertIn('"@type": "WebApplication"', page)
                self.assertIn('"@type": "FAQPage"', page)
                self.assertIn('"@type": "BreadcrumbList"', page)
                self.assertIn(f'href="{tool.path}"', directory)
                self.assertIn(f'href="{tool.path}"', home)
                self.assertIn("https://savefromnet.fun" + tool.path, urls)
                self.assertIn(f"<h1>{tool.name}</h1>", page)
                self.assertIn('growth-tools.mjs', page)
                self.assertIn('growth-tools.css', page)
                for question, answer in tool.faq:
                    self.assertIn(html.escape(question), page)
                    self.assertIn(answer, html.unescape(page))
                scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page)
                self.assertTrue(all(isinstance(json.loads(script), dict) for script in scripts))

    def test_translation_validation_and_real_response(self):
        for payload in ({}, {"text": "x" * 501, "source": "en", "target": "es"},
                        {"text": "Hello", "source": "en", "target": "en"},
                        {"text": "Hello", "source": "xx", "target": "es"}):
            with self.subTest(payload=payload):
                _limits.clear()
                response = self.client.post("/api/translate", json=payload)
                self.assertEqual(response.status_code, 400)
        _limits.clear()
        upstream = Response({"responseStatus": 200, "responseData": {"translatedText": "Hola &amp; adiós"}})
        with patch("growth_services.requests.get", return_value=upstream) as request_get:
            response = self.client.post("/api/translate", json={"text": "Hello & goodbye", "source": "en", "target": "es"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["translation"], "Hola & adiós")
        self.assertEqual(request_get.call_args.kwargs["params"]["langpair"], "en|es")
        self.assertEqual(request_get.call_args.args[0], "https://api.mymemory.translated.net/get")

    def test_translation_upstream_failure_is_not_fake(self):
        with patch("growth_services.requests.get", return_value=Response({"responseStatus": 429, "responseData": {"translatedText": "Hello"}})):
            response = self.client.post("/api/translate", json={"text": "Hello", "source": "en", "target": "es"})
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("translation", response.json)

        _limits.clear()
        with patch("growth_services.requests.get", return_value=Response({"responseStatus": 200, "responseData": []})):
            response = self.client.post("/api/translate", json={"text": "Hello", "source": "en", "target": "es"})
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("translation", response.json)

    def test_api_request_size_is_bounded(self):
        for path in ("/api/translate", "/api/weather/us"):
            with self.subTest(path=path):
                _limits.clear()
                response = self.client.post(path, data="x" * 4100,
                                            content_type="application/json")
                self.assertEqual(response.status_code, 413)

    def test_forecast_validation_and_source_url_guard(self):
        for value in ("", "1234", "123456", "1000x", "https://example.org", None):
            with self.subTest(value=value):
                _limits.clear()
                response = self.client.post("/api/weather/us", json={"zip": value})
                self.assertEqual(response.status_code, 400)
        for url in ("http://api.weather.gov/gridpoints/ABC/1,2/forecast",
                    "https://api.weather.gov.evil.test/gridpoints/ABC/1,2/forecast",
                    "https://api.weather.gov@evil.test/gridpoints/ABC/1,2/forecast",
                    "https://api.weather.gov:444/gridpoints/ABC/1,2/forecast",
                    "https://api.weather.gov/admin"):
            with self.subTest(url=url), self.assertRaises(GrowthServiceError):
                _public_nws_url(url)

    def test_forecast_returns_actual_periods_and_caches(self):
        zip_response = Response({"places": [{"place name": "New York", "state abbreviation": "NY",
                                              "latitude": "40.7506", "longitude": "-73.9972"}]})
        points_response = Response({"properties": {"forecast": "https://api.weather.gov/gridpoints/OKX/1,2/forecast"}})
        forecast_response = Response({"properties": {"updated": "2026-10-12T12:00:00Z", "periods": [
            {"name": "Today", "temperature": 72, "temperatureUnit": "F", "shortForecast": "Sunny",
             "detailedForecast": "Sunny all day.", "windSpeed": "5 mph", "windDirection": "W"}]}})
        with patch("growth_services.requests.get", side_effect=[zip_response, points_response, forecast_response]) as request_get:
            first = us_forecast("10001")
            second = us_forecast("10001")
        self.assertEqual(first, second)
        self.assertEqual(first["periods"][0]["short_forecast"], "Sunny")
        self.assertEqual(request_get.call_count, 3)
        self.assertEqual(request_get.call_args_list[-1].args[0], first["source_url"])

    def test_unknown_zip_and_malicious_forecast_link(self):
        with patch("growth_services.requests.get", return_value=Response(status=404)):
            response = self.client.post("/api/weather/us", json={"zip": "00000"})
        self.assertEqual(response.status_code, 404)
        location = Response({"places": [{"place name": "Test", "state abbreviation": "CA",
                                         "latitude": "34", "longitude": "-118"}]})
        malicious = Response({"properties": {"forecast": "https://evil.test/private"}})
        with patch("growth_services.requests.get", side_effect=[location, malicious]) as request_get:
            response = self.client.post("/api/weather/us", json={"zip": "90210"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(request_get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
