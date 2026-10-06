# SaveFromNet

A public media downloader for content the user owns or may download. It detects
YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads, and
Dailymotion links. The 25 pages share one URL validator, extraction service,
result UI, and background job runner. Ten practical guides and a guides hub
explain supported links and formats. Pages never invent formats: an option is
shown only after a source extractor returns it.

## Architecture

```
Cloudflare static assets: homepage, 25 tool pages, 11 guide pages, CSS, JS, sitemap
       ↓ POST /api/analyze and /api/download
Cloudflare Worker: per-IP rate limits
       ↓
Cloudflare Container: Flask + yt-dlp + gallery-dl + ffmpeg
       ↓
Ephemeral SQLite job history and temporary files
       ↓
15-minute signed, browser-bound file link
```

`generate_static.py` renders the Flask templates into edge assets for fast
first loads. The Flask routes remain usable locally. `extractors/detect.py`
normalizes allowlisted public URL shapes before any network request.
`extractors/service.py` analyzes real source formats, caches public metadata
for 90 seconds, and stores format selections under a short-lived analysis ID.
`downloader.py` runs the selected format in a background process; it never
passes a raw user URL or format string to a shell. `tools.py` owns tool-page
content and metadata. `guides.py` owns the editorial guides, each linked to a
working downloader. `db.py` stores anonymous history and local aggregate
events. The Worker also writes privacy-minimal, persistent aggregate events
to Cloudflare Analytics Engine dataset `savefromnet_events`.

`yt-dlp` handles public video/audio sources. `gallery-dl` handles accessible
Instagram post/profile/story media, TikTok Stories, and Pinterest images/GIFs.
Threads is limited to public posts that expose a video in Open Graph metadata.
The service does not use account cookies or bypass DRM, paywalls, private posts,
or other access controls. Source-site changes or data-center blocking can make
some public URLs unavailable; the API returns a clear error in that case.

## Local development

Requires Python 3.10+, Node.js 22+, and ffmpeg. On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open `http://127.0.0.1:5000`. Put `.venv/Scripts` on `PATH` when testing real
downloads so `yt-dlp` and `gallery-dl` CLI commands are found. To render the
edge site, run `python generate_static.py`. Run checks with
`python -m unittest discover -s tests -v`.

## API

- `POST /api/analyze` with `{ "url": "...", "tool": "youtube-to-mp3" }` returns
  title, author, thumbnail, duration, real available formats, and an
  `analysis_id`. Analysis IDs expire after 10 minutes and belong to the
  requesting anonymous browser.
- `POST /api/download` with `analysis_id`, a returned `format_id`, and the
  tool slug starts a background job. The server rechecks ownership and the
  selected format.
- `GET /api/progress/{job_id}` reports progress and, when ready, a signed
  `download_url`.
- `GET /api/file/{job_id}` requires the signed link and the same browser
  cookie. Links expire in 15 minutes; refresh history for a new link.
- `GET /api/history` and `DELETE /api/history/{job_id}` manage that browser's
  temporary files. `GET /healthz` reports service health.
- `GET /api/metrics` returns aggregate counters only when
`ADMIN_METRICS_TOKEN` is configured and supplied as a Bearer token. These
local counters reset when the Container sleeps; the Cloudflare Analytics
Engine dataset is the durable event source. No admin account system exists in
this project.

## Limits and storage

The Worker allows eight analyses, two download starts, four signed file
requests, and 30 analytics events per IP per minute.
Flask also applies per-browser limits. One 512 MB job runs at a time, and four
analyses may run concurrently. Completed files are cleaned up after about an
hour when the container remains active. The Container sleeps after five minutes
of inactivity; that can clear files sooner. SQLite history and metrics are
ephemeral as well. A future persistent history or analytics feature would
require a separate Cloudflare database; media files are deliberately not stored
permanently.

## Cloudflare deployment

The site is routed from `savefromnet.fun/*` to Worker `savefromnet-funyt`.
`wrangler.jsonc` pins a Cloudflare Container image tag. The GitHub Actions
workflow `.github/workflows/build-container.yml` builds and publishes that
image when manually dispatched. It uses short-lived registry credentials in
the repository's Actions secrets; remove them after a successful build.
Update the image tag to the built commit SHA, then run `npm ci` and
`npm run deploy`. The deploy script regenerates static pages before Wrangler
uploads them. It does not change the zone's existing DNS records.
