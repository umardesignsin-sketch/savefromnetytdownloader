"""Fetch only public YouTube-hosted image thumbnails for validated video IDs."""

from io import BytesIO

from PIL import Image, UnidentifiedImageError
import requests

from extractors.detect import DetectError, detect_url


class ThumbnailError(ValueError):
    pass


def get_thumbnail(raw_url):
    try:
        detection = detect_url(raw_url)
    except DetectError as exc:
        raise ThumbnailError(str(exc)) from exc
    if detection.platform != "youtube":
        raise ThumbnailError("Paste a link to one YouTube video or Short.")
    video_id = detection.normalized_url.rsplit("=", 1)[-1]
    for name in ("maxresdefault", "hqdefault"):
        url = f"https://i.ytimg.com/vi/{video_id}/{name}.jpg"
        try:
            with requests.get(url, timeout=(3, 6), stream=True, allow_redirects=False) as response:
                if response.status_code != 200 or not response.headers.get("Content-Type", "").lower().startswith("image/jpeg"):
                    continue
                data = bytearray()
                for chunk in response.iter_content(64 * 1024):
                    data.extend(chunk)
                    if len(data) > 2 * 1024 * 1024:
                        raise ThumbnailError("The thumbnail is too large to serve.")
        except requests.RequestException:
            continue
        try:
            with Image.open(BytesIO(data)) as image:
                if image.format != "JPEG" or image.width < 320 or image.height < 180:
                    continue
                image.verify()
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
            continue
        return BytesIO(data), f"youtube-thumbnail-{video_id}.jpg"
    raise ThumbnailError("YouTube did not provide an accessible thumbnail for this video.")
