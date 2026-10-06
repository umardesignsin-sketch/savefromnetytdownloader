"""Job runner: wraps yt-dlp in a subprocess and tracks progress in memory."""
import os
import ipaddress
import logging
import re
import shutil
import signal
import socket
import subprocess
import threading
import time
import uuid
from urllib.parse import urlsplit

from config import (
    DOWNLOAD_DIR,
    JOB_TIMEOUT,
    JOB_TTL,
    MAX_CONCURRENT_JOBS,
    MAX_FILESIZE,
    YTDLP_BIN,
)
import db

# job_id -> {status, percent, speed, eta, stage, title, filename, error}
JOBS = {}
_lock = threading.Lock()
_slots = threading.BoundedSemaphore(MAX_CONCURRENT_JOBS)

# yt-dlp progress line, e.g.
# [download]  42.7% of ~103.55MiB at  4.21MiB/s ETA 00:14
_PROGRESS = re.compile(
    r"\[download\]\s+(?P<pct>\d{1,3}(?:\.\d+)?)%"
    r"(?:\s+of\s+~?\s*(?P<total>[\d.]+\w+))?"
    r"(?:\s+at\s+(?P<speed>[\d.]+\w+/s|Unknown\s+\w+))?"
    r"(?:\s+ETA\s+(?P<eta>[\d:]+|Unknown))?"
)
_TITLE = re.compile(r"^__TITLE__ (.*)$")

QUALITIES = {
    "best": ["-f", "bv*+ba/b", "--merge-output-format", "mp4"],
    "1080p": ["-f", "bv*[height<=1080]+ba/b[height<=1080]", "--merge-output-format", "mp4"],
    "720p": ["-f", "bv*[height<=720]+ba/b[height<=720]", "--merge-output-format", "mp4"],
    "480p": ["-f", "bv*[height<=480]+ba/b[height<=480]", "--merge-output-format", "mp4"],
    "audio": ["-f", "ba/b", "-x", "--audio-format", "mp3"],
}

# Map raw yt-dlp stderr to something a human can act on.
_ERROR_HINTS = [
    ("private video", "This video is private."),
    ("members-only", "This video is for channel members only."),
    ("video unavailable", "This video is unavailable or has been removed."),
    ("has been removed", "This video has been removed."),
    ("account associated with this video has been terminated",
     "The uploader's account was terminated."),
    ("confirm your age", "This video is age-restricted and cannot be downloaded anonymously."),
    ("age-restricted", "This video is age-restricted and cannot be downloaded anonymously."),
    ("sign in to confirm", "YouTube is asking this server to sign in (bot check or age gate)."),
    ("not available in your country", "This video is geo-blocked for this server's region."),
    ("is not a valid url", "That doesn't look like a valid video URL."),
    ("unsupported url", "That URL isn't supported."),
    ("requested format is not available",
     "The selected quality isn't available for this video. Try 'best'."),
    ("live event will begin", "This is an upcoming live stream and hasn't started yet."),
]


def friendly_error(stderr):
    low = (stderr or "").lower()
    for needle, message in _ERROR_HINTS:
        if needle in low:
            return message
    # Fall back to the last ERROR: line yt-dlp emitted.
    for line in reversed((stderr or "").splitlines()):
        if line.strip().startswith("ERROR:"):
            return line.strip()[6:].strip() or "Download failed."
    return "Download failed. Check the URL and try again."


def _set(job_id, **fields):
    with _lock:
        if job_id in JOBS:
            JOBS[job_id].update(fields)


def get_state(job_id):
    with _lock:
        state = JOBS.get(job_id)
        return dict(state) if state else None


def _reap():
    """Drop finished jobs older than JOB_TTL from the in-memory map."""
    now = time.time()
    with _lock:
        expired = [
            j for j, s in JOBS.items()
            if s.get("ended_at") and now - s["ended_at"] > JOB_TTL
        ]
        for jid in expired:
            JOBS.pop(jid, None)
    for jid in expired:
        remove_files(jid)


def active_count():
    with _lock:
        return sum(s["status"] in ("queued", "downloading") for s in JOBS.values())


