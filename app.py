"""SaveFromNet public site and JSON API."""

import hashlib
import hmac
import os
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from urllib.parse import urlencode

from flask import Flask, g, jsonify, render_template, request, send_file, Response

import db
import downloader
from config import DOWNLOAD_DIR
from extractors import AnalysisError, DetectError, analyze, detect_url
from extractors.service import resolve
from guides import BY_SLUG as GUIDES_BY_SLUG, GUIDES
from site_pages import BY_SLUG as PAGES_BY_SLUG, PAGES, TOOL_GROUPS
from tools import BY_SLUG, PLATFORMS, TOOLS, related_tools

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
db.init_db()
CLIENT_ID = re.compile(r"^[A-Za-z0-9_-]{43}$")
JOB_ID = re.compile(r"^[0-9a-f]{32}$")
SIGNING_KEY = os.environ.get("DOWNLOAD_SIGNING_KEY", "").encode() or secrets.token_bytes(32)
SITE_URL = "https://savefromnet.fun"
_limits = defaultdict(deque)
_limits_lock = threading.Lock()
_analysis_slots = threading.BoundedSemaphore(4)
_last_cleanup = 0


@app.errorhandler(413)
def request_too_large(_error):
    if request.path.startswith("/api/"):
        return _json_error("The request is too large. Paste one media URL.", "request_too_large", 413)
    return "Request too large", 413


@app.errorhandler(500)
def internal_error(_error):
    if request.path.startswith("/api/"):
        return _json_error("A server error occurred. Please try again.", "server_error", 500)
    return "Server error", 500


def _json_error(message, code="error", status=400):
    return jsonify({"error": message, "code": code}), status


def _rate_limit(owner, action, max_calls, period=60):
    key = (owner, action)
    with _limits_lock:
        calls = _limits[key]
        now = time.monotonic()
        while calls and now - calls[0] > period:
            calls.popleft()
        if len(calls) >= max_calls:
            db.record_event("rate_limited", "unknown", "universal-video-downloader")
            return False
        calls.append(now)
        return True


def _cleanup():
    global _last_cleanup
    now = time.monotonic()
    if now - _last_cleanup < 60:
        return
    _last_cleanup = now
    for job_id in db.expired_files():
        downloader.remove_files(job_id)


@app.before_request
def identify_client():
    if request.path == "/healthz":
        return
    client_id = request.cookies.get("client_id", "")
    if not CLIENT_ID.fullmatch(client_id):
        client_id = secrets.token_urlsafe(32)
        g.new_client_id = client_id
    g.client_id = client_id
    _cleanup()


@app.after_request
def persist_client(response):
    client_id = getattr(g, "new_client_id", None)
    if client_id:
        response.set_cookie("client_id", client_id, max_age=30 * 24 * 3600,
                            secure=request.is_secure or request.headers.get("X-Forwarded-Proto") == "https",
                            httponly=True, samesite="Lax")
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    if request.path.startswith("/api/") or request.path in ("/healthz", "/sw.js"):
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


def _signed_link(job_id, owner):
    expires = int(time.time()) + 900
    signature = hmac.new(SIGNING_KEY, f"{job_id}:{owner}:{expires}".encode(), hashlib.sha256).hexdigest()
    return f"/api/file/{job_id}?{urlencode({'expires': expires, 'sig': signature})}"


def _verify_link(job_id, owner):
    try:
        expires = int(request.args.get("expires", "0"))
    except ValueError:
        return False
    if expires < time.time() or expires > time.time() + 901:
        return False
    signature = request.args.get("sig", "")
    expected = hmac.new(SIGNING_KEY, f"{job_id}:{owner}:{expires}".encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)


def _filter_formats(tool, media):
    if tool.platform != "universal" and tool.platform != media["platform"]:
        raise AnalysisError(f"Use a {tool.platform.title()} URL with this tool.", "wrong_platform")
    if media["type"] not in tool.content_types:
        raise AnalysisError("This tool needs a different kind of link. Check the supported URLs below.", "wrong_content_type")
    slug = tool.slug
    formats = media["formats"]
    if slug.endswith("to-mp3") or slug in ("youtube-audio-downloader", "youtube-song-downloader", "youtube-music-downloader"):
        formats = [f for f in formats if f["type"] == "audio" and (not slug.endswith("to-mp3") or f["extension"] == "mp3")]
    elif slug == "youtube-to-mp4":
        formats = [f for f in formats if f["extension"] == "mp4" and f["type"] == "video"]
    elif slug == "instagram-photo-downloader":
        formats = [f for f in formats if f["type"] == "image"]
    elif slug in ("instagram-video-downloader", "instagram-reels-downloader", "youtube-video-downloader", "youtube-shorts-downloader", "youtube-movies-downloader", "facebook-video-downloader", "reddit-video-downloader", "threads-video-downloader", "dailymotion-video-downloader"):
        formats = [f for f in formats if f["type"] == "video"]
    if not formats:
        raise AnalysisError("This source has no accessible format for this tool. Try a related tool.", "no_formats")
    media["formats"] = formats
    return media


