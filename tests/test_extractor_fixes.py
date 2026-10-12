"""Format parsing and analysis fixes for Shorts, Facebook and Instagram sources."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_tmp = tempfile.TemporaryDirectory()
os.environ.setdefault("DB_PATH", str(Path(_tmp.name) / "test.db"))
os.environ.setdefault("DOWNLOAD_DIR", str(Path(_tmp.name) / "downloads"))

from app import app  # noqa: E402
from extractors import service  # noqa: E402
from extractors.service import AnalysisError, _yt_formats  # noqa: E402

YT_INFO = {"title": "Clip", "uploader": "Owner", "duration": 30, "formats": [
    {"format_id": "18", "ext": "mp4", "vcodec": "avc1", "acodec": "mp4a", "height": 360, "width": 640},
]}


class UnknownProgressiveFormatTests(unittest.TestCase):
    def test_facebook_sd_and_hd_without_details_are_offered_best_first(self):
        found = _yt_formats({"formats": [
            {"format_id": "sd", "ext": "mp4", "vcodec": None, "acodec": None},
            {"format_id": "hd", "ext": "mp4", "vcodec": None, "acodec": None},
        ]})
        videos = [item for item in found if item["type"] == "video"]
        self.assertEqual([item["quality"] for item in videos], ["HD", "SD"])
        self.assertEqual([item["_spec"]["selector"] for item in videos], ["hd", "sd"])
        self.assertTrue(all(item["resolution"] is None and item["filesize"] is None for item in videos))

    def test_silent_source_is_offered_only_when_allowed_and_labelled(self):
        info = {"formats": [
            {"format_id": "2", "ext": "mp4", "vcodec": None, "acodec": "none"},
            {"format_id": "dash-v", "ext": "mp4", "vcodec": "avc1", "acodec": "none", "height": 640, "width": 640},
        ]}
        self.assertEqual(_yt_formats(info), [])
        found = _yt_formats(info, allow_silent=True)
        self.assertEqual([item["quality"] for item in found], ["640p · no audio", "Source video · no audio"])

    def test_video_only_stream_is_not_offered_when_source_has_audio(self):
        found = _yt_formats({"formats": [
            {"format_id": "v", "ext": "mp4", "vcodec": "avc1", "acodec": "none", "height": 720},
            {"format_id": "a", "ext": "webm", "vcodec": "none", "acodec": "opus"},
        ]}, allow_silent=True)
        self.assertEqual([item for item in found if item["type"] == "video"], [])

    def test_audio_stream_without_video_details_is_not_a_video(self):
        found = _yt_formats({"formats": [{"format_id": "a", "ext": "mp4", "vcodec": None, "acodec": "mp4a"}]})
        self.assertEqual([item for item in found if item["type"] == "video"], [])


class AnalysisTypeTests(unittest.TestCase):
    def setUp(self):
        service._metadata_cache.clear()
        self.client = app.test_client()

    def test_shorts_link_works_with_shorts_tool_even_after_a_cached_watch_link(self):
        with patch("extractors.service._run", return_value=__import__("json").dumps(YT_INFO)) as run:
            watch = self.client.post("/api/analyze", json={"tool": "youtube-downloader",
                                     "url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ"})
            short = self.client.post("/api/analyze", json={"tool": "youtube-shorts-downloader",
                                     "url": "https://www.youtube.com/shorts/aqz-KE-bpKQ"})
        self.assertEqual(watch.status_code, 200)
        self.assertEqual(short.status_code, 200, short.get_json())
        self.assertEqual(short.get_json()["type"], "short")
        self.assertEqual(run.call_count, 1)  # the second request used the metadata cache

    def test_watch_link_is_still_refused_by_shorts_tool(self):
        response = self.client.post("/api/analyze", json={"tool": "youtube-shorts-downloader",
                                    "url": "https://www.youtube.com/watch?v=aqz-KE-bpKQ"})
        self.assertEqual(response.get_json()["code"], "wrong_content_type")


class InstagramFallbackTests(unittest.TestCase):
    def setUp(self):
        service._metadata_cache.clear()

    def test_public_video_post_falls_back_to_yt_dlp(self):
        video = {"platform": "instagram", "type": "post", "title": "Video", "formats": [
            {"id": "v0", "type": "video", "extension": "mp4", "quality": "640p",
             "_spec": {"engine": "yt-dlp", "selector": "v", "extension": "mp4"}}]}
        with patch("extractors.service._gallery_analyze", side_effect=AnalysisError("login", "no_formats")), \
                patch("extractors.service._yt_analyze", return_value=video) as yt:
            result = service.analyze("https://www.instagram.com/p/aye83DjauH/", "owner")
        yt.assert_called_once()
        self.assertEqual(result["formats"][0]["quality"], "640p")

    def test_photo_post_keeps_the_gallery_error_when_fallback_fails(self):
        with patch("extractors.service._gallery_analyze", side_effect=AnalysisError("No images.", "no_formats")), \
                patch("extractors.service._yt_analyze", side_effect=AnalysisError("yt", "source_unavailable")):
            with self.assertRaises(AnalysisError) as raised:
                service.analyze("https://www.instagram.com/p/BQ0eAlwhDrw/", "owner")
        self.assertEqual(raised.exception.code, "no_formats")

    def test_profiles_do_not_fall_back(self):
        with patch("extractors.service._gallery_analyze", side_effect=AnalysisError("login", "no_formats")), \
                patch("extractors.service._yt_analyze") as yt:
            with self.assertRaises(AnalysisError):
                service.analyze("https://www.instagram.com/nasa/", "owner")
        yt.assert_not_called()


if __name__ == "__main__":
    unittest.main()
