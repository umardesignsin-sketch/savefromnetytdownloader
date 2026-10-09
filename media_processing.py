"""Bounded ffmpeg processing for files supplied by the visitor."""

from io import BytesIO
import json
import math
from pathlib import Path
import subprocess
import tempfile


MAX_UPLOAD = 16 * 1024 * 1024
MAX_OUTPUT = 24 * 1024 * 1024
INPUT_EXTENSIONS = {
    "video-to-gif": {".mp4", ".webm", ".mov"},
    "mp4-to-mp3": {".mp4"},
    "video-trimmer": {".mp4", ".webm", ".mov"},
    "audio-cutter": {".mp3", ".m4a", ".wav"},
}
FORMATS = {
    ".mp4": {"mov", "mp4", "m4a", "3gp", "3g2", "mj2"},
    ".mov": {"mov", "mp4", "m4a", "3gp", "3g2", "mj2"},
    ".m4a": {"mov", "mp4", "m4a", "3gp", "3g2", "mj2"},
    ".webm": {"matroska", "webm"},
    ".mp3": {"mp3"},
    ".wav": {"wav"},
}
OUTPUTS = {
    "video-to-gif": ("savefromnet-clip.gif", "image/gif"),
    "mp4-to-mp3": ("savefromnet-audio.mp3", "audio/mpeg"),
    "video-trimmer": ("savefromnet-trimmed.mp4", "video/mp4"),
    "audio-cutter": ("savefromnet-cut.mp3", "audio/mpeg"),
}


class MediaProcessError(ValueError):
    pass


def _seconds(value, label):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise MediaProcessError(f"Enter a valid {label} in seconds.") from None
    if not math.isfinite(number) or number < 0:
        raise MediaProcessError(f"Enter a valid {label} in seconds.")
    return number


def process_media(upload, slug, start_value=None, end_value=None):
    if slug not in INPUT_EXTENSIONS:
        raise MediaProcessError("Choose a supported media tool.")
    suffix = Path(upload.filename or "").suffix.lower()
    if suffix not in INPUT_EXTENSIONS[slug]:
        raise MediaProcessError("Choose a supported file type for this tool.")
    data = upload.stream.read(MAX_UPLOAD + 1)
    if not data or len(data) > MAX_UPLOAD:
        raise MediaProcessError("Choose a nonempty file no larger than 16 MB.")

    with tempfile.TemporaryDirectory(prefix="sfn-media-") as directory:
        source = Path(directory) / ("source" + suffix)
        filename, mime = OUTPUTS[slug]
        target = Path(directory) / filename
        source.write_bytes(data)
        try:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-show_entries",
                 "format=format_name,duration:stream=codec_type,width,height", "-of", "json", str(source)],
                capture_output=True, timeout=10, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise MediaProcessError("Media inspection is temporarily unavailable.") from exc
        if probe.returncode or len(probe.stdout) > 64 * 1024:
            raise MediaProcessError("This file could not be decoded. Choose a valid media file.")
        try:
            info = json.loads(probe.stdout)
            format_names = set(info["format"]["format_name"].split(","))
            duration = float(info["format"]["duration"])
            streams = {stream.get("codec_type") for stream in info.get("streams", ())}
        except (KeyError, ValueError, TypeError, AttributeError) as exc:
            raise MediaProcessError("This file does not have a readable duration.") from exc
        if not format_names.intersection(FORMATS[suffix]) or not math.isfinite(duration) or duration <= 0:
            raise MediaProcessError("The file content does not match a supported media format.")
        needs_video = slug in {"video-to-gif", "video-trimmer", "mp4-to-mp3"}
        if (needs_video and "video" not in streams) or (slug in {"mp4-to-mp3", "audio-cutter"} and "audio" not in streams):
            raise MediaProcessError("This file does not contain the video or audio track this tool needs.")
        if slug in {"video-to-gif", "video-trimmer"}:
            video = next((stream for stream in info["streams"] if stream.get("codec_type") == "video"), {})
            try:
                width, height = int(video.get("width") or 0), int(video.get("height") or 0)
            except (TypeError, ValueError):
                raise MediaProcessError("The video dimensions could not be read.") from None
            if width < 1 or height < 1 or width > 1920 or height > 1920 or width * height > 2_100_000:
                raise MediaProcessError("This tool accepts source video up to 1080p. Resize a larger clip first.")
        max_duration = 600 if slug in {"mp4-to-mp3", "audio-cutter"} else 180
        if duration > max_duration:
            raise MediaProcessError(f"This tool accepts media up to {max_duration} seconds long.")

        command = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-threads", "2", "-y",
                   "-protocol_whitelist", "file,pipe", "-i", str(source)]
        if slug == "video-to-gif":
            start = _seconds(start_value or 0, "start time")
            length = _seconds(end_value or 3, "clip length")
            if length <= 0 or length > 10 or start + length > duration + 0.05:
                raise MediaProcessError("Choose a clip of 1 to 10 seconds within the source video.")
            command += ["-ss", str(start), "-t", str(length), "-an",
                        "-vf", "fps=10,scale='min(480,iw)':-2:flags=lanczos", str(target)]
        elif slug in {"video-trimmer", "audio-cutter"}:
            start = _seconds(start_value, "start time")
            end = _seconds(end_value, "end time")
            limit = 60 if slug == "video-trimmer" else 120
            if end <= start or end - start > limit or end > duration + 0.05:
                raise MediaProcessError(f"Choose a segment within the file, no longer than {limit} seconds.")
            command += ["-ss", str(start), "-t", str(end - start)]
            if slug == "video-trimmer":
                command += ["-map", "0:v:0", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "25", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(target)]
            else:
                command += ["-vn", "-c:a", "libmp3lame", "-q:a", "4", str(target)]
        else:
            command += ["-vn", "-c:a", "libmp3lame", "-q:a", "4", str(target)]
        try:
            encoded = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                     timeout=50, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise MediaProcessError("Processing timed out. Try a shorter or smaller file.") from exc
        if encoded.returncode or not target.exists() or not target.stat().st_size:
            raise MediaProcessError("The media could not be processed. Try a different valid file.")
        if target.stat().st_size > MAX_OUTPUT:
            raise MediaProcessError("The result exceeds 24 MB. Choose a shorter segment.")
        output = BytesIO(target.read_bytes())
        return output, filename, mime, {"input_bytes": len(data), "output_bytes": output.getbuffer().nbytes}
