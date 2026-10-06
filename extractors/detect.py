"""Strict, server-side URL detection. No arbitrary web URLs reach an extractor."""

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, quote, urlsplit


class DetectError(ValueError):
    pass


@dataclass(frozen=True)
class Detection:
    platform: str
    content_type: str
    normalized_url: str
    extractor: str

    def as_dict(self):
        return {"platform": self.platform, "contentType": self.content_type,
                "normalizedUrl": self.normalized_url, "extractor": self.extractor}


HOSTS = {
    "youtube.com": "youtube", "www.youtube.com": "youtube",
    "m.youtube.com": "youtube", "music.youtube.com": "youtube",
    "youtu.be": "youtube", "www.youtu.be": "youtube",
    "instagram.com": "instagram", "www.instagram.com": "instagram",
    "tiktok.com": "tiktok", "www.tiktok.com": "tiktok",
    "m.tiktok.com": "tiktok", "vm.tiktok.com": "tiktok",
    "vt.tiktok.com": "tiktok", "facebook.com": "facebook",
    "www.facebook.com": "facebook", "m.facebook.com": "facebook",
    "web.facebook.com": "facebook", "fb.watch": "facebook",
    "www.fb.watch": "facebook", "pinterest.com": "pinterest",
    "www.pinterest.com": "pinterest", "in.pinterest.com": "pinterest",
    "pin.it": "pinterest", "www.pin.it": "pinterest",
    "reddit.com": "reddit", "www.reddit.com": "reddit",
    "old.reddit.com": "reddit", "redd.it": "reddit",
    "www.redd.it": "reddit", "threads.net": "threads",
    "www.threads.net": "threads", "threads.com": "threads",
    "www.threads.com": "threads", "dailymotion.com": "dailymotion",
    "www.dailymotion.com": "dailymotion", "dai.ly": "dailymotion",
    "www.dai.ly": "dailymotion",
}
YT_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{2,100}$")
USER = re.compile(r"^[A-Za-z0-9._-]{1,40}$")


def _valid_user(value):
    return bool(USER.fullmatch(value) and value not in (".", "..") and not value.startswith("."))


