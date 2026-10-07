import io
import json
import os
import tempfile
import unittest
from xml.etree import ElementTree

from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener()
_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = os.path.join(_tmp.name, "test.db")
os.environ["DOWNLOAD_DIR"] = os.path.join(_tmp.name, "downloads")

from app import app  # noqa: E402
from image_tools import IMAGE_TOOLS  # noqa: E402


class ImageToolTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def image(self, fmt):
        output = io.BytesIO()
        Image.new("RGB", (64, 48), (230, 80, 50)).save(output, format="HEIF" if fmt == "HEIC" else fmt)
        output.seek(0)
        return output

    def convert(self, slug, fmt, **fields):
        return app.test_client().post("/api/image/process", data={"tool": slug, "image": (self.image(fmt), "photo." + fmt.lower()), **fields})

    def test_all_image_pages_are_indexable_and_linked(self):
        sitemap = ElementTree.fromstring(self.client.get("/sitemap.xml").data)
        locs = {item.text for item in sitemap.findall(".//{*}loc")}
        directory = self.client.get("/tools").get_data(as_text=True)
        for tool in IMAGE_TOOLS:
            with self.subTest(tool=tool.slug):
                response = self.client.get(tool.path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn(f'<link rel="canonical" href="https://savefromnet.fun{tool.path}">', html)
                self.assertIn(f"<h1>{tool.name}</h1>", html)
                self.assertIn('id="image-form"', html)
                self.assertIn('"@type": "FAQPage"', html)
                self.assertIn("https://savefromnet.fun" + tool.path, locs)
                self.assertIn('href="' + tool.path + '"', directory)

    def test_every_conversion_returns_decodable_expected_format(self):
        cases = (
            ("image-compressor", "PNG", "WEBP"),
            ("png-to-heic", "PNG", "HEIF"),
            ("jpg-to-heic", "JPEG", "HEIF"),
            ("heic-to-jpg", "HEIC", "JPEG"),
            ("heic-to-png", "HEIC", "PNG"),
            ("png-to-webp", "PNG", "WEBP"),
            ("jpg-to-png", "JPEG", "PNG"),
            ("webp-to-png", "WEBP", "PNG"),
            ("image-resizer", "JPEG", "JPEG"),
        )
        for slug, source, expected in cases:
            with self.subTest(slug=slug):
                response = self.convert(slug, source, width="32" if slug == "image-resizer" else "")
                self.assertEqual(response.status_code, 200, response.data[:200])
                decoded = Image.open(io.BytesIO(response.data))
                self.assertEqual(decoded.format, expected)
                self.assertEqual(decoded.size, (32, 24) if slug == "image-resizer" else (64, 48))
                self.assertEqual(int(response.headers["X-SFN-Output-Bytes"]), len(response.data))
                if slug.endswith("to-heic"):
                    self.assertIn(b"ftypheic", response.data[:24])

    def test_invalid_and_wrong_images_fail_cleanly(self):
        response = self.client.post("/api/image/process", data={"tool": "png-to-heic", "image": (io.BytesIO(b"not an image"), "bad.png")})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["code"], "invalid_image")
        wrong = self.convert("png-to-heic", "JPEG")
        self.assertEqual(wrong.status_code, 422)
        large = app.test_client().post("/api/image/process", data={"tool": "png-to-heic", "image": (io.BytesIO(b"x" * (8 * 1024 * 1024 + 1)), "large.png")})
        self.assertEqual(large.status_code, 422)

    def test_animated_and_oversized_dimensions_are_rejected(self):
        animation = io.BytesIO()
        frames = [Image.new("RGB", (8, 8), color) for color in ("red", "blue")]
        frames[0].save(animation, format="WEBP", save_all=True, append_images=frames[1:], duration=100)
        animation.seek(0)
        animated = app.test_client().post("/api/image/process", data={"tool": "image-compressor", "image": (animation, "animated.webp")})
        self.assertEqual(animated.status_code, 422)
        self.assertIn("multi-frame", animated.json["error"])
        huge = io.BytesIO()
        Image.new("RGB", (8200, 1), "red").save(huge, format="PNG")
        huge.seek(0)
        oversized = app.test_client().post("/api/image/process", data={"tool": "png-to-webp", "image": (huge, "wide.png")})
        self.assertEqual(oversized.status_code, 422)
        self.assertIn("dimensions", oversized.json["error"])


if __name__ == "__main__":
    try:
        unittest.main()
    finally:
        _tmp.cleanup()
