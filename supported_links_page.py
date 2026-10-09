"""URL-shape reference generated from one reviewed platform table."""

from site_pages import Page, Section
from tools import BY_SLUG


SUPPORTED_URL_FAMILIES = (
    ("YouTube video, Shorts and music links", "youtube-downloader",
     "Use one youtube.com/watch?v=VIDEO_ID, youtube.com/shorts/VIDEO_ID, or youtu.be/VIDEO_ID link. A public music.youtube.com/watch?v=VIDEO_ID track is also recognized.",
     "A playlist, channel, search page, purchase, private upload or live stream is not one accessible finished file. Shorts, MP3, video and transcript tools each focus the result on a different task."),
    ("Instagram posts, Reels and Stories", "instagram-downloader",
     "Use one instagram.com/p/POST_ID or instagram.com/reel/REEL_ID link. An individual /stories/USERNAME/STORY_ID/ link or public profile URL has its own specialized tool.",
     "Stories expire and Instagram often requires sign-in even for media visible in its app. A feed or Explore page is not an individual post."),
    ("TikTok videos, photos and Stories", "tiktok-downloader",
     "Use one tiktok.com/@CREATOR/video/ID or /photo/ID link. Supported vm.tiktok.com and vt.tiktok.com short links can also identify a video; /@CREATOR/stories has a separate tool.",
     "A profile feed is not a single video. Some public posts are withheld from anonymous data-center requests, and Stories may expire."),
    ("Facebook videos and Reels", "facebook-video-downloader",
     "Use a public facebook.com/watch?v=ID, /videos/, /reel/, /share/v/, or /share/r/ link, or one fb.watch short link.",
     "Friends-only, group-only, deleted or login-gated videos cannot be fetched. A profile or group home page does not identify one finished video."),
    ("Pinterest Pins", "pinterest-video-downloader",
     "Use one pinterest.com/pin/NUMERIC_ID/ or pin.it/SHORT_ID link to a public Pin. The result may be an image, GIF or video depending on what that Pin actually exposes.",
     "Boards and search pages hold many Pins. A Pin that only previews a media file on another website does not make that external file available here."),
    ("Reddit posts", "reddit-video-downloader",
     "Use one reddit.com/r/COMMUNITY/comments/POST_ID/ or reddit.com/user/CREATOR/comments/POST_ID/ permalink, or a redd.it/POST_ID short link.",
     "A subreddit feed is not one post. Deleted, quarantined, adult-gated or private posts may be inaccessible; a link to an external host is not necessarily Reddit-hosted video."),
    ("Threads posts", "threads-video-downloader",
     "Use one threads.com/@CREATOR/post/POST_ID or threads.net/@CREATOR/post/POST_ID link to a public post.",
     "This tool can offer video only when the public post exposes a usable media URL. Many Threads posts do not expose video to anonymous requests."),
    ("Dailymotion videos", "dailymotion-video-downloader",
     "Use one dailymotion.com/video/VIDEO_ID or dai.ly/VIDEO_ID link to a public video.",
     "The source determines actual resolution and container. Private, removed or region-blocked videos do not yield a file here."),
)


SUPPORTED_LINKS_PAGE = Page(
    "supported-links", "Supported Media Links and URL Formats | SaveFromNet",
    "Check which YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads and Dailymotion URL shapes SaveFromNet accepts.",
    "Which media links does SaveFromNet support?",
    "Paste a direct link to one public media item you own or have permission to save. This reference lists URL shapes accepted by the site's validator; a valid link still needs the source to expose a usable file without sign-in.",
    tuple(Section(heading, (accepted, limitation), ((BY_SLUG[slug].path, "Open " + BY_SLUG[slug].name),))
          for heading, slug, accepted, limitation in SUPPORTED_URL_FAMILIES)
    + (Section("When a supported link returns no file", (
        "URL validation checks the platform and link shape before extraction. It cannot guarantee that a post remains public, has audio, provides a requested quality, or can be accessed from the processing server. The analyzer displays only formats actually found for the item.",
        "For an unknown platform, private item, playlist, account-only page, paywall or DRM-protected title, choose an authorized source rather than changing the link to imitate a supported URL. No arbitrary website fetch or account bypass is offered.",
    ), (("/universal-video-downloader", "Try automatic platform detection"), ("/guides/why-media-links-fail", "Troubleshoot an unavailable link"))),),
)
