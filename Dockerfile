FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DOWNLOAD_DIR=/data/downloads
ENV DB_PATH=/data/history.db
RUN mkdir -p /data/downloads

EXPOSE 5000

# Bump yt-dlp on every container start/redeploy — YouTube breaks it often
# and a stale copy is the most common cause of "video unavailable" errors
# that aren't actually true. Single gunicorn worker: progress state lives
# in process memory, so a second worker would never see jobs the first
# one started.
CMD pip install --no-cache-dir --upgrade yt-dlp && \
    gunicorn --workers 1 --threads 8 --timeout 120 --bind 0.0.0.0:${PORT:-5000} wsgi:app
