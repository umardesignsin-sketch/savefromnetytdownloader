"""Retrieve public YouTube caption tracks without downloading media files."""

import html
import json
import re
import tempfile
from pathlib import Path

from extractors.detect import DetectError, detect_url
from extractors.service import AnalysisError, _run, _safe_text


LANGUAGE = re.compile(r"^[A-Za-z0-9-]{2,20}$")
CUE_TIME = re.compile(r"^(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})$")
MAX_CAPTION_BYTES = 1_000_000
MAX_SEGMENTS = 6_000


def _timestamp_ms(value):
    match = CUE_TIME.fullmatch(value.strip())
    if not match:
        return None
    hours, minutes, seconds, millis = match.groups()
    return ((int(hours or 0) * 3600 + int(minutes) * 60 + int(seconds)) * 1000
            + int(millis))


def parse_vtt(source):
    """Keep only caption cues; discard WebVTT headers, styling and HTML tags."""
    segments = []
    for block in re.split(r"\n\s*\n", source.replace("\r\n", "\n").lstrip("\ufeff")):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        timing = next((index for index, line in enumerate(lines[:2]) if " --> " in line), None)
        if timing is None:
            continue
        start_raw, end_raw = lines[timing].split(" --> ", 1)
        start = _timestamp_ms(start_raw)
        end = _timestamp_ms(end_raw.split()[0])
        if start is None or end is None or end <= start:
            continue
        content = " ".join(lines[timing + 1:])
        content = html.unescape(re.sub(r"<[^>]*>", "", content))
        content = " ".join(content.split())
        if not content:
            continue
        if segments and segments[-1]["text"] == content and start <= segments[-1]["end_ms"]:
            segments[-1]["end_ms"] = max(end, segments[-1]["end_ms"])
            continue
        segments.append({"start_ms": start, "end_ms": end, "text": content})
        if len(segments) > MAX_SEGMENTS:
            raise AnalysisError("This transcript is too long to display here.", "too_large")
    if not segments:
        raise AnalysisError("This video has no readable public caption cues.", "no_captions")
    return segments


def _tracks(info):
    choices = {}
    for kind, field in (("manual", "subtitles"), ("automatic", "automatic_captions")):
        for code, formats in (info.get(field) or {}).items():
            if (LANGUAGE.fullmatch(code) and isinstance(formats, list)
                    and any(item.get("ext") == "vtt" for item in formats if isinstance(item, dict))):
                choices.setdefault(code, kind)
    return choices


def _choose_language(choices, requested):
    if requested:
        if not LANGUAGE.fullmatch(requested) or requested not in choices:
            raise AnalysisError("That caption language is not available for this video.", "invalid_language")
        return requested
    for code in ("en", "en-US", "en-GB"):
        if code in choices and choices[code] == "manual":
            return code
    manual = sorted(code for code, kind in choices.items() if kind == "manual")
    if manual:
        return manual[0]
    for code in ("en", "en-US", "en-GB"):
        if code in choices:
            return code
    return sorted(choices)[0]


def get_transcript(raw_url, requested_language=None):
    """Return bounded caption cues from a single allowlisted public video."""
    detection = detect_url(raw_url)
    if detection.platform != "youtube" or detection.content_type not in ("video", "short"):
        raise DetectError("Paste a direct YouTube video or Shorts URL.")
    if requested_language is not None and (not isinstance(requested_language, str)
                                           or not LANGUAGE.fullmatch(requested_language)):
        raise AnalysisError("Choose a valid caption language.", "invalid_language")

    url = detection.normalized_url
    info_text = _run([
        "yt-dlp", "--ignore-config", "--no-playlist", "--skip-download",
        "--dump-single-json", "--no-warnings", "--use-extractors", "default,-generic",
        "--js-runtimes", "node", "--", url,
    ], timeout=40)
    try:
        info = json.loads(info_text)
    except (TypeError, ValueError) as exc:
        raise AnalysisError("YouTube returned unreadable caption details.", "source_unavailable") from exc
    if info.get("is_live") or info.get("live_status") in ("is_live", "is_upcoming"):
        raise AnalysisError("Live streams are unavailable until captions are published.", "live")
    if info.get("_type") in ("playlist", "multi_video"):
        raise AnalysisError("Use a link to one video instead of a playlist.", "unsupported")
    choices = _tracks(info)
    if not choices:
        raise AnalysisError("No public captions were found for this video. This tool does not transcribe audio without captions.", "no_captions")
    language = _choose_language(choices, requested_language)

    with tempfile.TemporaryDirectory(prefix="sfn-transcript-") as directory:
        output = str(Path(directory) / "captions.%(ext)s")
        _run([
            "yt-dlp", "--ignore-config", "--no-playlist", "--skip-download",
            "--write-subs", "--write-auto-subs", "--sub-langs", f"^{re.escape(language)}$",
            "--sub-format", "vtt", "--no-warnings", "--no-progress",
            "--use-extractors", "default,-generic", "--js-runtimes", "node",
            "--output", output, "--", url,
        ], timeout=45)
        caption = Path(directory) / f"captions.{language}.vtt"
        if not caption.is_file():
            raise AnalysisError("The caption track could not be retrieved. Try another available language.", "source_unavailable")
        if caption.stat().st_size > MAX_CAPTION_BYTES:
            raise AnalysisError("This caption track is too large to display here.", "too_large")
        segments = parse_vtt(caption.read_text(encoding="utf-8-sig", errors="replace"))

    available = [{"code": code, "kind": kind} for code, kind in sorted(
        choices.items(), key=lambda item: (item[1] != "manual", item[0]))]
    return {
        "platform": "youtube", "url": url,
        "title": _safe_text(info.get("title") or "YouTube video"),
        "author": _safe_text(info.get("uploader") or info.get("channel")),
        "duration": info.get("duration") if isinstance(info.get("duration"), (int, float)) else None,
        "language": language, "kind": choices[language], "languages": available,
        "segments": segments,
    }