def _related_guides(guide):
    if not guide:
        return ()
    platform = BY_SLUG[guide.tool_slug].platform
    candidates = list(guide.related)
    candidates += [item.slug for item in reversed(GUIDES)
                   if item.slug != guide.slug and BY_SLUG[item.tool_slug].platform == platform]
    candidates.append("why-media-links-fail")
    return tuple(GUIDES_BY_SLUG[slug] for slug in dict.fromkeys(candidates)
                 if slug != guide.slug and slug in GUIDES_BY_SLUG)[:4]


def _page(tool=None, guide=None, guide_index=False):
    platform_home = next((item for item in TOOLS if tool and item.platform == tool.platform), None)
    primary_tools = [next(item for item in TOOLS if item.platform == platform) for platform in PLATFORMS]
    quick_links = []
    if tool and tool.platform != "universal":
        quick_links = [tool] + [item for item in TOOLS if item.platform == tool.platform and item.slug != tool.slug]
        quick_links += [BY_SLUG["universal-video-downloader"]] + primary_tools
    else:
        quick_links = primary_tools
    quick_links = list({item.slug: item for item in quick_links}.values())[:8]
    if guide:
        title = f"{guide.title} | SaveFromNet Guides"
        description = guide.description
        canonical = SITE_URL + guide.path
    elif guide_index:
        title = "Media Download Guides | SaveFromNet"
        description = "Practical guides to public video, photo and audio links, available formats and common download problems across eight supported platforms."
        canonical = SITE_URL + "/guides"
    else:
        title = tool.seo_title if tool else "SaveFromNet — Video Downloader & Converter"
        description = tool.seo_description if tool else "Download public videos, reels, shorts, photos and audio from your favorite platforms. See real formats before you save."
        canonical = SITE_URL + tool.path if tool else SITE_URL + "/"
    if guide:
        schema = [{"@context": "https://schema.org", "@type": "Article", "headline": guide.title,
                   "description": description, "mainEntityOfPage": canonical,
                   "publisher": {"@type": "Organization", "name": "SaveFromNet", "url": SITE_URL}}]
    elif guide_index:
        schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Media Download Guides",
                   "description": description, "url": canonical}]
    else:
        schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": tool.name if tool else "SaveFromNet",
                   "applicationCategory": "MultimediaApplication", "operatingSystem": "Any",
                   "url": canonical, "description": description,
                   "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
    if guide:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q,
                                       "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in guide.faq]})
    elif tool:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                      for q, a in tool.faq]})
    if guide or guide_index:
        schema.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
                                           {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE_URL + "/guides"}]
                                          + ([{"@type": "ListItem", "position": 3, "name": guide.title, "item": canonical}] if guide else [])})
    elif tool:
        schema.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
                                          + ([{"@type": "ListItem", "position": 2, "name": platform_home.name,
                                               "item": SITE_URL + platform_home.path}] if platform_home and platform_home.slug != tool.slug else [])
                                          + [{"@type": "ListItem", "position": 3 if platform_home and platform_home.slug != tool.slug else 2,
                                              "name": tool.name, "item": canonical}]})
    platform_guides = {"youtube": "youtube-video-formats", "instagram": "instagram-public-media",
                       "tiktok": "tiktok-video-and-audio", "facebook": "facebook-public-videos",
                       "pinterest": "pinterest-pin-media", "reddit": "reddit-video-with-audio",
                       "threads": "threads-video-availability", "dailymotion": "dailymotion-video-quality"}
    platform_guide = GUIDES_BY_SLUG.get(platform_guides.get(tool.platform)) if tool else None
    return render_template("site.html", tool=tool, title=title, description=description,
                           canonical=canonical, tools=TOOLS, platforms=PLATFORMS,
                           related=related_tools(tool) if tool else TOOLS[:10], schema=schema,
                           guide=guide, guide_index=guide_index, guides=GUIDES,
                           related_guides=_related_guides(guide),
                           platform_guide=platform_guide, platform_home=platform_home,
                           quick_links=quick_links)


@app.get("/")
def index():
    return _page()


@app.get("/guides")
def guides_index():
    return _page(guide_index=True)


