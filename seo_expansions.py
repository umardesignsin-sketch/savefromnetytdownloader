"""Practical guidance for specialized downloader pages.

Keep this separate from the core tool registry so the copy can grow without
duplicating templates or changing the behavior of any extractor.
"""

TOOL_SECTIONS = {
    "youtube-audio-downloader": (
        ("Choose source audio or a converted MP3", (
            "Paste one public YouTube video, Short, or music.youtube.com/watch link. After analysis, this page shows audio choices only. An original M4A or WebM track may be available alongside an MP3 conversion; the list depends on the streams returned for that particular upload.",
            "Choose the original audio when you want to avoid another conversion. Choose MP3 when your player or editor needs that file type. The MP3 is made from the accessible source track, so a higher output setting cannot restore sound detail the upload never contained.",
        )),
        ("When the audio track is unavailable", (
            "A silent upload has no sound to extract. Some music videos also require sign-in, are limited by region, or are removed. This tool cannot use an account, bypass a restriction, or turn a playlist into one file. Try the direct link to a single public item you have permission to save.",
        )),
    ),
    "youtube-song-downloader": (
        ("Save audio from one permitted song upload", (
            "Use the direct watch-page, Shorts, or youtu.be link for one public upload that you own or are allowed to download. The tool checks the audio stream for that item and presents only the original audio or MP3 conversion it can prepare. It does not search a music catalog or download an entire playlist.",
        )),
        ("Check the source before choosing a file", (
            "An original audio stream may be M4A or WebM. MP3 requires a conversion, and converting a compressed source does not improve its fidelity. Official tracks and music videos can be region restricted or require an account even when a preview is visible; in that case there is no downloadable result here.",
        )),
    ),
    "youtube-music-downloader": (
        ("Use a direct YouTube Music track link", (
            "Paste a public music.youtube.com/watch?v= link to one track page. SaveFromNet validates the video ID and checks whether an audio stream is accessible without signing in. When it is, the result shows source audio formats and an MP3 conversion rather than a fixed list of promised bitrates.",
        )),
        ("Why a track may not appear", (
            "A subscription-only, region-limited, deleted, or account-gated track may play in your signed-in browser but remain unavailable to this anonymous service. Album, artist, and playlist pages are not single-track URLs. Use a direct public track link and download only music you own or have permission to save.",
        )),
    ),
    "youtube-movies-downloader": (
        ("Public uploads are different from rentals", (
            "This video-only tool accepts the watch-page URL of one publicly accessible movie upload that you own or are allowed to download. It checks the actual video streams and lists only complete video choices it can prepare within the 512 MB processing limit. Long uploads may exceed that limit even at a resolution visible in the player.",
        )),
        ("What this movie tool cannot process", (
            "Paid rentals and purchases, DRM-protected titles, age-gated videos, private uploads, and live streams are outside this service. It does not use your YouTube account or bypass a paywall. For a permitted short clip with a direct link, use the ordinary YouTube Video Downloader if this page returns no eligible movie format.",
        )),
    ),
    "instagram-video-downloader": (
        ("Find video in a public post", (
            "Paste one instagram.com/p/ or instagram.com/reel/ link that contains video. The analyzer checks the media returned for that item, then this page filters the result to video files. A photo-only post has no video option; use the photo downloader for still images instead.",
        )),
        ("Why a visible post can still fail", (
            "Instagram sometimes lets a signed-in browser display a post while withholding its files from anonymous extraction. Private, removed, or login-gated media cannot be fetched here. Copy the post or Reel URL itself rather than a feed, Explore page, or profile URL, and save only media you may use.",
        )),
    ),
    "instagram-photo-downloader": (
        ("Save an original image item", (
            "Use a direct public instagram.com/p/ link to a photo or a mixed-media post. This page displays only image items returned by the source, with each accessible item offered separately. It does not convert a video frame into a photo or invent a higher-resolution image than the public source provides.",
        )),
        ("Photos in a carousel", (
            "If a post contains several images, the analyzer can list the accessible items individually, up to the service's 12-item limit. For a post that mixes photos and videos, use the Instagram Carousel Downloader to compare both media types. Private or sign-in-gated posts cannot be retrieved here.",
        )),
    ),
    "instagram-story-downloader": (
        ("Use the link to one Story item", (
            "Paste a direct instagram.com/stories/username/story-id/ URL. A profile link or a link to the Stories tray does not identify one Story item. If that specific item is publicly accessible to the extractor, the result shows its actual image or video file.",
        )),
        ("Story access changes quickly", (
            "Stories expire and often require an Instagram account, even when the profile itself is public. This service does not sign in or bypass a private account. If analysis reports no accessible media, check that the Story is still live and that you copied its individual URL; an expired Story cannot be recovered here.",
        )),
    ),
    "instagram-profile-downloader": (
        ("Inspect a public profile, one item at a time", (
            "Paste an instagram.com/username/ profile URL. The extractor may return up to 12 publicly accessible media items, each shown as an individual image or video choice. This is a limited preview of what the source exposes anonymously, not a complete account backup.",
        )),
        ("When a profile shows no files", (
            "Instagram frequently requires sign-in to browse a profile feed, and private profiles are unavailable. An account page can also exist while exposing no media to this service. For one known public post, use its direct /p/ or /reel/ link with the relevant downloader instead.",
        )),
    ),
    "tiktok-story-downloader": (
        ("Check a public TikTok Story feed", (
            "Paste a tiktok.com/@username/stories link. The gallery extractor checks only the accessible Story items and presents the image or video files it actually returns, up to 12 items. A standard /video/id link belongs in the TikTok Downloader instead.",
        )),
        ("If the Story has disappeared", (
            "TikTok Stories are temporary and can be limited to certain viewers. A public-looking account may still withhold Stories from an anonymous request. This tool cannot recover an expired Story or sign in as a viewer; use a current public link to media you own or may download.",
        )),
    ),
}


TOOL_LINKS = {
    "youtube-audio-downloader": (("/youtube-to-mp3", "MP3-only conversion"), ("/guides/mp3-vs-m4a", "Compare MP3 and M4A")),
    "youtube-song-downloader": (("/youtube-audio-downloader", "Compare source audio"), ("/guides/mp3-vs-m4a", "Choose an audio format")),
    "youtube-music-downloader": (("/youtube-to-mp3", "YouTube to MP3 converter"), ("/youtube-audio-downloader", "Original audio options")),
    "youtube-movies-downloader": (("/youtube-video-downloader", "Standard video downloads"), ("/guides/video-file-size-estimates", "Estimate video file size")),
    "instagram-video-downloader": (("/instagram-reels-downloader", "Reels downloader"), ("/instagram-photo-downloader", "Photo posts")),
    "instagram-photo-downloader": (("/instagram-carousel-downloader", "Mixed-media carousels"), ("/guides/instagram-public-media", "Public Instagram links")),
    "instagram-story-downloader": (("/guides/instagram-public-media", "Instagram access guide"), ("/instagram-reels-downloader", "Reels downloader")),
    "instagram-profile-downloader": (("/instagram-downloader", "Individual Instagram posts"), ("/guides/instagram-public-media", "Instagram access guide")),
    "tiktok-story-downloader": (("/tiktok-downloader", "TikTok videos and photos"), ("/guides/tiktok-video-and-audio", "TikTok link guide")),
}
