FROM node:22-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates ffmpeg python3 python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/downloader

ENV PATH=/opt/downloader/bin:/usr/local/bin:/usr/bin:/bin \
    PYTHONDONTWRITEBYTECODE=1 \
    DOWNLOAD_DIR=/tmp/savefromnet/downloads \
    DB_PATH=/tmp/savefromnet/history.db \
    MAX_CONCURRENT_JOBS=1 \
    MAX_FILESIZE=512M \
    PORT=8080

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 'yt-dlp[default]'
COPY . .

RUN mkdir -p /tmp/savefromnet/downloads \
    && chown -R node:node /app /tmp/savefromnet
USER node

EXPOSE 8080
CMD ["gunicorn", "--workers", "1", "--threads", "8", "--timeout", "120", "--bind", "0.0.0.0:8080", "wsgi:app"]