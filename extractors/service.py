"""Analyze supported public URLs and expose only real extractor formats."""

import html
import copy
import json
import re
import subprocess
import threading
import time
import uuid
from urllib.parse import urlsplit

from .detect import detect_url


class AnalysisError(Exception):
    def __init__(self, message, code="source_unavailable"):
        super().__init__(message)
        self.code = code


_cache = {}
_metadata_cache = {}
_lock = threading.Lock()
CACHE_TTL = 600
MAX_BYTES = 512 * 1024 * 1024


def friendly_error(raw):
    low = (raw or "").lower()
    for needle, code, message in (
        ("private", "private", "This post is private. Only public media can be downloaded."),
        ("login required", "private", "This post requires sign-in and is unavailable here."),
        ("sign in", "restricted", "This source requires sign-in and is unavailable here."),
        ("age-restricted", "restricted", "Age-restricted media is unavailable here."),
        ("not available in your country", "region_restricted", "This media is unavailable in the server's region."),
        ("geo restricted", "region_restricted", "This media is unavailable in the server's region."),
        ("not found", "deleted", "This post was removed or could not be found."),
        ("404", "deleted", "This post was removed or could not be found."),
        ("live", "live", "Live streams cannot be processed while they are running."),
        ("unsupported url", "unsupported", "This URL is not supported by the source extractor."),
    ):
        if needle in low:
            return AnalysisError(message, code)
    return AnalysisError("Couldn't process this media. It may be unavailable, restricted, or unsupported.")


def _run(command, timeout=35):
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout,
                              check=False, encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired as exc:
        raise AnalysisError("The source took too long to respond. Please try again.", "timeout") from exc
    except OSError as exc:
        raise AnalysisError("The media extractor is unavailable on this server.", "server_error") from exc
    if proc.returncode:
        raise friendly_error(proc.stderr)
    if len(proc.stdout) > 4_000_000:
        raise AnalysisError("This post contains too many items to process.", "too_large")
    return proc.stdout


def _safe_text(value, limit=180):
    return re.sub(r"[\x00-\x1f\x7f]", "", str(value or "")).strip()[:limit]


def _estimate(item):
    size = item.get("filesize") or item.get("filesize_approx")
    return int(size) if isinstance(size, (int, float)) and size > 0 else None


def _yt_formats(info):
    formats = info.get("formats") or []
    audio = [f for f in formats if f.get("acodec") not in (None, "none") and
             f.get("vcodec") in (None, "none") and f.get("format_id")]
    audio.sort(key=lambda f: (f.get("abr") or 0, _estimate(f) or 0), reverse=True)
    result = []
    seen = set()
    for f in sorted(formats, key=lambda x: (x.get("height") or 0, x.get("tbr") or 0), reverse=True):
        if f.get("vcodec") in (None, "none") or f.get("ext") not in ("mp4", "webm") or not f.get("format_id"):
            continue
        height = f.get("height")
        if not height or height > 2160:
            continue
        key = (f["ext"], height)
        if key in seen:
            continue
        has_audio = f.get("acodec") not in (None, "none")
        partner = None if has_audio else next((a for a in audio if a.get("ext") == ("m4a" if f["ext"] == "mp4" else "webm")), None)
        if not has_audio and not partner:
            continue
        size = (_estimate(f) or 0) + (_estimate(partner) or 0) if partner else _estimate(f)
        if size and size > MAX_BYTES:
            continue
        seen.add(key)
        selector = f["format_id"] + ("+" + partner["format_id"] if partner else "")
        result.append({"id": f"v{len(result)}", "type": "video", "extension": f["ext"],
                       "quality": f"{height}p", "resolution": [f.get("width"), height],
                       "bitrate": int(f["tbr"]) if f.get("tbr") else None,
                       "filesize": size or None,
                       "_spec": {"engine": "yt-dlp", "selector": selector, "extension": f["ext"]}})
        if len(result) >= 12:
            break
    if audio or any(f.get("acodec") not in (None, "none") for f in formats):
        best = audio[0] if audio else next(f for f in formats if f.get("acodec") not in (None, "none"))
        audio_selector = str(best["format_id"])
        if best.get("ext") in ("m4a", "mp3", "webm") and _estimate(best) != 0:
            ext = best["ext"]
            result.append({"id": "a-source", "type": "audio", "extension": ext,
                           "quality": "Original audio", "resolution": None,
                           "bitrate": int(best["abr"]) if best.get("abr") else None,
                           "filesize": _estimate(best),
                           "_spec": {"engine": "yt-dlp", "selector": audio_selector, "extension": ext}})
        result.append({"id": "a-mp3", "type": "audio", "extension": "mp3",
                       "quality": "Converted MP3", "resolution": None, "bitrate": None,
                       "filesize": None,
                       "_spec": {"engine": "yt-dlp", "selector": audio_selector,
                                 "extension": "mp3", "convert_mp3": True}})
    return result


