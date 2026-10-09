# SaveFromNet

A public media downloader for content the user owns or may download. It detects
YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads, and
Dailymotion links. The 26 media and transcript tool pages share one URL validator, extraction service,
result UI, and background job runner. Eighteen working single-image tools, a
batch image converter, five media utilities, and 21 practical media guides have their own pages. Localized tool pages,
the guides hub, tool directory, supported-link reference, image-format guide, transcript API documentation and trust pages bring the
public canonical page count to 117. Pages never invent formats: an option is
shown only after a source extractor returns it.

Useful starting points: [supported public URL formats](https://savefromnet.fun/supported-links),
[YouTube Shorts on a phone](https://savefromnet.fun/guides/youtube-shorts-on-phone),
[YouTube MP3 on a phone](https://savefromnet.fun/guides/youtube-mp3-on-phone),
and the [working downloader directory](https://savefromnet.fun/tools).

## Architecture

```
Cloudflare static assets: homepage, 26 media and transcript tools, 18 single-image tools, five media utilities, batch converter, localized pages, guides, directory/resource/trust pages, CSS, JS, sitemap
       ↓ POST /api/analyze and /api/download
Cloudflare Worker: per-IP rate limits
       ↓
Cloudflare Container: Flask + yt-dlp + gallery-dl + ffmpeg
       ↓
Ephemeral SQLite job history and temporary files
       ↓
15-minute signed, browser-bound file link
```

The batch image tool uses the same Pillow-based conversion path as the
single-image tools. A batch contains at most five still images, each at most
8 MB and 20 megapixels, with a 20 MB aggregate input limit. The endpoint
returns a ZIP of the actual results (maximum 32 MB) directly to the browser;
neither source images nor the ZIP are stored in job history. The Worker and
Flask both rate-limit batch requests. This first release is a free beta; no
paid tier or API entitlement is shown until a merchant product and checkout
are configured and tested.

The YouTube Thumbnail Downloader accepts only validated YouTube video IDs and
fetches JPGs from the fixed YouTube thumbnail host. The four upload-based media
utilities use the existing ffmpeg container for real GIF, MP3, video trim, and
audio cut output. Uploads are capped at 16 MB; source duration, segment length,
output size, concurrency and processing time are bounded. Files are kept in a
temporary directory for each request and deleted after the result is read.
The image cropper and AVIF converter use the existing Pillow path and 8 MB
image cap. These utilities are linked from the tools directory and sitemap.

`generate_static.py` renders the Flask templates into edge assets for fast
first loads. The Flask routes remain usable locally. `extractors/detect.py`
normalizes allowlisted public URL shapes before any network request.
`extractors/service.py` analyzes real source formats, caches public metadata
for 90 seconds, and stores format selections under a short-lived analysis ID.
`downloader.py` runs the selected format in a background process; it never
passes a raw user URL or format string to a shell. `tools.py` owns tool-page
content and metadata. `guides.py` owns the editorial guides, each linked to a
working downloader. `site_pages.py` owns the tools directory and trust copy;
`growth/seo-audit-2026-10-07.md` explains the reference URL mapping and why
overlapping MP3 landing pages were deferred. `db.py` stores anonymous history and local aggregate
events. The Worker also writes privacy-minimal, persistent aggregate events
to Cloudflare Analytics Engine dataset `savefromnet_events`.

## Programmatic tool content

`tools.py` is the registry for all 26 canonical media and transcript routes. Each tool
defines its supported content types, link guidance, format explanation, errors,
metadata, and FAQ. `TOOL_SECTIONS` adds distinct, task-specific guidance to
selected routes; `TOOL_SEO_LINKS` connects those sections to relevant working
tools and guides. The shared `templates/site.html` renders these records, so a
copy change does not require a new route or a duplicate page template. Keep
claims aligned with `extractors/detect.py`, `extractors/service.py`, and the
tool-specific filtering in `app.py`. Add a new indexable URL only when its
actual downloader behavior and search intent differ from an existing route.
The route, link, and editorial-content checks live in `tests/test_platform.py`.
`guides.py` now includes specific-link and troubleshooting pages with a real
tool form and contextual related guides. The tools directory links to the new
pages. Run `python growth/build_target_inventory.py` after changing public
routes to refresh the canonical URL inventory; the tests compare that inventory
with the generated sitemap.

`yt-dlp` handles public video/audio sources and the YouTube to Transcript page's public caption tracks. The transcript endpoint downloads only a selected caption track into a temporary directory, returns bounded timed cues, and deletes the temporary file; TXT, SRT and VTT exports are generated in the browser. It does not run speech recognition for videos without accessible captions. `gallery-dl` handles accessible
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
- `POST /api/transcript` with a direct public YouTube `url` and optional returned
  `language` code returns actual caption cues, track languages and video metadata.
  The request is rate limited and does not store a transcript download file.
- `POST /api/v1/youtube/transcript` is the versioned public developer route for
  the same caption extractor. See the [API documentation](https://savefromnet.fun/youtube-transcript-api)
  for a request example, response fields, and limitations. It currently has no
  API key or paid entitlement and is intended for low-volume use.
- `POST /api/v2/youtube/transcript` accepts the same JSON with a developer Bearer
  API key. The subscription plan is $5/month for 1,000 successful transcripts,
  with four attempts per minute and two concurrent extractions per account.
  `/developers` provides checkout, key rotation, account recovery, usage and
  billing management. Checkout requires a separate Dodo subscription product
  and webhook; see [billing setup](docs/transcript-api-billing.md).
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
Engine dataset is the durable event source.

## Private visitor dashboard

`/analytics` is a private, password-protected dashboard. Sign in with username
`admin` and the Cloudflare Worker secret `DASHBOARD_PASSWORD`. The dashboard and
`GET /api/analytics` are never cached or indexed. `VISITOR_HASH_KEY` is a
separate Worker secret used to derive a rotating daily HMAC from the request IP
and browser type. Neither the raw IP nor a media URL is stored in visitor
analytics. A first-party `/api/visit` page signal and visible-tab heartbeat
provide approximate unique visitors today, page views, live visitors in the
last five minutes, and country counts. The numbers start at deployment and
reset at midnight UTC; visitor rows expire after about two days. The dashboard
includes a draggable globe and updates every 15 seconds.

## Limits and storage

The Worker allows eight analyses, two download starts, four signed file
requests, and 30 analytics events per IP per minute.
Flask also applies per-browser limits. One 512 MB job runs at a time, and four
analyses may run concurrently. Completed files are cleaned up after about an
hour when the container remains active. The Container sleeps after five minutes
of inactivity; that can clear files sooner. SQLite history and metrics are
ephemeral as well. Visitor counts use a separate SQLite-backed Durable Object
and persist across Container sleeps. Media files are deliberately not stored
permanently.

## Cloudflare deployment

The site is routed from `savefromnet.fun/*` to Worker `savefromnet-funyt`.
The separate `savefromnet-www-redirect` Worker routes `www.savefromnet.fun/*`
and `http://savefromnet.fun/*` to the HTTPS apex with a permanent redirect
while preserving path and query. HTTPS apex requests continue to use the main
static-asset Worker route.
Deploy it with `npx wrangler deploy --config wrangler.www.jsonc`.
`wrangler.jsonc` pins a Cloudflare Container image tag. The GitHub Actions
workflow `.github/workflows/build-container.yml` builds and publishes that
image when manually dispatched. It uses short-lived registry credentials in
the repository's Actions secrets; remove them after a successful build.
Update the image tag to the built commit SHA, then run `npm ci` and
`npm run deploy`. The deploy script regenerates static pages before Wrangler
uploads them. It does not change the zone's existing DNS records.
