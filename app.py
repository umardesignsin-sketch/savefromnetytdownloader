import os
import re
import secrets
from urllib.parse import urlparse

from flask import Flask, g, jsonify, render_template, request, send_file

import db
import downloader
from config import DOWNLOAD_DIR

app = Flask(__name__)
db.init_db()
CLIENT_ID = re.compile(r"^[A-Za-z0-9_-]{43}$")


@app.before_request
def identify_client():
    if request.path in ("/healthz", "/api/activity"):
        return
    client_id = request.cookies.get("client_id", "")
    if not CLIENT_ID.fullmatch(client_id):
        client_id = secrets.token_urlsafe(32)
        g.new_client_id = client_id
    g.client_id = client_id


@app.after_request
def persist_client(response):
    client_id = getattr(g, "new_client_id", None)
    if client_id:
        response.set_cookie(
            "client_id", client_id, max_age=30 * 24 * 3600,
            secure=request.is_secure or request.headers.get("X-Forwarded-Proto") == "https",
            httponly=True, samesite="Lax",
        )
    response.headers["Cache-Control"] = "no-store"
    return response

ALLOWED_HOSTS = {
    "youtube.com", "www.youtube.com", "m.youtube.com",
    "music.youtube.com", "youtu.be", "www.youtu.be",
}

_YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def validate_url(raw):
    """Return (normalized_url, error). Only accepts YouTube video URLs."""
    if not raw or not raw.strip():
        return None, "Please enter a URL."
    raw = raw.strip()
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw

    try:
        parsed = urlparse(raw)
    except ValueError:
        return None, "That URL could not be parsed."

    if parsed.scheme not in ("http", "https"):
        return None, "Only http and https URLs are supported."
    host = (parsed.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        return None, "Only YouTube links are supported."

    if host.endswith("youtu.be"):
        vid = parsed.path.lstrip("/").split("/")[0]
    else:
        if parsed.path not in ("/watch", "/shorts", "/live") and not parsed.path.startswith(
            ("/shorts/", "/live/", "/embed/")
        ):
            return None, "That doesn't look like a link to a single video."
        if parsed.path == "/watch":
            from urllib.parse import parse_qs
            vid = (parse_qs(parsed.query).get("v") or [""])[0]
        else:
            vid = parsed.path.rstrip("/").split("/")[-1]

    if not _YT_ID.match(vid):
        return None, "Couldn't find a valid video ID in that URL."

    return f"https://www.youtube.com/watch?v={vid}", None


@app.get("/")
def index():
    return render_template(
        "index.html",
        qualities=list(downloader.QUALITIES.keys()),
        ytdlp_ok=downloader.ytdlp_available(),
    )


@app.post("/api/download")
def api_download():
    data = request.get_json(silent=True) or {}
    url, error = validate_url(data.get("url"))
    if error:
        return jsonify({"error": error}), 400

    quality = data.get("quality", "best")
    if quality not in downloader.QUALITIES:
        return jsonify({"error": "Unknown quality option."}), 400

    if not downloader.ytdlp_available():
        return jsonify({"error": "yt-dlp is not installed on the server."}), 503

    job_id = downloader.start(url, quality, g.client_id)
    if not job_id:
        return jsonify({"error": "The server is busy. Please try again shortly."}), 429
    return jsonify({"job_id": job_id}), 202


@app.get("/api/progress/<job_id>")
def api_progress(job_id):
    row = db.get_job(job_id, g.client_id)
    if not row:
        return jsonify({"error": "Unknown job."}), 404
    state = downloader.get_state(job_id)
    if state:
        state.pop("ended_at", None)
        return jsonify(state)

    # Job aged out of memory — fall back to what SQLite recorded.
    return jsonify({
        "job_id": job_id,
        "status": row["status"],
        "percent": 100.0 if row["status"] == "done" else 0.0,
        "stage": "Complete" if row["status"] == "done" else "Failed",
        "title": row["title"],
        "filename": row["filename"],
        "error": row["error"],
        "speed": None,
        "eta": None,
    })


@app.get("/api/file/<job_id>")
def api_file(job_id):
    row = db.get_job(job_id, g.client_id)
    if not row or row["status"] != "done" or not row["filename"]:
        return jsonify({"error": "File is not available."}), 404

    path = downloader.file_path(job_id, row["filename"])
    if not path:
        return jsonify({"error": "File no longer exists on the server."}), 410

    return send_file(path, as_attachment=True, download_name=os.path.basename(path))


@app.get("/api/history")
def api_history():
    rows = db.list_history(g.client_id, limit=50)
    for r in rows:
        r["available"] = bool(
            r["filename"] and downloader.file_path(r["job_id"], r["filename"])
        )
    return jsonify(rows)


@app.delete("/api/history/<job_id>")
def api_history_delete(job_id):
    if not db.get_job(job_id, g.client_id):
        return jsonify({"error": "Unknown job."}), 404
    downloader.remove_files(job_id)
    db.delete_history_entry(job_id, g.client_id)
    return jsonify({"ok": True})


@app.get("/api/activity")
def api_activity():
    return jsonify({"active": downloader.active_count()})


@app.get("/healthz")
def healthz():
    return jsonify({
        "ok": True,
        "ytdlp": downloader.ytdlp_available(),
        "download_dir": DOWNLOAD_DIR,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
