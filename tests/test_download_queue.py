"""A busy download slot should queue a few jobs instead of refusing them."""
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

_tmp = tempfile.TemporaryDirectory()
os.environ.setdefault("DB_PATH", str(Path(_tmp.name) / "test.db"))
os.environ.setdefault("DOWNLOAD_DIR", str(Path(_tmp.name) / "downloads"))

import downloader  # noqa: E402

SPEC = {"engine": "yt-dlp", "selector": "18", "extension": "mp4"}


class DownloadQueueTest(unittest.TestCase):
    def setUp(self):
        downloader.JOBS.clear()

    def tearDown(self):
        downloader.JOBS.clear()

    def test_jobs_queue_until_queue_is_full(self):
        capacity = downloader.MAX_CONCURRENT_JOBS + downloader.MAX_QUEUED_JOBS
        with patch.object(downloader.db, "insert_job"), patch.object(downloader, "_run"):
            ids = [downloader.start("https://www.youtube.com/watch?v=jNQXAC9IVRw", "mp4", "owner", SPEC, "youtube", "youtube-to-mp4")
                   for _ in range(capacity + 1)]
        self.assertTrue(all(ids[:capacity]))
        self.assertIsNone(ids[capacity])
        self.assertTrue(all(downloader.JOBS[j]["stage"] == "Queued" for j in ids[:capacity]))

    def test_queued_job_fails_cleanly_when_no_slot_frees(self):
        job_id = "a" * 32
        downloader.JOBS[job_id] = {"status": "queued", "stage": "Queued"}
        slots = threading.BoundedSemaphore(1)
        slots.acquire()
        with patch.object(downloader, "_slots", slots), patch.object(downloader, "QUEUE_WAIT", 0.01), \
                patch.object(downloader.db, "finish_job"), patch.object(downloader, "_download") as download:
            downloader._run(job_id, "https://www.youtube.com/watch?v=jNQXAC9IVRw", "mp4", SPEC)
        download.assert_not_called()
        self.assertEqual(downloader.JOBS[job_id]["status"], "error")
        self.assertIn("busy", downloader.JOBS[job_id]["error"])


if __name__ == "__main__":
    unittest.main()
