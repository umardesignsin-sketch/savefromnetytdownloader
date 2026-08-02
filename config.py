import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Where finished files land. Override with DOWNLOAD_DIR on the server.
DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", os.path.join(BASE_DIR, "downloads"))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "history.db"))

# Absolute path to the yt-dlp binary (use the venv one on a VPS).
YTDLP_BIN = os.environ.get("YTDLP_BIN", "yt-dlp")

# Hard ceiling so one job can't hang a worker forever (seconds).
JOB_TIMEOUT = int(os.environ.get("JOB_TIMEOUT", "1800"))

# Keep finished job metadata in memory for this long (seconds).
JOB_TTL = int(os.environ.get("JOB_TTL", "3600"))

MAX_CONCURRENT_JOBS = int(os.environ.get("MAX_CONCURRENT_JOBS", "3"))

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