def start(url, quality, owner_id, spec=None, platform="", tool_slug=""):
    if spec is None and quality not in QUALITIES:
        raise ValueError("Unknown quality option.")
    _reap()
    job_id = uuid.uuid4().hex
    with _lock:
        if sum(s["status"] in ("queued", "downloading") for s in JOBS.values()) >= MAX_CONCURRENT_JOBS:
            return None
        JOBS[job_id] = {
            "job_id": job_id,
            "url": url,
            "quality": quality,
            "spec": spec,
            "status": "queued",
            "percent": 0.0,
            "stage": "Queued",
            "speed": None,
            "eta": None,
            "title": None,
            "filename": None,
            "error": None,
            "ended_at": None,
        }
    db.insert_job(job_id, url, quality, owner_id, platform, tool_slug,
                  spec.get("extension", "") if spec else "")
    threading.Thread(target=_run, args=(job_id, url, quality, spec), daemon=True).start()
    return job_id


def _job_dir(job_id):
    return os.path.join(DOWNLOAD_DIR, job_id)


def _run(job_id, url, quality, spec):
    acquired = _slots.acquire(timeout=JOB_TIMEOUT)
    if not acquired:
        _fail(job_id, "Server is busy — too many downloads in progress. Try again shortly.")
        return
    try:
        _download(job_id, url, quality, spec)
    except Exception:  # noqa: BLE001 - keep unexpected details in server logs
        logging.exception("Download job failed")
        _fail(job_id, "A server error interrupted this download. Please try again.")
    finally:
        _slots.release()


def _download(job_id, url, quality, spec=None):
    out_dir = _job_dir(job_id)
    os.makedirs(out_dir, exist_ok=True)

    if spec and spec.get("engine") == "threads":
        return _download_threads(job_id, spec, out_dir)

    if spec and spec.get("engine") == "gallery-dl":
        index = spec["index"]
        cmd = ["gallery-dl", "--config-ignore", "--no-input", "--filesize-max", MAX_FILESIZE,
               "--range", f"{index}-{index}", "--directory", out_dir, "--", url]
    else:
        options = QUALITIES[quality] if spec is None else ["-f", spec["selector"]]
        if spec and spec.get("convert_mp3"):
            options += ["-x", "--audio-format", "mp3"]
        elif spec and spec.get("extension") in ("mp4", "webm"):
            options += ["--merge-output-format", spec["extension"]]

        cmd = [
        YTDLP_BIN,
        "--ignore-config",
        "--use-extractors", "default,-generic",
        "--newline",                 # one progress update per line
        "--no-playlist",
        "--max-filesize", MAX_FILESIZE,
        "--js-runtimes", "node",
        "--no-color",
        "--restrict-filenames",
        "--no-warnings",
        "--progress",
        "--print", "before_dl:__TITLE__ %(title)s",
        "-o", os.path.join(out_dir, "%(title)s.%(ext)s"),
        *options,
        "--",
        url,
        ]

    _set(job_id, status="downloading", stage="Starting")
    db.update_job(job_id, status="downloading")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        # New process group so a timeout kills ffmpeg children too (POSIX).
        start_new_session=(os.name != "nt"),
    )

    stderr_lines = []

    def drain_stderr():
        for line in proc.stderr:
            stderr_lines.append(line.rstrip())

    err_thread = threading.Thread(target=drain_stderr, daemon=True)
    err_thread.start()

    deadline = time.time() + JOB_TIMEOUT
    timed_out = threading.Event()

    def on_timeout():
        timed_out.set()
        _kill(proc)

    watchdog = threading.Timer(JOB_TIMEOUT, on_timeout)
    watchdog.daemon = True
    watchdog.start()
    for line in proc.stdout:
        line = line.strip()
        if time.time() > deadline:
            _kill(proc)
            _fail(job_id, "Download timed out.")
            return

        title = _TITLE.match(line)
        if title:
            name = title.group(1).strip()
            _set(job_id, title=name)
            db.update_job(job_id, title=name)
            continue

        m = _PROGRESS.search(line)
        if m:
            pct = float(m.group("pct"))
            _set(
                job_id,
                percent=pct,
                speed=m.group("speed"),
                eta=m.group("eta"),
                stage="Downloading",
            )
            continue

        if line.startswith("[Merger]") or line.startswith("[VideoConvertor]"):
            _set(job_id, stage="Merging", percent=99.0)
        elif line.startswith("[ExtractAudio]"):
            _set(job_id, stage="Extracting audio", percent=99.0)

    proc.wait()
    watchdog.cancel()
    err_thread.join(timeout=5)
    stderr = "\n".join(stderr_lines)

    if timed_out.is_set():
        _fail(job_id, "Download timed out. Please try a shorter or smaller video.")
        return

    if proc.returncode != 0:
        _fail(job_id, friendly_error(stderr))
        return

    files = [os.path.join(root, f) for root, _, names in os.walk(out_dir)
             for f in names if not f.endswith((".part", ".ytdl"))]
    if not files:
        _fail(job_id, friendly_error(stderr))
        return

    # A merge can leave fragments behind; the finished file is the largest one.
    selected = max(files, key=os.path.getsize)
    filename = os.path.relpath(selected, out_dir)
    size = os.path.getsize(selected)
    if size > 512 * 1024 * 1024:
        return _fail(job_id, "The finished file exceeds the 512 MB limit.")

    _set(
        job_id,
        status="done",
        percent=100.0,
        stage="Complete",
        filename=filename,
        ended_at=time.time(),
    )
    db.finish_job(job_id, "done", filename=filename, filesize=size)


