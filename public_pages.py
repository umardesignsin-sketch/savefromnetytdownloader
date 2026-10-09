"""Canonical public page registry used by Flask, static rendering, and audits."""

from site_pages import PAGES as BASE_PAGES, TOOL_GROUPS
from supported_links_page import SUPPORTED_LINKS_PAGE
from utility_pages import UTILITY_PAGES


PAGES = (SUPPORTED_LINKS_PAGE,) + UTILITY_PAGES + BASE_PAGES
BY_SLUG = {page.slug: page for page in PAGES}
