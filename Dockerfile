FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# PO Token provider: YouTube now requires a proof-of-origin token for
# authenticated (cookied) requests. Without one, yt-dlp's client negotiation
# silently falls back to a broken "tv" client that returns no real formats
# ("Requested format is not available" + "Unknown codec iamf..."). This runs
# a local PO token server that the bgutil-ytdlp-pot-provider yt-dlp plugin
# talks to automatically — this is the documented fix for that failure mode.
RUN pip install --no-cache-dir bgutil-ytdlp-pot-provider \
    && git clone --depth 1 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git /opt/bgutil-provider \
    && cd /opt/bgutil-provider/server \
    && npm install \
    && npx tsc

COPY . .

ENV DOWNLOAD_DIR=/data/downloads
ENV DB_PATH=/data/history.db
RUN mkdir -p /data/downloads

EXPOSE 5000

# Bump yt-dlp on every container start/redeploy — YouTube breaks it often
# and a stale copy is the most common cause of "video unavailable" errors
# that aren't actually true. Single gunicorn worker: progress state lives
# in process memory, so a second worker would never see jobs the first
# one started. The PO token server runs in the background on its default
# port (4416); the yt-dlp plugin talks to it there automatically.
CMD pip install --no-cache-dir --upgrade yt-dlp && \
    node /opt/bgutil-provider/server/build/main.js & \
    gunicorn --workers 1 --threads 8 --timeout 120 --bind 0.0.0.0:${PORT:-5000} wsgi:app
