import sqlite3
from contextlib import contextmanager

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS downloads (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id      TEXT UNIQUE NOT NULL,
    url         TEXT NOT NULL,
    title       TEXT,
    quality     TEXT NOT NULL,
    status      TEXT NOT NULL,          -- queued | downloading | done | error
    error       TEXT,
    filename    TEXT,
    filesize    INTEGER,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_downloads_created ON downloads(created_at DESC);
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


def insert_job(job_id, url, quality):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO downloads (job_id, url, quality, status) VALUES (?, ?, ?, 'queued')",
            (job_id, url, quality),
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


def get_job(job_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM downloads WHERE job_id = ?", (job_id,)
        ).fetchone()
    return dict(row) if row else None


def list_history(limit=50):
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM downloads ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def delete_history_entry(job_id):
    with get_db() as conn:
        conn.execute("DELETE FROM downloads WHERE job_id = ?", (job_id,))
