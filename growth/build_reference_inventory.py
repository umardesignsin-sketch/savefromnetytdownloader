"""Snapshot VidsSave's public sitemap and linked URL architecture.

This records URLs and inferred intent, never source text or design assets.
Run explicitly; it is not part of the site build.
"""

import csv
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from xml.etree import ElementTree

import requests


BASE = "https://vidssave.com"
OUTPUT = Path(__file__).with_name("reference-url-gap.csv")
LOCALES = {"ar", "bn", "de", "es", "fr", "hi", "id", "it", "ja", "ko", "ms", "my", "pa", "pt", "ru", "ta", "te", "th", "tr", "ur", "vi"}

# Reference path -> SaveFromNet path, page type, primary intent, disposition.
# The two branded MP3 URLs requested for SaveFromNet stay out of this map until
# query-to-page Search Console data identifies the URLs already earning clicks.
MAP = {
    "/": ("/", "home", "general media download", "CONSOLIDATED"),
    "/home": ("/", "home alias", "general media download", "CONSOLIDATED"),
    "/index-3tz": ("/", "home", "general media download", "IMPLEMENTED"),
    "/youtube-video-downloader-10jq": ("/youtube-video-downloader", "tool", "YouTube video download", "IMPLEMENTED"),
    "/youtube-video-downloader-8hs": ("/youtube-video-downloader", "duplicate tool", "YouTube video download", "CONSOLIDATED"),
    "/youtube-shorts-download-1mf": ("/youtube-shorts-downloader", "tool", "YouTube Shorts download", "IMPLEMENTED"),
    "/youtube-shorts-download": ("/youtube-shorts-downloader", "tool alias", "YouTube Shorts download", "CONSOLIDATED"),
    "/yt-downloader-3bx": ("/youtube-downloader", "tool", "YouTube download", "IMPLEMENTED"),
    "/yt": ("/youtube-downloader", "tool alias", "YouTube download", "CONSOLIDATED"),
    "/youtube-to-mp3-4cy": ("/youtube-to-mp3", "converter", "YouTube to MP3", "IMPLEMENTED"),
    "/youtube-to-mp4-5du": ("/youtube-to-mp4", "converter", "YouTube to MP4", "IMPLEMENTED"),
    "/youtube-song-downloader-3bx": ("/youtube-song-downloader", "tool", "YouTube song audio", "IMPLEMENTED"),
    "/youtube-music-download-3bx": ("/youtube-music-downloader", "tool", "YouTube Music audio", "IMPLEMENTED"),
    "/youtube-audio-downloader-2az": ("/youtube-audio-downloader", "tool", "YouTube audio download", "IMPLEMENTED"),
    "/youtube-movies-2az": ("/youtube-movies-downloader", "tool", "public YouTube movie upload", "IMPLEMENTED"),
    "/facebook": ("/facebook-video-downloader", "tool", "Facebook video download", "IMPLEMENTED"),
    "/tiktok": ("/tiktok-downloader", "tool redirect", "TikTok download", "IMPLEMENTED"),
    "/tiktok-video-download": ("/tiktok-downloader", "tool alias", "TikTok video download", "CONSOLIDATED"),
    "/tiktok-to-mp3": ("/tiktok-to-mp3", "converter redirect", "TikTok to MP3", "IMPLEMENTED"),
    "/tiktok-mp3-download": ("/tiktok-to-mp3", "converter alias", "TikTok to MP3", "CONSOLIDATED"),
    "/tiktok-song-download": ("/tiktok-to-mp3", "converter alias", "TikTok audio download", "CONSOLIDATED"),
    "/tiktok-story-downloader": ("/tiktok-story-downloader", "tool", "TikTok Story download", "IMPLEMENTED"),
    "/ins": ("/instagram-downloader", "tool redirect", "Instagram download", "IMPLEMENTED"),
    "/ins/video": ("/instagram-video-downloader", "tool redirect", "Instagram video download", "IMPLEMENTED"),
    "/ins/reels": ("/instagram-reels-downloader", "tool redirect", "Instagram Reels download", "IMPLEMENTED"),
    "/ins/photo": ("/instagram-photo-downloader", "tool redirect", "Instagram photo download", "IMPLEMENTED"),
    "/ins/carousel": ("/instagram-carousel-downloader", "tool redirect", "Instagram carousel download", "IMPLEMENTED"),
    "/ins/profile": ("/instagram-profile-downloader", "tool redirect", "Instagram public profile media", "IMPLEMENTED"),
    "/ins/story": ("/instagram-story-downloader", "tool redirect", "Instagram Story download", "IMPLEMENTED"),
    "/video": ("/instagram-video-downloader", "tool alias", "Instagram video download", "CONSOLIDATED"),
    "/reels": ("/instagram-reels-downloader", "tool alias", "Instagram Reels download", "CONSOLIDATED"),
    "/photo": ("/instagram-photo-downloader", "tool alias", "Instagram photo download", "CONSOLIDATED"),
    "/carousel": ("/instagram-carousel-downloader", "tool alias", "Instagram carousel download", "CONSOLIDATED"),
    "/profile": ("/instagram-profile-downloader", "tool alias", "Instagram public profile media", "CONSOLIDATED"),
    "/story": ("/instagram-story-downloader", "tool alias", "Instagram Story download", "CONSOLIDATED"),
    "/reddit": ("/reddit-video-downloader", "tool", "Reddit video download", "IMPLEMENTED"),
    "/threads": ("/threads-video-downloader", "tool", "Threads public video download", "IMPLEMENTED"),
    "/pin-3bx": ("/pinterest-video-downloader", "tool", "Pinterest Pin media", "IMPLEMENTED"),
    "/pin": ("/pinterest-video-downloader", "tool alias", "Pinterest Pin media", "CONSOLIDATED"),
    "/pin/pinterest-gif-downloader": ("/pinterest-video-downloader", "format tool", "Pinterest GIF download", "CONSOLIDATED"),
    "/dailymotion-1mf": ("/dailymotion-video-downloader", "tool", "Dailymotion video download", "IMPLEMENTED"),
    "/dailymotion": ("/dailymotion-video-downloader", "tool alias", "Dailymotion video download", "CONSOLIDATED"),
    "/platform-supports": ("/universal-video-downloader", "platform directory", "all supported platforms", "CONSOLIDATED"),
    "/yt/why-cannot-i-download-youtube-videos": ("/guides/why-media-links-fail", "guide", "YouTube download failures", "CONSOLIDATED"),
    "/yt/how-to-download-youtube-shorts": ("/youtube-shorts-downloader", "guide", "how to save a Short", "CONSOLIDATED"),
    "/yt/how-to-extract-audio-from-youtube-video": ("/youtube-to-mp3", "guide", "YouTube audio extraction", "CONSOLIDATED"),
    "/yt/why-is-there-no-sound-after-downloading-youtube-video": ("/guides/youtube-video-formats", "guide", "YouTube video audio streams", "CONSOLIDATED"),
    "/ins/how-to-download-instagram-photos-in-hd": ("/instagram-photo-downloader", "guide", "Instagram photo quality", "CONSOLIDATED"),
    "/pin/why-is-pinterest-not-letting-me-download": ("/guides/pinterest-pin-media", "guide", "Pinterest download failures", "CONSOLIDATED"),
    "/tiktok/how-to-download-tiktok-sounds-1mf": ("/tiktok-to-mp3", "guide", "TikTok audio download", "CONSOLIDATED"),
    "/tiktok/how-to-download-tiktok-sounds": ("/tiktok-to-mp3", "guide alias", "TikTok audio download", "CONSOLIDATED"),
    "/about": ("/about", "trust page", "about the service", "IMPLEMENTED"),
    "/privacy": ("/privacy-policy", "policy", "privacy", "IMPLEMENTED"),
    "/terms": ("/terms", "policy", "terms of use", "IMPLEMENTED"),
    "/x": ("", "unsupported platform tool", "X video download", "NOT TECHNICALLY SUPPORTED"),
    "/twitter-gif-downloader": ("", "unsupported platform tool", "X GIF download", "NOT TECHNICALLY SUPPORTED"),
    "/extension": ("", "extension page", "browser extension", "NOT TECHNICALLY SUPPORTED"),
    "/extension/chrome": ("", "extension page", "Chrome extension", "NOT TECHNICALLY SUPPORTED"),
    "/topic/the-backrooms-movie": ("", "entertainment topic", "movie information", "NOT RELEVANT"),
}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.canonical = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
        elif tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href", "")


