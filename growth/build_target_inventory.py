"""Refresh the target URL inventory from the site's real rendered routes.

Existing change labels are retained so a rerun never silently rewrites the
history of which URLs existed before an SEO expansion.
"""

import csv
import os
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path


OUTPUT = Path(__file__).with_name("savefromnet-url-inventory.csv")
BASE = "https://savefromnet.fun"
FIELDS = ("url", "page_type", "change", "http_status", "title", "h1", "canonical", "robots")


class PageInfo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = None
        self.title = ""
        self.h1 = ""
        self.canonical = ""
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag in ("title", "h1"):
            self.active = tag
        if tag == "link" and "canonical" in attributes.get("rel", "").split():
            self.canonical = attributes.get("href", "")
        if tag == "meta" and attributes.get("name") == "robots":
            self.noindex = "noindex" in attributes.get("content", "").lower()

    def handle_endtag(self, tag):
        if tag == self.active:
            self.active = None

    def handle_data(self, data):
        if self.active == "title":
            self.title += data
        elif self.active == "h1":
            self.h1 += data


def main():
    previous = {}
    if OUTPUT.exists():
        with OUTPUT.open(encoding="utf-8", newline="") as handle:
            previous = {row["url"]: row["change"] for row in csv.DictReader(handle)}

    with tempfile.TemporaryDirectory() as temporary:
        os.environ["DB_PATH"] = str(Path(temporary) / "inventory.db")
        os.environ["DOWNLOAD_DIR"] = str(Path(temporary) / "downloads")
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from app import app  # Imported after temporary paths are configured.
        from guides import GUIDES
        from site_pages import PAGES
        from tools import TOOLS

        routes = [("/", "home"), ("/guides", "guide hub")]
        routes += [(tool.path, "tool") for tool in TOOLS]
        routes += [(guide.path, "guide") for guide in GUIDES]
        routes += [(page.path, "directory" if page.slug == "tools" else "trust") for page in PAGES]
        client = app.test_client()
        rows = []
        for path, page_type in routes:
            response = client.get(path)
            if response.status_code != 200:
                raise RuntimeError(f"{path} returned HTTP {response.status_code}")
            info = PageInfo()
            info.feed(response.get_data(as_text=True))
            url = BASE + path
            if not info.title or not info.h1 or info.canonical != url or info.noindex:
                raise RuntimeError(f"Incomplete indexable page: {path}")
            rows.append({"url": url, "page_type": page_type,
                         "change": previous.get(url, "new"), "http_status": 200,
                         "title": info.title.strip(), "h1": info.h1.strip(),
                         "canonical": info.canonical, "robots": "indexable"})

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Updated {OUTPUT} with {len(rows)} canonical pages")


if __name__ == "__main__":
    main()
