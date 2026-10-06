import sqlite3
from contextlib import contextmanager

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS downloads (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id      TEXT UNIQUE NOT NULL,
    owner_id    TEXT NOT NULL,
    url         TEXT NOT NULL,
    title       TEXT,
    quality     TEXT NOT NULL,
    status      TEXT NOT NULL,          -- queued | downloading | done | error
    error       TEXT,
    filename    TEXT,
    filesize    INTEGER,
    platform    TEXT NOT NULL DEFAULT '',
    tool_slug   TEXT NOT NULL DEFAULT '',
    file_format TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_downloads_created ON downloads(created_at DESC);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    platform TEXT NOT NULL,
    tool_slug TEXT NOT NULL,
    format TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at DESC);
"""


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(downloads)")}
        if "owner_id" not in columns:
            conn.execute("ALTER TABLE downloads ADD COLUMN owner_id TEXT NOT NULL DEFAULT ''")
        for name in ("platform", "tool_slug", "file_format"):
            if name not in columns:
                conn.execute(f"ALTER TABLE downloads ADD COLUMN {name} TEXT NOT NULL DEFAULT ''")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_downloads_owner ON downloads(owner_id, id DESC)")


def insert_job(job_id, url, quality, owner_id, platform="", tool_slug="", file_format=""):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO downloads (job_id, url, quality, owner_id, platform, tool_slug, file_format, status) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 'queued')",
            (job_id, url, quality, owner_id, platform, tool_slug, file_format),
        )


def update_job(job_id, **fields):
    if not fields:
        return
    cols = ", ".join(f"{k} = ?" for k in fields)
    with get_db() as conn:
        conn.execute(
            f"UPDATE downloads SET {cols} WHERE job_id = ?",
            (*fields.values(), job_id),
        )


def finish_job(job_id, status, **fields):
    update_job(job_id, status=status, **fields)
    with get_db() as conn:
        conn.execute(
            "UPDATE downloads SET finished_at = datetime('now') WHERE job_id = ?",
            (job_id,),
        )


def get_job(job_id, owner_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM downloads WHERE job_id = ? AND owner_id = ?", (job_id, owner_id)
        ).fetchone()
    return dict(row) if row else None


def list_history(owner_id, limit=50):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT job_id, url, title, quality, status, error, filename, filesize, created_at, finished_at "
            "FROM downloads WHERE owner_id = ? ORDER BY id DESC LIMIT ?", (owner_id, limit)
        ).fetchall()
    return [dict(r) for r in rows]


def delete_history_entry(job_id, owner_id):
    with get_db() as conn:
        conn.execute("DELETE FROM downloads WHERE job_id = ? AND owner_id = ?", (job_id, owner_id))


def expired_files(minutes=60):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT job_id FROM downloads WHERE filename IS NOT NULL AND "
            "finished_at < datetime('now', ?)", (f"-{minutes} minutes",)
        ).fetchall()
        conn.execute(
            "UPDATE downloads SET filename = NULL WHERE filename IS NOT NULL AND "
            "finished_at < datetime('now', ?)", (f"-{minutes} minutes",)
        )
    return [row[0] for row in rows]


def record_event(event, platform, tool_slug, file_format=None):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO events (event, platform, tool_slug, format) VALUES (?, ?, ?, ?)",
            (event, platform, tool_slug, file_format),
        )


def metrics():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM downloads WHERE status = 'done'").fetchone()[0]
        failures = conn.execute("SELECT COUNT(*) FROM downloads WHERE status = 'error'").fetchone()[0]
        by_platform = conn.execute(
            "SELECT platform, COUNT(*) AS count FROM events WHERE event = 'download_completed' "
            "GROUP BY platform ORDER BY count DESC"
        ).fetchall()
        by_tool = conn.execute(
            "SELECT tool_slug, COUNT(*) AS count FROM events WHERE event = 'download_completed' "
            "GROUP BY tool_slug ORDER BY count DESC"
        ).fetchall()
        errors = conn.execute(
            "SELECT event, COUNT(*) AS count FROM events WHERE event IN "
            "('analysis_failed', 'processing_error', 'rate_limited') GROUP BY event"
        ).fetchall()
    return {"total_downloads": total, "failed_jobs": failures,
            "downloads_by_platform": [dict(row) for row in by_platform],
            "downloads_by_tool": [dict(row) for row in by_tool],
            "errors": [dict(row) for row in errors]}
