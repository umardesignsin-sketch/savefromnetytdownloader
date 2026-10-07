"""Caption extraction, safety and transcript-page contract checks."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_temp = tempfile.TemporaryDirectory()
os.environ.setdefault("DB_PATH", str(Path(_temp.name) / "transcript-test.db"))
os.environ.setdefault("DOWNLOAD_DIR", str(Path(_temp.name) / "downloads"))

from app import app  # noqa: E402
from extractors.detect import DetectError  # noqa: E402
from extractors.service import AnalysisError  # noqa: E402
from transcripts import get_transcript, parse_vtt  # noqa: E402


SAMPLE_VTT = """WEBVTT
Kind: captions
Language: en

00:00:08.829 --> 00:00:10.200
<v Speaker>First &amp; second</v>

00:00:10.729 --> 00:00:16.900 align:start
Next line
continues here
"""


class TranscriptTests(unittest.TestCase):
    def test_vtt_cues_keep_timing_and_clean_caption_markup(self):
        self.assertEqual(parse_vtt(SAMPLE_VTT), [
            {"start_ms": 8829, "end_ms": 10200, "text": "First & second"},
            {"start_ms": 10729, "end_ms": 16900, "text": "Next line continues here"},
        ])

    def test_only_allowlisted_youtube_video_reaches_extractor(self):
        with patch("transcripts._run") as run:
            for url in ("http://127.0.0.1/", "https://evil.example/video", "https://www.youtube.com/playlist?list=PL123"):
                with self.subTest(url=url), self.assertRaises(DetectError):
                    get_transcript(url)
            run.assert_not_called()

    def test_real_caption_track_is_selected_and_temp_file_removed(self):
        metadata = {"title": "Public example", "channel": "Example channel", "duration": 20,
                    "subtitles": {"en": [{"ext": "vtt"}], "fr": [{"ext": "vtt"}]},
                    "automatic_captions": {"en": [{"ext": "vtt"}]}}
        output_file = None

        def run(command, timeout=35):
            nonlocal output_file
            self.assertEqual(command[-2:], ["--", "https://www.youtube.com/watch?v=PRU2ShMzQRg"])
            if "--dump-single-json" in command:
                return json.dumps(metadata)
            self.assertIn("--skip-download", command)
            self.assertEqual(command[command.index("--sub-langs") + 1], "^en$")
            output_file = Path(command[command.index("--output") + 1].replace("%(ext)s", "en.vtt"))
            output_file.write_text(SAMPLE_VTT, encoding="utf-8")
            return ""

        with patch("transcripts._run", side_effect=run):
            result = get_transcript("https://youtu.be/PRU2ShMzQRg")
        self.assertEqual(result["language"], "en")
        self.assertEqual(result["kind"], "manual")
        self.assertEqual(len(result["segments"]), 2)
        self.assertFalse(output_file.exists())

    def test_missing_captions_and_unavailable_language_are_honest(self):
        metadata = {"title": "Example", "subtitles": {"en": [{"ext": "vtt"}]}, "automatic_captions": {}}
        with patch("transcripts._run", return_value=json.dumps(metadata)) as run:
            with self.assertRaises(AnalysisError) as raised:
                get_transcript("https://youtu.be/PRU2ShMzQRg", "de")
            self.assertEqual(raised.exception.code, "invalid_language")
            self.assertEqual(run.call_count, 1)
        with patch("transcripts._run", return_value=json.dumps({"title": "No captions"})):
            with self.assertRaises(AnalysisError) as raised:
                get_transcript("https://youtu.be/PRU2ShMzQRg")
            self.assertEqual(raised.exception.code, "no_captions")

    def test_page_and_api_have_distinct_real_transcript_behavior(self):
        client = app.test_client()
        page = client.get("/youtube-to-transcript").get_data(as_text=True)
        self.assertIn("<title>YouTube to Transcript Converter | SaveFromNet</title>", page)
        self.assertIn('<link rel="canonical" href="https://savefromnet.fun/youtube-to-transcript">', page)
        self.assertIn('<h1 id="download-heading">YouTube to Transcript Converter</h1>', page)
        self.assertIn('id="transcript-form"', page)
        self.assertIn('src="/static/js/transcript.js"', page)
        self.assertIn("A video without captions cannot be transcribed", page)
        self.assertEqual(client.get("/sitemap.xml").get_data(as_text=True).count(
            "<loc>https://savefromnet.fun/youtube-to-transcript</loc>"), 1)
        self.assertIn('href="/youtube-to-transcript"', client.get("/tools").get_data(as_text=True))
        response = client.post("/api/transcript", json={"url": "https://example.com/video"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["code"], "invalid_url")


if __name__ == "__main__":
    unittest.main()
