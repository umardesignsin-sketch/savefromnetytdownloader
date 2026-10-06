"""Render SEO pages once for Cloudflare's edge asset service.

Flask remains the local renderer and API; the Worker serves these pages without
starting a Container. Re-run before every Worker deployment.
"""

from pathlib import Path
import shutil

from app import app
from tools import TOOLS

BASE = Path(__file__).resolve().parent
DIST = BASE / "dist"


def main():
    resolved = DIST.resolve()
    if resolved.parent != BASE or resolved.name != "dist":
        raise RuntimeError("Refusing to write outside the project")
    if DIST.exists():
        shutil.rmtree(resolved)
    DIST.mkdir()
    client = app.test_client()
    pages = [("/", "index.html"), ("/robots.txt", "robots.txt"),
             ("/sitemap.xml", "sitemap.xml"), ("/missing-page", "404.html")]
    pages += [(tool.path, f"{tool.slug}.html") for tool in TOOLS]
    for route, filename in pages:
        response = client.get(route)
        expected = 404 if filename == "404.html" else 200
        if response.status_code != expected:
            raise RuntimeError(f"Could not render {route}: HTTP {response.status_code}")
        (DIST / filename).write_bytes(response.data)
    for name in ("css/site.css", "js/site.js", "favicon.svg"):
        source = BASE / "static" / name
        target = DIST / "static" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(f"Rendered {len(TOOLS)} tool pages, homepage, and site assets to {DIST}")


if __name__ == "__main__":
    main()
