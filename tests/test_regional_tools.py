"""US, UK, Australia and EU tools: data integrity and rendered pages."""
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

from app import app  # noqa: E402
from growth_tools import GROWTH_TOOLS, REGIONAL_TOOLS  # noqa: E402
from regional_data import EU_VAT_RATES, PASSPORT_SPECS, TAX_CALCULATORS, US_STATE_SALES_TAX  # noqa: E402


def data_attribute(page, name):
    match = re.search(rf"{name}='(.*?)'", page, re.S)
    return json.loads(unescape(match.group(1)))


class RegionalDataTests(unittest.TestCase):
    def test_eu_has_27_member_states_within_legal_range(self):
        self.assertEqual(len(EU_VAT_RATES), 27)
        self.assertEqual(len({code for code, _, _ in EU_VAT_RATES}), 27)
        for code, name, rate in EU_VAT_RATES:
            with self.subTest(country=name):
                self.assertGreaterEqual(rate, 15)  # EU minimum standard rate
                self.assertLessEqual(rate, 27)
        rates = dict((name, rate) for _, name, rate in EU_VAT_RATES)
        self.assertEqual((rates["Germany"], rates["Hungary"], rates["Luxembourg"], rates["Finland"]), (19, 27, 17, 25.5))

    def test_us_has_every_state_and_dc_and_five_without_state_tax(self):
        self.assertEqual(len(US_STATE_SALES_TAX), 51)
        self.assertEqual(len({code for code, _, _ in US_STATE_SALES_TAX}), 51)
        self.assertEqual({code for code, _, rate in US_STATE_SALES_TAX if rate == 0}, {"AK", "DE", "MT", "NH", "OR"})
        self.assertEqual(dict((code, rate) for code, _, rate in US_STATE_SALES_TAX)["CA"], 7.25)

    def test_photo_specs_are_consistent(self):
        for key, spec in PASSPORT_SPECS.items():
            with self.subTest(spec=key):
                low, high = spec["head_mm"]
                self.assertTrue(low < spec["target_head_mm"] < high)
                for mm, px in zip(spec["photo_mm"], spec["photo_px"]):
                    self.assertLessEqual(abs(mm / 25.4 * 300 - px), 1)  # 300 dpi output
                self.assertEqual(spec["sheet"]["px"], [1800, 1200])  # 6 x 4 inches at 300 dpi
                self.assertTrue(spec["official_url"].startswith("https://"))
        self.assertEqual(PASSPORT_SPECS["uk"]["online"]["min_px"], [600, 750])
        self.assertIsNone(PASSPORT_SPECS["au"]["online"])  # online renewal uses a photo code


class RegionalPageTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_seven_country_tools_are_registered_once(self):
        self.assertEqual(len(REGIONAL_TOOLS), 7)
        self.assertEqual({tool.region for tool in REGIONAL_TOOLS}, {"US", "UK", "AU", "EU"})
        slugs = [tool.slug for tool in GROWTH_TOOLS]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_passport_pages_render_official_spec_and_modes(self):
        for tool in (t for t in REGIONAL_TOOLS if t.kind == "passport"):
            with self.subTest(tool=tool.slug):
                page = self.client.get(tool.path).get_data(as_text=True)
                spec = data_attribute(page, "data-spec")
                self.assertEqual(spec, PASSPORT_SPECS[tool.preset])
                self.assertIn(f'href="{spec["official_url"]}"', page)
                self.assertIn("passport-photo.mjs", page)
                self.assertIn(unescape(spec["head_label"]), unescape(page))
                self.assertEqual('value="online"' in page, spec["online"] is not None)

    def test_tax_pages_render_config_options_and_tables(self):
        for tool in (t for t in REGIONAL_TOOLS if t.kind == "tax"):
            with self.subTest(tool=tool.slug):
                page = self.client.get(tool.path).get_data(as_text=True)
                config = data_attribute(page, "data-config")
                self.assertEqual(config, json.loads(json.dumps(TAX_CALCULATORS[tool.preset])))
                self.assertIn("tax-tools.mjs", page)
                options = re.findall(r'<select id="tax-rate">(.*?)</select>', page, re.S)[0]
                self.assertEqual(options.count("<option"), len(config["rates"]) + 1)  # plus Custom rate
                rows = page.count("<tr><td>")
                self.assertEqual(rows, len(config["rates"]) if tool.preset in ("eu", "us") else 0)
        self.assertIn('id="tax-local-rate"', self.client.get("/us-sales-tax-calculator").get_data(as_text=True))

    def test_home_and_directory_link_every_country_tool(self):
        home = self.client.get("/").get_data(as_text=True)
        directory = self.client.get("/tools").get_data(as_text=True)
        for page in (home, directory):
            self.assertIn('id="country-tools"', page)
            for tool in REGIONAL_TOOLS:
                self.assertIn(f'href="{tool.path}"', page)

    def test_each_country_tool_links_its_sibling_tools(self):
        for tool in REGIONAL_TOOLS:
            with self.subTest(tool=tool.slug):
                page = self.client.get(tool.path).get_data(as_text=True)
                related = re.search(r'<section aria-labelledby="related-country-tools">(.*?)</section>', page, re.S).group(1)
                siblings = {t.path for t in REGIONAL_TOOLS if t.kind == tool.kind and t.slug != tool.slug}
                self.assertEqual(set(re.findall(r'href="([^"]+)"', related)), siblings)

    def test_privacy_policy_discloses_on_device_photo_processing(self):
        page = unescape(self.client.get("/privacy-policy").get_data(as_text=True))
        self.assertIn("passport photo tools also process your selected image on your device", page)


if __name__ == "__main__":
    unittest.main()
