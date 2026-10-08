"""Small, bounded batches built on the existing still-image converter."""

from dataclasses import dataclass
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from image_processing import ImageProcessError, process_image


MAX_BATCH_FILES = 5
MAX_PAID_BATCH_FILES = 10
MAX_BATCH_INPUT = 20 * 1024 * 1024
MAX_BATCH_OUTPUT = 32 * 1024 * 1024


@dataclass(frozen=True)
class BatchTool:
    slug: str
    output_format: str
    input_formats: tuple[str, ...] = ("JPEG", "PNG", "WEBP", "HEIC")


FORMATS = {
    "jpg": BatchTool("batch-jpg", "JPEG"),
    "png": BatchTool("batch-png", "PNG"),
    "webp": BatchTool("batch-webp", "WEBP"),
    "heic": BatchTool("batch-heic", "HEIC"),
    "resize": BatchTool("image-resizer", "SAME"),
}


def build_batch(uploads, output_format, quality, width, max_files=MAX_BATCH_FILES):
    """Return a ZIP and actual per-file metadata; fail the whole batch cleanly."""
    if output_format not in FORMATS:
        raise ImageProcessError("Choose JPG, PNG, WebP, HEIC or resize.")
    if not 1 <= len(uploads) <= max_files:
        raise ImageProcessError(f"Choose between 1 and {max_files} images.")
    if output_format == "resize" and not width:
        raise ImageProcessError("Enter an output width for resizing.")

    archive = BytesIO()
    details = []
    total_input = 0
    total_output = 0
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=1, allowZip64=False) as bundle:
        for index, upload in enumerate(uploads, 1):
            # Content-Length is checked by Flask and the Worker; this also
            # rejects a collection of individually valid but oversized files.
            try:
                output, filename, _mime, item = process_image(upload, FORMATS[output_format], quality, width)
            except ImageProcessError as exc:
                raise ImageProcessError(f"Image {index}: {exc}") from exc
            total_input += item["input_bytes"]
            total_output += item["output_bytes"]
            if total_input > MAX_BATCH_INPUT:
                raise ImageProcessError("The batch exceeds 20 MB. Choose fewer or smaller images.")
            if total_output > MAX_BATCH_OUTPUT:
                raise ImageProcessError("The finished batch exceeds 32 MB. Choose smaller images or lower quality.")
            safe_name = f"{index:02d}-{filename}"
            bundle.writestr(safe_name, output.getvalue())
            output.close()
            details.append({"name": safe_name, **item})
    if archive.tell() > MAX_BATCH_OUTPUT:
        raise ImageProcessError("The finished ZIP exceeds 32 MB. Choose smaller images or lower quality.")
    archive.seek(0)
    return archive, {"files": details, "input_bytes": total_input, "output_bytes": total_output}