def _download_threads(job_id, spec, out_dir):
    import requests
    media_url = spec["media_url"]
    host = (urlsplit(media_url).hostname or "").lower()
    if not (host.endswith(".cdninstagram.com") or host.endswith(".fbcdn.net")):
        return _fail(job_id, "The source video URL is unavailable.")
    response = None
    try:
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            return _fail(job_id, "The source video address is invalid.")
        response = requests.get(media_url, stream=True, timeout=(8, 30), allow_redirects=False)
        if response.status_code != 200:
            return _fail(job_id, "The source video is no longer available.")
        if not response.headers.get("Content-Type", "").lower().startswith("video/mp4"):
            return _fail(job_id, "The source did not return an MP4 video.")
        path = os.path.join(out_dir, "threads-video.mp4")
        total = 0
        deadline = time.monotonic() + JOB_TIMEOUT
        with open(path, "wb") as output:
            for chunk in response.iter_content(128 * 1024):
                if time.monotonic() > deadline:
                    return _fail(job_id, "Download timed out.")
                total += len(chunk)
                if total > 512 * 1024 * 1024:
                    return _fail(job_id, "The file exceeds the 512 MB limit.")
                output.write(chunk)
        if not total:
            return _fail(job_id, "The source returned an empty video.")
        _set(job_id, status="done", percent=100.0, stage="Complete", filename="threads-video.mp4", ended_at=time.time())
        db.finish_job(job_id, "done", filename="threads-video.mp4", filesize=total)
    except (OSError, requests.RequestException):
        _fail(job_id, "The source video could not be transferred.")
    finally:
        if response is not None:
            response.close()


def _kill(proc):
    try:
        if os.name != "nt":
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        else:
            proc.kill()
    except Exception:
        pass


def _fail(job_id, message):
    _set(job_id, status="error", error=message, stage="Failed", ended_at=time.time())
    db.finish_job(job_id, "error", error=message)
    shutil.rmtree(_job_dir(job_id), ignore_errors=True)


def file_path(job_id, filename):
    """Resolve a stored file, refusing anything outside its own job directory."""
    base = os.path.realpath(_job_dir(job_id))
    target = os.path.realpath(os.path.join(base, filename))
    if os.path.commonpath([base, target]) != base or not os.path.isfile(target):
        return None
    return target


def remove_files(job_id):
    shutil.rmtree(_job_dir(job_id), ignore_errors=True)


def ytdlp_available():
    return shutil.which(YTDLP_BIN) is not None or os.path.isfile(YTDLP_BIN)