@app.get("/guides/<slug>")
def guide_page(slug):
    guide = GUIDES_BY_SLUG.get(slug)
    if not guide:
        return render_template("404.html", tools=TOOLS), 404
    return _page(tool=BY_SLUG[guide.tool_slug], guide=guide)


@app.get("/sw.js")
def service_worker():
    response = send_file(os.path.join(app.root_path, "sw.js"), mimetype="application/javascript")
    response.headers["Cache-Control"] = "no-cache"
    return response


def _content_page(page):
    canonical = SITE_URL + page.path
    schema = [
        {"@context": "https://schema.org", "@type": page.schema_type,
         "name": page.heading, "description": page.description, "url": canonical},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
             {"@type": "ListItem", "position": 2, "name": page.heading, "item": canonical},
         ]},
    ]
    groups = [(name, [BY_SLUG[slug] for slug in slugs]) for name, slugs in TOOL_GROUPS]
    return render_template("site.html", content_page=page, tool_groups=groups,
                           title=page.title, description=page.description,
                           canonical=canonical, schema=schema, tool=None,
                           guide=None, guide_index=False, tools=TOOLS,
                           platforms=PLATFORMS, guides=GUIDES,
                           featured_guides=GUIDES[-6:])


@app.get("/<slug>")
def tool_page(slug):
    tool = BY_SLUG.get(slug)
    if tool:
        return _page(tool)
    page = PAGES_BY_SLUG.get(slug)
    if page:
        return _content_page(page)
    return render_template("404.html", tools=TOOLS), 404


@app.post("/api/analyze")
def api_analyze():
    if not _rate_limit(g.client_id, "analyze", 8):
        return _json_error("Too many analyses. Please try again in a minute.", "rate_limited", 429)
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return _json_error("Send a URL in a JSON object.", "invalid_request")
    slug = data.get("tool") or "universal-video-downloader"
    tool = BY_SLUG.get(slug)
    if not tool:
        return _json_error("Unknown downloader tool.", "invalid_tool")
    try:
        detection = detect_url(data.get("url"))
        db.record_event("url_submitted", detection.platform, slug)
        db.record_event("platform_detected", detection.platform, slug)
        if tool.platform != "universal" and tool.platform != detection.platform:
            raise AnalysisError(f"Use a {tool.platform.title()} URL with this tool.", "wrong_platform")
        if detection.content_type not in tool.content_types:
            raise AnalysisError("This tool needs a different kind of link. Check the supported URLs below.", "wrong_content_type")
        if not _analysis_slots.acquire(blocking=False):
            return _json_error("Analysis capacity is busy. Please try again shortly.", "busy", 429)
        try:
            media = _filter_formats(tool, analyze(detection.normalized_url, g.client_id))
        finally:
            _analysis_slots.release()
    except DetectError as exc:
        db.record_event("analysis_failed", "unknown", slug)
        return _json_error(str(exc), "invalid_url")
    except AnalysisError as exc:
        db.record_event("analysis_failed", detection.platform if "detection" in locals() else "unknown", slug)
        return _json_error(str(exc), exc.code, 422)
    db.record_event("analysis_successful", detection.platform, slug)
    media["tool"] = slug
    return jsonify(media)


@app.post("/api/download")
def api_download():
    if not _rate_limit(g.client_id, "download", 2):
        return _json_error("Too many downloads. Please try again in a minute.", "rate_limited", 429)
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return _json_error("Send a selected format in a JSON object.", "invalid_request")
    try:
        url, detection, spec = resolve(data.get("analysis_id", ""), data.get("format_id", ""), g.client_id)
    except AnalysisError as exc:
        return _json_error(str(exc), exc.code, 400)
    slug = data.get("tool") or "universal-video-downloader"
    if slug not in BY_SLUG:
        return _json_error("Unknown downloader tool.", "invalid_tool")
    if not downloader.ytdlp_available() and spec["engine"] == "yt-dlp":
        return _json_error("The media extractor is unavailable. Please try later.", "server_error", 503)
    job_id = downloader.start(url, spec["label"], g.client_id, spec, detection.platform, slug)
    if not job_id:
        return _json_error("The server is busy. Please try again shortly.", "busy", 429)
    db.record_event("download_clicked", detection.platform, slug, spec.get("extension"))
    return jsonify({"job_id": job_id, "platform": detection.platform,
                    "tool": slug, "format": spec.get("extension", "")}), 202


