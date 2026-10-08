"""Render SEO pages once for Cloudflare's edge asset service.

Flask remains the local renderer and API; the Worker serves these pages without
starting a Container. Re-run before every Worker deployment.
"""

from pathlib import Path
import shutil

from app import app
from guides import GUIDES
from image_tools import IMAGE_TOOLS
from site_pages import PAGES
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
    pages = [("/", "index.html"), ("/batch-image-converter", "batch-image-converter.html"), ("/robots.txt", "robots.txt"),
             ("/sitemap.xml", "sitemap.xml"), ("/missing-page", "404.html")]
    pages += [(tool.path, f"{tool.slug}.html") for tool in TOOLS]
    pages += [(tool.path, f"{tool.slug}.html") for tool in IMAGE_TOOLS]
    pages += [("/guides", "guides.html")]
    pages += [(guide.path, f"guides/{guide.slug}.html") for guide in GUIDES]
    pages += [(page.path, f"{page.slug}.html") for page in PAGES]
    for route, filename in pages:
        response = client.get(route)
        expected = 404 if filename == "404.html" else 200
        if response.status_code != expected:
            raise RuntimeError(f"Could not render {route}: HTTP {response.status_code}")
        target = DIST / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(response.data)
    for name in ("css/site.css", "css/reference.css", "css/content.css", "css/image-tools.css", "css/batch-images.css", "css/transcript.css", "js/site.js", "js/visitor.js", "js/transcript.js", "js/image-tools.js", "js/batch-images.js", "js/size-estimator.mjs", "favicon.svg"):
        source = BASE / "static" / name
        target = DIST / "static" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(BASE / "sw.js", DIST / "sw.js")
    shutil.copy2(BASE / "_headers", DIST / "_headers")
    print(f"Rendered {len(TOOLS)} media tools, {len(IMAGE_TOOLS)} image tools, {len(GUIDES)} guides, {len(PAGES)} directory and trust pages, homepage, and site assets to {DIST}")


if __name__ == "__main__":
    main()