def _yt_analyze(detection):
    output = _run(["yt-dlp", "--ignore-config", "--no-playlist", "--skip-download",
                   "--dump-single-json", "--no-warnings", "--no-overwrites",
                   "--use-extractors", "default,-generic", "--js-runtimes", "node",
                   "--", detection.normalized_url])
    try:
        info = json.loads(output)
    except (ValueError, TypeError) as exc:
        raise AnalysisError("The source returned unreadable media details.") from exc
    if info.get("is_live") or info.get("live_status") in ("is_live", "is_upcoming"):
        raise AnalysisError("Live streams cannot be processed while they are running.", "live")
    if info.get("_type") in ("playlist", "multi_video"):
        raise AnalysisError("Use a link to one video or post instead of a playlist.", "unsupported")
    result = _yt_formats(info)
    if not result:
        raise AnalysisError("No downloadable public formats were returned for this media.", "no_formats")
    return {"platform": detection.platform, "type": detection.content_type,
            "title": _safe_text(info.get("title") or "Untitled media"),
            "author": _safe_text(info.get("uploader") or info.get("channel") or info.get("creator")),
            "thumbnail": info.get("thumbnail") if str(info.get("thumbnail", "")).startswith("https://") else None,
            "duration": info.get("duration"), "formats": result}


def _gallery_analyze(detection):
    output = _run(["gallery-dl", "--config-ignore", "--no-input", "--dump-json",
                   "--range", "1-12", "--", detection.normalized_url], timeout=35)
    try:
        messages = json.loads(output)
    except (ValueError, TypeError) as exc:
        raise AnalysisError("The source returned unreadable media details.") from exc
    if not isinstance(messages, list):
        raise AnalysisError("No public media was returned for this post.", "no_formats")
    media = [m for m in messages if isinstance(m, list) and len(m) >= 3 and m[0] == 3 and isinstance(m[2], dict)]
    result = []
    for index, item in enumerate(media[:12], start=1):
        meta = item[2]
        ext = str(meta.get("extension") or "").lower().lstrip(".")
        if ext not in ("jpg", "jpeg", "png", "webp", "gif", "mp4", "webm"):
            continue
        kind = "video" if ext in ("mp4", "webm") else "image"
        result.append({"id": f"g{index}", "type": kind, "extension": ext,
                       "quality": f"Item {index} · original", "resolution": None,
                       "bitrate": None, "filesize": None,
                       "_spec": {"engine": "gallery-dl", "index": index, "extension": ext}})
    if not result:
        raise AnalysisError("No accessible public images or videos were found in this post.", "no_formats")
    first = media[0][2]
    return {"platform": detection.platform, "type": detection.content_type,
            "title": _safe_text(first.get("description") or first.get("title") or f"{detection.platform.title()} media"),
            "author": _safe_text(first.get("username") or first.get("user") or first.get("owner")),
            "thumbnail": None, "duration": None, "formats": result}


