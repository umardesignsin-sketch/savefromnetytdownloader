# Legacy URL recovery — 2026-10-10

Search results still showed pages from SaveFromNet's previous transcript-focused site on `www.savefromnet.fun`. The `www` hostname correctly redirects to the apex while preserving paths, but sampled legacy paths then returned HTTP 404. In particular, `/clipconverter-alternative` and `/youtube-transcript-for/developers` had no replacement redirect.

The `_redirects` file now sends those paths and the old transcript-language and audience page families to the closest working canonical tool or API documentation. The observed old `/de` and `/pt` transcript homepages go to the working transcript tool. The Spanish and French homepages already exist and were not moved. No old page was added to the sitemap, and no existing indexable canonical was changed.

After deployment, verify each source returns HTTP 301 and the final page returns HTTP 200 with a self-canonical. Review Search Console's **Not found (404)** and **Page with redirect** reports over subsequent weeks for other old URLs with impressions or links. Add individual redirects only where a real equivalent exists; let unrelated dead pages return 404. Redirects help preserve relevant signals during a site move but cannot guarantee ranking gains.
