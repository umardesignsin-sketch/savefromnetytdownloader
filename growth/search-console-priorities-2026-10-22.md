# Search Console priorities, 2026-10-22

Source: Search Console Performance report for `sc-domain:savefromnet.fun`, last 3 months
(3 August to 19 October 2026): 12.3K clicks, 292K impressions, 4.2% CTR, average position 10.

## What performs

| Page (as reported) | Clicks | Impressions | Position | Main queries |
| --- | ---: | ---: | ---: | --- |
| www/youtube-video-downloader | 3,431 | 65,909 | 9.4 | save from net youtube, youtube video downloader (7.7K impr., pos. 10.2, 1.2% CTR) |
| / | 2,807 | 118,667 | 7.1 | save from net, savefromnet, save to net |
| */youtube-to-mp3 | 3,280 | 47,100 | 9.9 | save from net mp3, savefrom mp3 converter, youtube to mp3 |
| www/best-youtube-video-downloader | 656 | 11,033 | 16.0 | youtube video downloader, youtube downloader, "no ads" variants |
| www/y2mate-alternative | 435 | 6,530 | 7.0 | y2mate alternative (pos. 6.3), y2mate.com alternative, alternative to y2mate |
| www/compare/y2mate | 262 | 5,874 | 7.4 | mostly "savefrom.net / y2mate" comparisons |
| */facebook-video-downloader | 31 | 5,750 | 17.0 | save from net facebook videos (1.3K impr., 0.2% CTR) |

Countries: India 4,964 clicks; United States 1,142 (position 17.3); Indonesia 701; Pakistan 468;
United Kingdom 457 (position 17.6, 10.2% CTR); Canada 197.

## Changes made

- `/y2mate-alternative` is a real YouTube to MP3 and MP4 downloader page again instead of a redirect
  to the generic YouTube downloader. Its intent ranked at position 6–7. The page states that
  SaveFromNet is not affiliated with Y2Mate. `/compare/y2mate` now redirects there.
- `/youtube-video-downloader` has a title and description aimed at "youtube video downloader" and a
  "How to choose a YouTube video downloader" section, which absorbs the
  `/best-youtube-video-downloader` intent that already redirects to it.
- `/facebook-video-downloader` has a title and description naming videos, Reels, HD and SD.

## Deliberately unchanged

- The homepage title stays as protected by `test_priority_youtube_intents_keep_existing_canonicals`.
- No page targets the separate SaveFrom.net brand. Queries such as "savefrom.net / y2mate" come from
  name similarity; SaveFromNet does not claim to be that service.

## Next check

Compare these pages over the 28 days after 2026-10-22 against the 28 days before: clicks, CTR and
position for "youtube video downloader", "y2mate alternative" and "save from net facebook videos".
