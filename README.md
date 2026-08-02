# YouTube Downloader (Flask + yt-dlp)

A small web app that runs `yt-dlp` as a subprocess, streams its progress to the
browser, and serves the finished file. History is stored in SQLite.

## Features

- URL input with client- and server-side YouTube URL validation
- Quality selection: best / 1080p / 720p / 480p / audio-only (MP3)
- Live progress bar with percentage, speed and ETA (polled from parsed yt-dlp output)
- Download history in SQLite, with re-download and remove
- Human-readable errors for private, removed, age-restricted and geo-blocked videos

## Requirements

- Python 3.9+
- `ffmpeg` on `PATH` (needed for merging video+audio and for MP3 extraction)

## Local run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

On Windows, activate with `.venv\Scripts\activate` and install ffmpeg via
`winget install Gyan.FFmpeg`.

## Configuration

All optional, set as environment variables (see `config.py`):

| Variable | Default | Meaning |
| --- | --- | --- |
| `DOWNLOAD_DIR` | `./downloads` | Where finished files are stored |
| `DB_PATH` | `./history.db` | SQLite database file |
| `YTDLP_BIN` | `yt-dlp` | Path to the yt-dlp binary |
| `COOKIES_FILE` | *(unset)* | Path to a Netscape cookies.txt, for when YouTube blocks the server's IP |
| `JOB_TIMEOUT` | `1800` | Per-download timeout, seconds |
| `JOB_TTL` | `3600` | How long finished jobs stay in memory |
| `MAX_CONCURRENT_JOBS` | `3` | Simultaneous yt-dlp processes |

---

## Deploying to Railway

The repo includes a `Dockerfile` and `railway.toml` — Railway builds and runs
it with almost no manual setup.

1. **New project → Deploy from GitHub repo** → pick this repo. Railway detects
   the Dockerfile automatically.
2. **Attach a volume**: Settings → Volumes → add a volume mounted at `/data`.
   Without this, `history.db` and any file mid-download reset on every
   redeploy — the Dockerfile already points `DOWNLOAD_DIR`/`DB_PATH` at
   `/data`, so this is the only step you can't skip.
3. **Set `MAX_CONCURRENT_JOBS`** (optional) if you want fewer than 3
   simultaneous downloads on a small instance.
4. Railway sets `$PORT` automatically; the Dockerfile's `CMD` already binds
   to it.

**About YouTube blocking the server.** Railway (and Render, and most VPS
providers) run on datacenter IP ranges. YouTube frequently responds to those
with "Sign in to confirm you're not a bot" and the download fails outright —
this is unrelated to any bug in the app. If you hit it:

1. Log into YouTube in a normal browser, export cookies with an extension
   like *Get cookies.txt LOCALLY* (Netscape format).
2. Upload `cookies.txt` into the attached volume (e.g. `/data/cookies.txt`)
   — **do not** commit it to git, it's a live session credential.
3. Set the `COOKIES_FILE` env var to that path (e.g. `/data/cookies.txt`).
   `downloader.py` passes it to yt-dlp automatically when set.
4. Cookies expire — you'll need to re-export and re-upload periodically.

The container also runs `pip install --upgrade yt-dlp` on every start, since
YouTube changes break older yt-dlp releases within weeks.

---

## Deploying to a Linux VPS (Ubuntu 22.04/24.04)

### 1. System packages

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip ffmpeg nginx
```

### 2. Create a service user and lay down the code

```bash
sudo adduser --system --group --home /opt/ytdl ytdl
sudo -u ytdl git clone <your-repo-url> /opt/ytdl/app
```

(Or `scp` the directory to `/opt/ytdl/app` and `sudo chown -R ytdl:ytdl /opt/ytdl`.)

### 3. Virtualenv

```bash
sudo -u ytdl python3 -m venv /opt/ytdl/venv
sudo -u ytdl /opt/ytdl/venv/bin/pip install -r /opt/ytdl/app/requirements.txt
```

### 4. systemd unit

**Important:** run exactly **one** Gunicorn worker. Job progress is held in
process memory, so a second worker would not see jobs started by the first.
Use threads (`--threads`) for concurrency instead of workers.

```bash
sudo tee /etc/systemd/system/ytdl.service >/dev/null <<'EOF'
[Unit]
Description=YouTube Downloader (Flask + yt-dlp)
After=network.target

[Service]
User=ytdl
Group=ytdl
WorkingDirectory=/opt/ytdl/app
Environment="DOWNLOAD_DIR=/var/lib/ytdl/downloads"
Environment="DB_PATH=/var/lib/ytdl/history.db"
Environment="YTDLP_BIN=/opt/ytdl/venv/bin/yt-dlp"
ExecStart=/opt/ytdl/venv/bin/gunicorn \
    --workers 1 --threads 8 --timeout 120 \
    --bind 127.0.0.1:8000 wsgi:app
Restart=always
RestartSec=3

# Hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/ytdl

[Install]
WantedBy=multi-user.target
EOF

sudo mkdir -p /var/lib/ytdl/downloads
sudo chown -R ytdl:ytdl /var/lib/ytdl
sudo systemctl daemon-reload
sudo systemctl enable --now ytdl
sudo systemctl status ytdl
```

### 5. Nginx reverse proxy

```bash
sudo tee /etc/nginx/sites-available/ytdl >/dev/null <<'EOF'
server {
    listen 80;
    server_name your.domain.com;

    # Large files are streamed straight through.
    client_max_body_size 10m;
    proxy_max_temp_file_size 0;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_buffering off;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ytdl /etc/nginx/sites-enabled/ytdl
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

### 6. HTTPS

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your.domain.com
```

### 7. Firewall

```bash
sudo ufw allow OpenSSH && sudo ufw allow 'Nginx Full' && sudo ufw enable
```

### 8. Keep yt-dlp current

YouTube changes break yt-dlp regularly; update it weekly:

```bash
sudo tee /etc/systemd/system/ytdl-update.service >/dev/null <<'EOF'
[Unit]
Description=Update yt-dlp
[Service]
Type=oneshot
ExecStart=/opt/ytdl/venv/bin/pip install --upgrade yt-dlp
ExecStartPost=/bin/systemctl restart ytdl
EOF

sudo tee /etc/systemd/system/ytdl-update.timer >/dev/null <<'EOF'
[Unit]
Description=Weekly yt-dlp update
[Timer]
OnCalendar=weekly
Persistent=true
[Install]
WantedBy=timers.target
EOF

sudo systemctl enable --now ytdl-update.timer
```

### 9. Prune old downloads

```bash
echo '0 4 * * * find /var/lib/ytdl/downloads -mindepth 1 -maxdepth 1 -type d -mtime +1 -exec rm -rf {} +' \
  | sudo crontab -u ytdl -
```

### Logs and health

```bash
journalctl -u ytdl -f
curl -s localhost:8000/healthz
```

## Operational notes

- **Access control.** There is no authentication. On a public VPS, put it behind
  HTTP basic auth in Nginx or restrict by IP — an open downloader will be abused.
- **Bot checks.** YouTube may ask a datacenter IP to "sign in to confirm you're
  not a bot". If that happens, pass cookies to yt-dlp via `--cookies` in
  `downloader.py`.
- **Legal.** Download only content you have the right to download.
