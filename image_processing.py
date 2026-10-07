"""Bounded, in-memory still-image conversion. No uploaded image is stored."""

from io import BytesIO
from pathlib import Path
import re

from PIL import Image, ImageOps, UnidentifiedImageError
from pillow_heif import register_heif_opener


register_heif_opener()
Image.MAX_IMAGE_PIXELS = 20_000_000
MAX_UPLOAD = 8 * 1024 * 1024
MAX_OUTPUT = 16 * 1024 * 1024
MAX_DIMENSION = 8192
MIME = {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp", "HEIC": "image/heic"}
EXTENSION = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "HEIC": "heic"}


class ImageProcessError(ValueError):
    pass


def process_image(upload, tool, quality_value, width_value):
    data = upload.stream.read(MAX_UPLOAD + 1)
    if not data:
        raise ImageProcessError("Choose an image to upload.")
    if len(data) > MAX_UPLOAD:
        raise ImageProcessError("The image must be 8 MB or smaller.")
    try:
        source = Image.open(BytesIO(data))
        source_format = "HEIC" if source.format == "HEIF" else source.format
        if source_format not in tool.input_formats:
            supported = ", ".join("JPG" if name == "JPEG" else name for name in tool.input_formats)
            raise ImageProcessError(f"This tool accepts {supported} images. Choose a different file or tool.")
        if getattr(source, "n_frames", 1) != 1:
            raise ImageProcessError("Animated and multi-frame images are not supported.")
        width, height = source.size
        if width < 1 or height < 1 or width > MAX_DIMENSION or height > MAX_DIMENSION or width * height > 20_000_000:
            raise ImageProcessError("Image dimensions exceed the 20-megapixel or 8192-pixel limit.")
        source.load()
        image = ImageOps.exif_transpose(source)
        # Rebuild pixels so source metadata, including GPS EXIF, is not copied.
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        image = image.copy()
        if tool.slug == "image-resizer":
            width, height = image.size
            try:
                target_width = int(width_value)
            except (TypeError, ValueError):
                raise ImageProcessError("Enter a valid output width in pixels.") from None
            if target_width < 1 or target_width > width:
                raise ImageProcessError(f"Choose a width between 1 and {width} pixels.")
            target_height = max(1, round(height * target_width / width))
            image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        output_format = source_format if tool.output_format == "SAME" else tool.output_format
        if output_format in ("JPEG", "WEBP", "HEIC"):
            try:
                quality = int(quality_value or 82)
            except (TypeError, ValueError):
                raise ImageProcessError("Choose a quality from 40 to 95.") from None
            if quality < 40 or quality > 95:
                raise ImageProcessError("Choose a quality from 40 to 95.")
        else:
            quality = None
        if output_format == "JPEG" and image.mode == "RGBA":
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.getchannel("A"))
            image = background
        output = BytesIO()
        options = {"optimize": True} if output_format == "PNG" else {"quality": quality}
        image.save(output, format="HEIF" if output_format == "HEIC" else output_format, **options)
        if output.tell() > MAX_OUTPUT:
            raise ImageProcessError("The result exceeds 16 MB. Try a smaller image or lower quality.")
        output.seek(0)
        stem = re.sub(r"[^A-Za-z0-9_-]", "-", Path(upload.filename or "image").stem).strip("-")[:48] or "image"
        return output, f"{stem}-{tool.slug}.{EXTENSION[output_format]}", MIME[output_format], {
            "input_bytes": len(data), "output_bytes": output.getbuffer().nbytes,
            "width": image.width, "height": image.height, "format": output_format,
        }
    except ImageProcessError:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise ImageProcessError("This image could not be decoded or converted. Try a valid still image.") from exc