def same_site_links(url):
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "SaveFromNet architecture audit"})
        parser = LinkParser()
        parser.feed(response.text)
        links = set()
        for href in parser.hrefs:
            absolute = urljoin(url, href)
            parsed = urlsplit(absolute)
            if parsed.scheme == "https" and parsed.netloc == "vidssave.com" and not parsed.query:
                clean = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
                if not clean.endswith((".png", ".jpg", ".svg", ".webp", ".js", ".css")):
                    links.add(clean)
        return url, response.status_code, response.url, parser.canonical, links
    except requests.RequestException:
        return url, "unavailable", "", "", set()


def main():
    response = requests.get(BASE + "/sitemap.xml", timeout=20)
    response.raise_for_status()
    sitemap_urls = {node.text for node in ElementTree.fromstring(response.content).findall(".//{*}loc")}
    english = [url for url in sitemap_urls if urlsplit(url).netloc == "vidssave.com" and urlsplit(url).path.strip("/").split("/")[0] not in LOCALES]
    examined = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        for url, status, final_url, canonical, links in pool.map(same_site_links, english):
            examined[url] = (status, final_url, canonical, links)
    linked_urls = set().union(*(item[3] for item in examined.values())) if examined else set()
    all_urls = sitemap_urls | linked_urls
    fields = ("reference_url", "discovered_in", "http_status", "final_url", "reference_canonical",
              "page_type", "primary_search_intent", "primary_keyword", "parent_category",
              "related_reference_urls", "functionality", "seo_purpose", "savefromnet_url",
              "status", "indexable_on_savefromnet", "notes")
    with OUTPUT.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for url in sorted(all_urls):
            parsed = urlsplit(url)
            path = parsed.path.rstrip("/") or "/"
            segment = path.strip("/").split("/")[0]
            localized = parsed.netloc != "vidssave.com" or segment in LOCALES
            record = examined.get(url, ("not fetched", "", "", set()))
            if localized:
                target, kind, intent, disposition = "", "localized page", "language-specific search", "NOT RECOMMENDED"
                note = "No original, verified translation or locale-specific downloader is available; do not generate a thin locale page."
            elif path in MAP:
                target, kind, intent, disposition = MAP[path]
                note = "Mapped by supported function and intent; reference design and copy were not reused."
            else:
                target, kind, intent, disposition = "", "linked alias or ancillary page", "unverified distinct intent", "NOT RECOMMENDED"
                note = "Linked but not a distinct sitemap target; verify need and functionality before creating a page."
            parent = "locale: " + (parsed.netloc.split(".")[0] if parsed.netloc != "vidssave.com" else segment) if localized else (path.strip("/").split("/")[0] or "home")
            related = sorted(record[3] - {url})[:8]
            writer.writerow({
                "reference_url": url, "discovered_in": "sitemap" if url in sitemap_urls else "internal link",
                "http_status": record[0], "final_url": record[1], "reference_canonical": record[2],
                "page_type": kind, "primary_search_intent": intent, "primary_keyword": intent if not localized else "not analyzed",
                "parent_category": parent, "related_reference_urls": " | ".join(related),
                "functionality": "working downloader or content" if target else "not offered on SaveFromNet",
                "seo_purpose": "answer " + intent if target else "excluded to protect relevance and quality",
                "savefromnet_url": "https://savefromnet.fun" + target if target else "",
                "status": disposition, "indexable_on_savefromnet": "yes" if target else "no", "notes": note,
            })
    print(f"Wrote {len(all_urls)} reference URLs ({len(sitemap_urls)} sitemap, {len(linked_urls - sitemap_urls)} linked extras) to {OUTPUT}")


if __name__ == "__main__":
    main()
