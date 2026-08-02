"""Job runner: wraps yt-dlp in a subprocess and tracks progress in memory."""
import os
import re
import shutil
import signal
import subprocess
import threading
import time
import uuid

from config import (
    COOKIES_FILE,
    DOWNLOAD_DIR,
    JOB_TIMEOUT,
    JOB_TTL,
    MAX_CONCURRENT_JOBS,
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


# YouTube's web client formats can include codecs (e.g. IAMF audio) that
# yt-dlp's format matcher doesn't yet recognize, making bv*+ba impossible to
# satisfy even though compatible formats exist. Forcing the Android/iOS
# player clients sidesteps this — they serve the older, universally-supported
# codec set. See yt-dlp issue tracker for "Unknown codec iamf" reports.
_CLIENT_ARGS = ["--extractor-args", "youtube:player_client=android,ios,web"]

QUALITIES = {
    "best": [*_CLIENT_ARGS, "-f", "bv*+ba/b", "--merge-output-format", "mp4"],
    "1080p": [*_CLIENT_ARGS, "-f", "bv*[height<=1080]+ba/b[height<=1080]", "--merge-output-format", "mp4"],
    "720p": [*_CLIENT_ARGS, "-f", "bv*[height<=720]+ba/b[height<=720]", "--merge-output-format", "mp4"],
    "480p": [*_CLIENT_ARGS, "-f", "bv*[height<=480]+ba/b[height<=480]", "--merge-output-format", "mp4"],
    "audio": [*_CLIENT_ARGS, "-f", "ba/b", "-x", "--audio-format", "mp3"],
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
        for jid in [
            j for j, s in JOBS.items()
            if s.get("ended_at") and now - s["ended_at"] > JOB_TTL
        ]:
            JOBS.pop(jid, None)


def start(url, quality):
    if quality not in QUALITIES:
        raise ValueError("Unknown quality option.")
    _reap()
    job_id = uuid.uuid4().hex
    with _lock:
        JOBS[job_id] = {
            "job_id": job_id,
            "url": url,
            "quality": quality,
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
    db.insert_job(job_id, url, quality)
    threading.Thread(target=_run, args=(job_id, url, quality), daemon=True).start()
    return job_id


def _job_dir(job_id):
    return os.path.join(DOWNLOAD_DIR, job_id)


def _run(job_id, url, quality):
    acquired = _slots.acquire(timeout=JOB_TIMEOUT)
    if not acquired:
        _fail(job_id, "Server is busy — too many downloads in progress. Try again shortly.")
        return
    try:
        _download(job_id, url, quality)
    except Exception as exc:  # noqa: BLE001 - surface anything unexpected to the user
        _fail(job_id, f"Unexpected server error: {exc}")
    finally:
        _slots.release()


def _download(job_id, url, quality):
    out_dir = _job_dir(job_id)
    os.makedirs(out_dir, exist_ok=True)

    # yt-dlp writes updated session cookies back to this file on exit, but
    # Render (and similar platforms) mount secret files read-only, which
    # crashes the whole process. Give it a writable per-job copy instead.
    cookies_arg = []
    if COOKIES_FILE and os.path.isfile(COOKIES_FILE):
        job_cookies = os.path.join(out_dir, "cookies.txt")
        shutil.copyfile(COOKIES_FILE, job_cookies)
        cookies_arg = ["--cookies", job_cookies]

    cmd = [
        YTDLP_BIN,
        "--newline",                 # one progress update per line
        "--no-playlist",
        "--no-color",
        "--restrict-filenames",
        "--no-warnings",
        "--progress",
        "--print", "before_dl:__TITLE__ %(title)s",
        "-o", os.path.join(out_dir, "%(title)s.%(ext)s"),
        *cookies_arg,
        *QUALITIES[quality],
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
    err_thread.join(timeout=5)
    stderr = "\n".join(stderr_lines)

    if proc.returncode != 0:
        print(f"[yt-dlp:{job_id}] exit {proc.returncode}\n{stderr}", flush=True)
        _fail(job_id, friendly_error(stderr))
        return

    files = [
        f for f in os.listdir(out_dir)
        if os.path.isfile(os.path.join(out_dir, f)) and not f.endswith(".part")
    ]
    if not files:
        _fail(job_id, friendly_error(stderr))
        return

    # A merge can leave fragments behind; the finished file is the largest one.
    filename = max(files, key=lambda f: os.path.getsize(os.path.join(out_dir, f)))
    size = os.path.getsize(os.path.join(out_dir, filename))

    _set(
        job_id,
        status="done",
        percent=100.0,
        stage="Complete",
        filename=filename,
        ended_at=time.time(),
    )
    db.finish_job(job_id, "done", filename=filename, filesize=size)


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