@app.get("/api/progress/<job_id>")
def api_progress(job_id):
    if not JOB_ID.fullmatch(job_id):
        return _json_error("Unknown job.", "not_found", 404)
    row = db.get_job(job_id, g.client_id)
    if not row:
        return _json_error("Unknown job.", "not_found", 404)
    state = downloader.get_state(job_id)
    if state:
        for key in ("ended_at", "spec", "url"):
            state.pop(key, None)
        if state["status"] == "done":
            state["download_url"] = _signed_link(job_id, g.client_id)
        return jsonify(state)
    return jsonify({"job_id": job_id, "status": row["status"],
                    "percent": 100.0 if row["status"] == "done" else 0.0,
                    "stage": "Complete" if row["status"] == "done" else "Failed",
                    "title": row["title"], "filename": row["filename"],
                    "error": row["error"], "speed": None, "eta": None,
                    "download_url": _signed_link(job_id, g.client_id) if row["status"] == "done" else None})


@app.get("/api/file/<job_id>")
def api_file(job_id):
    if not JOB_ID.fullmatch(job_id) or not _verify_link(job_id, g.client_id):
        return _json_error("This download link has expired. Refresh your history for a new link.", "expired", 403)
    row = db.get_job(job_id, g.client_id)
    if not row or row["status"] != "done" or not row["filename"]:
        return _json_error("File is not available.", "not_found", 404)
    path = downloader.file_path(job_id, row["filename"])
    if not path:
        return _json_error("This temporary file has expired.", "expired", 410)
    response = send_file(path, as_attachment=True, download_name=os.path.basename(path))
    if row["platform"] and row["tool_slug"]:
        response.headers["X-SFN-Platform"] = row["platform"]
        response.headers["X-SFN-Tool"] = row["tool_slug"]
        response.headers["X-SFN-Format"] = row["file_format"]
        response.call_on_close(lambda: db.record_event("download_completed", row["platform"], row["tool_slug"], row["file_format"]))
    return response


@app.get("/api/history")
def api_history():
    rows = db.list_history(g.client_id, limit=30)
    for row in rows:
        row["available"] = bool(row["filename"] and downloader.file_path(row["job_id"], row["filename"]))
        row["download_url"] = _signed_link(row["job_id"], g.client_id) if row["available"] else None
    return jsonify(rows)


@app.delete("/api/history/<job_id>")
def api_history_delete(job_id):
    if not JOB_ID.fullmatch(job_id) or not db.get_job(job_id, g.client_id):
        return _json_error("Unknown job.", "not_found", 404)
    downloader.remove_files(job_id)
    db.delete_history_entry(job_id, g.client_id)
    return jsonify({"ok": True})


@app.post("/api/event")
def api_event():
    if not _rate_limit(g.client_id, "event", 30):
        return _json_error("Too many events.", "rate_limited", 429)
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict) or data.get("event") not in ("format_selected", "error_occurred", "tool_page_view", "download_failed"):
        return _json_error("Unknown event.", "invalid_event")
    tool = BY_SLUG.get(data.get("tool"))
    platform = data.get("platform")
    if not tool or platform not in (*PLATFORMS, "unknown") or (tool.platform != "universal" and tool.platform != platform):
        return _json_error("Invalid event context.", "invalid_event")
    db.record_event(data["event"], platform, tool.slug, str(data.get("format", ""))[:12])
    return jsonify({"ok": True})


@app.get("/api/metrics")
def api_metrics():
    admin_token = os.environ.get("ADMIN_METRICS_TOKEN", "")
    supplied = request.headers.get("Authorization", "").removeprefix("Bearer ")
    if not admin_token or not hmac.compare_digest(supplied, admin_token):
        return _json_error("Not found.", "not_found", 404)
    return jsonify(db.metrics())


@app.get("/api/activity")
def api_activity():
    return jsonify({"active": downloader.active_count()})


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "ytdlp": downloader.ytdlp_available(), "download_dir": DOWNLOAD_DIR})


@app.get("/robots.txt")
def robots():
    return Response(f"User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /healthz\nDisallow: /sw.js\nSitemap: {SITE_URL}/sitemap.xml\n", mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap():
    pages = [(SITE_URL + "/", "1.0")] + [(SITE_URL + tool.path, "0.7") for tool in TOOLS]
    pages += [(SITE_URL + "/guides", "0.7")]
    pages += [(SITE_URL + guide.path, "0.6") for guide in GUIDES]
    pages += [(SITE_URL + page.path, "0.8" if page.slug == "tools" else "0.4") for page in PAGES]
    body = "".join(f"<url><loc>{url}</loc><changefreq>weekly</changefreq><priority>{priority}</priority></url>" for url, priority in pages)
    return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>", mimetype="application/xml")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