def _threads_analyze(detection):
    # Threads has no stable yt-dlp extractor. Public pages sometimes expose an
    # Open Graph video; use it only when served by Meta's media CDN.
    import requests
    try:
        with requests.get(detection.normalized_url, timeout=(5, 12), allow_redirects=False, stream=True,
                          headers={"User-Agent": "Mozilla/5.0 (compatible; SaveFromNet/1.0)"}) as response:
            length = response.headers.get("Content-Length", "0")
            if response.status_code != 200 or (length.isdigit() and int(length) > 2_000_000):
                raise AnalysisError("This Threads post is unavailable or requires sign-in.", "source_unavailable")
            chunks = []
            total = 0
            for chunk in response.iter_content(64 * 1024):
                total += len(chunk)
                if total > 2_000_000:
                    raise AnalysisError("This Threads page is too large to inspect.", "too_large")
                chunks.append(chunk)
            page_html = b"".join(chunks).decode("utf-8", "replace")
    except requests.RequestException as exc:
        raise AnalysisError("This Threads post is unavailable right now.", "source_unavailable") from exc
    tags = {}
    for tag in re.findall(r"<meta\b[^>]*>", page_html, re.I):
        attrs = dict((k.lower(), html.unescape(v)) for k, v in re.findall(r'(property|name|content)=["\']([^"\']+)["\']', tag, re.I))
        if attrs.get("property") and attrs.get("content"):
            tags[attrs["property"]] = attrs["content"]
    media_url = tags.get("og:video:secure_url") or tags.get("og:video")
    host = (urlsplit(media_url).hostname or "").lower() if media_url else ""
    if not (media_url and media_url.startswith("https://") and
            (host.endswith(".cdninstagram.com") or host.endswith(".fbcdn.net"))):
        raise AnalysisError("No public video was exposed for this Threads post.", "no_formats")
    return {"platform": "threads", "type": "post", "title": _safe_text(tags.get("og:title") or "Threads video"),
            "author": "", "thumbnail": tags.get("og:image"), "duration": None,
            "formats": [{"id": "t-video", "type": "video", "extension": "mp4", "quality": "Source video",
                         "resolution": None, "bitrate": None, "filesize": None,
                         "_spec": {"engine": "threads", "media_url": media_url, "extension": "mp4"}}]}


def analyze(raw_url, owner_id):
    detection = detect_url(raw_url)
    with _lock:
        cached = _metadata_cache.get(detection.normalized_url)
        result = copy.deepcopy(cached["result"]) if cached and cached["expires"] > time.time() else None
    if result is None:
        if detection.extractor == "gallery-dl":
            try:
                result = _gallery_analyze(detection)
            except AnalysisError:
                if detection.platform == "pinterest":
                    result = _yt_analyze(detection)
                else:
                    raise
        elif detection.extractor == "threads":
            result = _threads_analyze(detection)
        else:
            result = _yt_analyze(detection)
        with _lock:
            _metadata_cache[detection.normalized_url] = {"result": copy.deepcopy(result), "expires": time.time() + 90}
    token = uuid.uuid4().hex
    specs = {}
    for item in result["formats"]:
        spec = item.pop("_spec")
        spec["label"] = f"{item['extension'].upper()} {item['quality']}"
        specs[item["id"]] = spec
    with _lock:
        now = time.time()
        for key in list(_cache):
            if _cache[key]["expires"] < now:
                del _cache[key]
        for key in list(_metadata_cache):
            if _metadata_cache[key]["expires"] < now:
                del _metadata_cache[key]
        _cache[token] = {"owner": owner_id, "url": detection.normalized_url,
                         "detection": detection, "specs": specs, "expires": now + CACHE_TTL}
    result["analysis_id"] = token
    result["detected"] = detection.as_dict()
    return result


def resolve(analysis_id, format_id, owner_id):
    with _lock:
        item = _cache.get(analysis_id)
    if not item or item["expires"] < time.time() or item["owner"] != owner_id:
        raise AnalysisError("Analysis expired. Paste the URL again to refresh formats.", "expired")
    spec = item["specs"].get(format_id)
    if not spec:
        raise AnalysisError("That format was not returned by the source.", "invalid_format")
    return item["url"], item["detection"], spec