def detect_url(raw):
    if not isinstance(raw, str) or not raw.strip():
        raise DetectError("Paste a public media URL to continue.")
    raw = raw.strip()
    if len(raw) > 2048 or any(ord(ch) < 32 or ch == "\\" for ch in raw):
        raise DetectError("That URL is invalid or too long.")
    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw
    try:
        url = urlsplit(raw)
        host = (url.hostname or "").lower().rstrip(".")
        port = url.port
    except ValueError as exc:
        raise DetectError("That URL could not be parsed.") from exc
    if url.scheme not in ("http", "https") or url.username or url.password or port:
        raise DetectError("Use a standard public HTTPS link without a port or sign-in details.")
    platform = HOSTS.get(host) or ("pinterest" if host.endswith(".pinterest.com") and host.count(".") <= 3 else None)
    if not platform:
        raise DetectError("This platform is not supported. Paste a link from a platform shown below.")
    path = url.path.rstrip("/") or "/"
    parts = [p for p in path.split("/") if p]
    query = parse_qs(url.query, keep_blank_values=False)

    def result(kind, canonical, extractor="yt-dlp"):
        return Detection(platform, kind, canonical, extractor)

    if platform == "youtube":
        video_id = (parts[0] if host.endswith("youtu.be") and len(parts) == 1 else
                    (query.get("v") or [""])[0] if path == "/watch" else
                    parts[1] if len(parts) == 2 and parts[0] in ("shorts", "live", "embed") else "")
        if not YT_ID.fullmatch(video_id):
            raise DetectError("Paste a link to one YouTube video, Short, or music track.")
        kind = "short" if parts and parts[0] == "shorts" else "video"
        return result(kind, f"https://www.youtube.com/watch?v={video_id}")

    if platform == "instagram":
        if len(parts) == 2 and parts[0] in ("p", "reel", "reels", "tv") and SAFE_ID.fullmatch(parts[1]):
            kind = "reel" if parts[0] in ("reel", "reels") else "post"
            return result(kind, f"https://www.instagram.com/{'reel' if kind == 'reel' else 'p'}/{parts[1]}/", "gallery-dl" if kind == "post" else "yt-dlp")
        if len(parts) == 3 and parts[0] == "stories" and _valid_user(parts[1]) and SAFE_ID.fullmatch(parts[2]):
            return result("story", f"https://www.instagram.com/stories/{parts[1]}/{parts[2]}/", "gallery-dl")
        if len(parts) == 1 and _valid_user(parts[0]) and parts[0] not in ("explore", "accounts", "stories", "reel", "p"):
            return result("profile", f"https://www.instagram.com/{parts[0]}/", "gallery-dl")
        raise DetectError("Paste a public Instagram post, Reel, Story, or profile link.")

    if platform == "tiktok":
        if len(parts) == 2 and parts[0].startswith("@") and _valid_user(parts[0][1:]) and parts[1] == "stories":
            return result("story", f"https://www.tiktok.com/{parts[0]}/stories", "gallery-dl")
        if host in ("vm.tiktok.com", "vt.tiktok.com") and len(parts) == 1 and SAFE_ID.fullmatch(parts[0]):
            return result("video", f"https://{host}/{parts[0]}/")
        if len(parts) == 3 and parts[0].startswith("@") and _valid_user(parts[0][1:]) and parts[1] in ("video", "photo") and parts[2].isdigit():
            kind = "video" if parts[1] == "video" else "photo"
            return result(kind, f"https://www.tiktok.com/{parts[0]}/{parts[1]}/{parts[2]}",
                          "gallery-dl" if kind == "photo" else "yt-dlp")
        if len(parts) == 2 and parts[0] == "t" and SAFE_ID.fullmatch(parts[1]):
            return result("video", f"https://www.tiktok.com/t/{parts[1]}/")
        raise DetectError("Paste a public TikTok video or photo link. Private stories are unavailable.")

    if platform == "facebook":
        if host.endswith("fb.watch") and len(parts) == 1 and SAFE_ID.fullmatch(parts[0]):
            return result("video", f"https://fb.watch/{parts[0]}/")
        if path == "/watch" and (query.get("v") or [""])[0].isdigit():
            return result("video", f"https://www.facebook.com/watch/?v={query['v'][0]}")
        if len(parts) == 3 and parts[0] == "share" and parts[1] in ("v", "r") and SAFE_ID.fullmatch(parts[2]):
            return result("video", f"https://www.facebook.com/share/{parts[1]}/{parts[2]}/")
        if len(parts) >= 2 and any(p in ("videos", "reel", "reels") for p in parts) and all(re.fullmatch(r"[A-Za-z0-9._-]+", p) for p in parts):
            return result("video", f"https://www.facebook.com/{'/'.join(parts)}/")
        raise DetectError("Paste a public Facebook video or Reel link.")

    if platform == "pinterest":
        if host.endswith("pin.it") and len(parts) == 1 and SAFE_ID.fullmatch(parts[0]):
            return result("pin", f"https://pin.it/{parts[0]}", "gallery-dl")
        if len(parts) == 2 and parts[0] == "pin" and parts[1].isdigit():
            return result("pin", f"https://www.pinterest.com/pin/{parts[1]}/", "gallery-dl")
        raise DetectError("Paste a link to one public Pinterest Pin.")

    if platform == "reddit":
        if host.endswith("redd.it") and len(parts) == 1 and SAFE_ID.fullmatch(parts[0]):
            return result("post", f"https://redd.it/{parts[0]}")
        if len(parts) >= 4 and parts[0] in ("r", "user") and re.fullmatch(r"[A-Za-z0-9_-]{1,40}", parts[1]) and parts[2] == "comments" and SAFE_ID.fullmatch(parts[3]):
            return result("post", f"https://www.reddit.com/{parts[0]}/{quote(parts[1])}/comments/{parts[3]}/")
        raise DetectError("Paste a public Reddit post link.")

    if platform == "threads":
        if len(parts) == 3 and parts[0].startswith("@") and _valid_user(parts[0][1:]) and parts[1] == "post" and SAFE_ID.fullmatch(parts[2]):
            return result("post", f"https://www.threads.com/{parts[0]}/post/{parts[2]}", "threads")
        raise DetectError("Paste a link to one public Threads post.")

    if platform == "dailymotion":
        video_id = parts[0] if host.endswith("dai.ly") and len(parts) == 1 else parts[1] if len(parts) == 2 and parts[0] == "video" else ""
        if not SAFE_ID.fullmatch(video_id):
            raise DetectError("Paste a Dailymotion video link.")
        return result("video", f"https://www.dailymotion.com/video/{video_id}")

    raise DetectError("Unsupported URL.")
