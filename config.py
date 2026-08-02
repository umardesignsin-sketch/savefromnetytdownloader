import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Where finished files land. Override with DOWNLOAD_DIR on the server.
DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", os.path.join(BASE_DIR, "downloads"))
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "history.db"))

# Absolute path to the yt-dlp binary (use the venv one on a VPS).
YTDLP_BIN = os.environ.get("YTDLP_BIN", "yt-dlp")

# Path to a Netscape-format cookies.txt exported from a logged-in YouTube
# session. Datacenter IPs (Railway, Render, most VPS providers) frequently get
# "Sign in to confirm you're not a bot" from YouTube; passing cookies works
# around it. Leave unset to run without cookies.
COOKIES_FILE = os.environ.get("COOKIES_FILE", "")

# Residential proxy URL, e.g. http://user:pass@p.webshare.io:80
# The actual fix for datacenter-IP blocking: routes yt-dlp's traffic through
# a residential IP so YouTube treats it like a normal home user. Cookies
# alone (above) stop working once YouTube also gates the client on IP
# reputation. Leave unset to connect directly.
PROXY_URL = os.environ.get("PROXY_URL", "")

# Hard ceiling so one job can't hang a worker forever (seconds).
JOB_TIMEOUT = int(os.environ.get("JOB_TIMEOUT", "1800"))

# Keep finished job metadata in memory for this long (seconds).
JOB_TTL = int(os.environ.get("JOB_TTL", "3600"))

MAX_CONCURRENT_JOBS = int(os.environ.get("MAX_CONCURRENT_JOBS", "3"))

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
