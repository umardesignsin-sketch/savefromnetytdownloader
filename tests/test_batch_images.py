import io
import os
import tempfile
import unittest
from zipfile import ZipFile

from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener()
_tmp = tempfile.TemporaryDirectory()
os.environ["DB_PATH"] = os.path.join(_tmp.name, "batch-test.db")
os.environ["DOWNLOAD_DIR"] = os.path.join(_tmp.name, "downloads")

from app import app  # noqa: E402


def image(fmt, color):
    data = io.BytesIO()
    Image.new("RGBA" if fmt == "PNG" else "RGB", (80, 60), color).save(data, format=fmt)
    data.seek(0)
    return data


class BatchImageTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_real_mixed_input_zip_and_metadata_removal(self):
        source = image("JPEG", "red")
        source_bytes = source.getvalue()
        response = self.client.post("/api/image/batch", data={
            "format": "webp", "quality": "76",
            "images": [(io.BytesIO(source_bytes), "photo.jpg"), (image("PNG", "blue"), "logo.png")],
        })
        self.assertEqual(response.status_code, 200, response.json if response.is_json else response.status)
        self.assertEqual(response.headers["Content-Type"], "application/zip")
        self.assertEqual(response.headers["X-SFN-Files"], "2")
        self.assertEqual(int(response.headers["X-SFN-Input-Bytes"]), len(source_bytes) + len(image("PNG", "blue").getvalue()))
        with ZipFile(io.BytesIO(response.data)) as bundle:
            self.assertEqual(bundle.namelist(), ["01-photo-batch-webp.webp", "02-logo-batch-webp.webp"])
            for name in bundle.namelist():
                decoded = Image.open(io.BytesIO(bundle.read(name)))
                self.assertEqual(decoded.format, "WEBP")
                self.assertEqual(decoded.size, (80, 60))
                self.assertFalse(decoded.getexif())

    def test_bad_image_stops_entire_batch(self):
        response = self.client.post("/api/image/batch", data={
            "format": "jpg", "images": [(image("PNG", "green"), "good.png"), (io.BytesIO(b"bad"), "bad.png")],
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["code"], "invalid_batch")
        self.assertIn("Image 2", response.json["error"])

    def test_bounds_and_resize_are_enforced(self):
        too_many = self.client.post("/api/image/batch", data={
            "format": "webp", "images": [(image("PNG", "green"), f"{index}.png") for index in range(6)],
        })
        self.assertEqual(too_many.status_code, 400)
        resized = self.client.post("/api/image/batch", data={
            "format": "resize", "width": "40", "images": [(image("JPEG", "green"), "photo.jpg")],
        })
        self.assertEqual(resized.status_code, 200)
        with ZipFile(io.BytesIO(resized.data)) as bundle:
            decoded = Image.open(io.BytesIO(bundle.read(bundle.namelist()[0])))
            self.assertEqual(decoded.size, (40, 30))
            self.assertEqual(decoded.format, "JPEG")

    def test_page_is_indexable_and_linked(self):
        page = self.client.get("/batch-image-converter")
        self.assertEqual(page.status_code, 200)
        html = page.get_data(as_text=True)
        self.assertIn("<h1>Batch Image Converter &amp; Resizer</h1>", html)
        self.assertIn('id="batch-form"', html)
        self.assertIn('rel="canonical" href="https://savefromnet.fun/batch-image-converter"', html)
        self.assertIn("https://savefromnet.fun/batch-image-converter", self.client.get("/sitemap.xml").get_data(as_text=True))
        self.assertIn('href="/batch-image-converter"', self.client.get("/tools").get_data(as_text=True))


if __name__ == "__main__":
    try:
        unittest.main()
    finally:
        _tmp.cleanup()
