"""Editorial guides grounded in the downloader's actual public URL support."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Guide:
    slug: str
    title: str
    description: str
    intro: str
    tool_slug: str
    sections: tuple
    faq: tuple

    @property
    def path(self):
        return f"/guides/{self.slug}"


GUIDES = (
    Guide(
        "youtube-video-formats", "YouTube video formats: MP4, WebM and audio",
        "Understand why YouTube video qualities and audio formats vary, and how SaveFromNet shows the choices available for a public upload.",
        "A YouTube link does not have one universal download file. The uploader, source and playback format determine which streams can be accessed. Analyze one public video before choosing a file.",
        "youtube-video-downloader",
        (
            ("Why 1080p can need two streams", "A higher-resolution picture and its audio are often delivered separately. If both streams are available, SaveFromNet can combine them into one downloadable video. It will not show a video-only stream as a finished file when it cannot also get audio."),
            ("MP4 and WebM are containers, not quality guarantees", "A 720p MP4 and a 720p WebM can differ in codec, bitrate and size. The result card reports the actual container and height returned for that upload. A requested height may be absent even if another YouTube video offers it."),
            ("Picking a practical file", "Start with a resolution your device can play and a file size you can store. The service caps a prepared file at 512 MB, so very long or high-bitrate videos may omit large options. Estimated sizes appear only when source information supports an estimate."),
        ),
        (("Can I choose 4K for every video?", "No. A 4K option appears only when the source exposes one that fits the service limit."),
         ("Why is MP3 listed separately?", "MP3 is a conversion from accessible audio, while M4A or WebM audio may come from the original source.")),
    ),
    Guide(
        "instagram-public-media", "Instagram posts, Reels, carousels and Stories",
        "Learn which public Instagram links SaveFromNet accepts and why different post types produce different downloadable items.",
        "Instagram uses several link types for media. A single post, a Reel, a carousel and a Story do not expose the same files, so the first step is to copy the link to the exact item you need.",
        "instagram-downloader",
        (
            ("Match the link to the media", "Use an instagram.com/p/ link for a post or carousel, and an instagram.com/reel/ link for a Reel. A carousel may return multiple images or videos; each accessible item is listed separately, up to 12 items. A video-only post does not create a photo option."),
            ("Stories and profiles have different limits", "A Story needs its individual story link, including the story ID. Stories expire and commonly require sign-in. A public profile link can expose a small set of recent items, but many profile feeds require login and cannot be read here."),
            ("What to do when analysis finds nothing", "Open the same link in a signed-out browser window. If it asks for login or the item is private, SaveFromNet cannot bypass that restriction. If it is public, retry the direct post link rather than a share page or a link to the profile."),
        ),
        (("Does a carousel download as one archive?", "No. Accessible carousel items are shown as individual file choices."),
         ("Can I access private Stories?", "No. This service does not use an Instagram account or bypass private content.")),
    ),
    Guide(
        "tiktok-video-and-audio", "TikTok video, photo posts and MP3 audio",
        "See how public TikTok video, photo and Story links differ, and when an MP3 conversion can actually be offered.",
        "A TikTok URL can refer to a video, a photo post or a Story. SaveFromNet validates the link type before analysis and only displays files returned by the public source.",
        "tiktok-downloader",
        (
            ("Use the direct post URL", "A video link usually contains /@username/video/ followed by a numeric ID. Photo posts use /photo/ instead. Supported vm.tiktok.com and vt.tiktok.com short links can also be analyzed. A creator profile or feed URL is not the same as an individual post."),
            ("Audio conversion depends on the clip", "The TikTok to MP3 tool converts audio from an accessible public video. It cannot make a meaningful MP3 from a silent clip, a photo post without audio, or a post that the source refuses to serve. No fixed audio bitrate is promised."),
            ("Why a public post may still fail", "TikTok can restrict requests from data-center networks, change how pages are served, or remove a post. Stories expire and may require sign-in. If analysis fails, verify the exact post is still publicly reachable; this service does not ask for account credentials."),
        ),
        (("Can I paste a TikTok profile?", "Use a link to one supported video or photo post instead."),
         ("Will every video offer MP3?", "Only videos with accessible audio can produce an MP3 option.")),
    ),
    Guide(
        "facebook-public-videos", "Finding a usable public Facebook video link",
        "A practical guide to Facebook watch, Reel and shared video URLs, plus the access limits that can stop extraction.",
        "Facebook has several ways to share the same video. SaveFromNet accepts public watch, Reel and video-post links, but it cannot see media reserved for friends, groups or signed-in viewers.",
        "facebook-video-downloader",
        (
            ("Copy the video, not the surrounding page", "A facebook.com/watch?v= link, a public /videos/ or /reel/ link, and an fb.watch short link are supported shapes. A general profile or group home page does not identify one video. Open the post itself and copy its direct link."),
            ("Check public access first", "Try the URL in a signed-out browser session. If Facebook asks you to log in, says the post is unavailable, or shows it only to friends, an anonymous extractor cannot fetch it. Sharing settings belong to the publisher and are not changed here."),
            ("Choose from the returned formats", "Video height, container and estimated size depend on the post. The result card is populated after analysis; it does not promise HD for every upload. A source-side change or region restriction can make even a public-looking link unavailable."),
        ),
        (("Can I save friends-only posts?", "No. Only media available without signing in can be processed."),
         ("Does a Facebook Reel use a separate tool?", "Public Reel links can be analyzed in the Facebook Video Downloader.")),
    ),
    Guide(
        "pinterest-pin-media", "Pinterest Pins: images, GIFs and video",
        "Understand the difference between Pinterest-hosted media and Pins that lead to an external website.",
        "A Pin may contain a still image, an animated GIF, a video or a link to another site. Analyze the exact Pin to learn which file, if any, Pinterest exposes publicly.",
        "pinterest-video-downloader",
        (
            ("Use one Pin URL", "Paste a pinterest.com/pin/ link with its numeric Pin ID, or a pin.it short link. A board, search result or creator profile contains many Pins and is not a single media item. Opening the Pin before copying its link avoids ambiguity."),
            ("Do not infer a video from the preview", "Some Pins display a preview from an external website rather than hosting that media themselves. SaveFromNet only offers media it can actually extract from the supported public Pin. It may return an image, GIF or video; it does not scrape the linked destination."),
            ("What the file label means", "The image or video extension comes from the source metadata. A GIF may be a true GIF file, while an animated preview on the Pinterest page could be represented differently. Check the returned format before starting a download."),
        ),
        (("Can I download a whole Pinterest board?", "No. Paste a link to one public Pin at a time."),
         ("Why do I only see an image?", "That may be the only accessible media item for that Pin, even if it links to a separate video elsewhere.")),
    ),
    Guide(
        "reddit-video-with-audio", "Why Reddit video and audio may need merging",
        "Learn how public Reddit post URLs, separate audio streams and unavailable posts affect a finished video download.",
        "Reddit video posts can expose picture and sound as separate streams. SaveFromNet inspects the post and offers a finished video only when the needed source streams can be prepared together.",
        "reddit-video-downloader",
        (
            ("Copy the post permalink", "Use a reddit.com/r/community/comments/post-id/ link or a redd.it short link to one post. A subreddit feed is not a media URL. The service checks that the link points to an allowed public Reddit post before contacting the extractor."),
            ("What happens to separate audio", "If a usable video stream and audio stream are returned, the server can merge them into one file. A video-only source with no matching audio is not presented as an ordinary finished video with sound. Available heights are taken from the actual post."),
            ("When the post is not accessible", "Deleted, quarantined, adult-gated or otherwise restricted posts may not be visible to the anonymous server. A post can also point to an external host rather than contain Reddit media. Check the original post and its permissions before retrying."),
        ),
        (("Why is my downloaded video silent?", "The source may have no accessible audio track; the result should only offer formats it can prepare from available streams."),
         ("Can I download a whole subreddit?", "No. The tool accepts one public post permalink at a time.")),
    ),
    Guide(
        "threads-video-availability", "When a Threads post exposes a public video",
        "Understand the narrow public-video case supported by the Threads tool and why many posts cannot be downloaded.",
        "The Threads tool has a narrower job than the other platform extractors. It looks for a public video URL in the post's page metadata and offers that file only when the source exposes it.",
        "threads-video-downloader",
        (
            ("Use the individual post link", "A supported link identifies one post, such as threads.com/@username/post/post-id. A profile or feed URL cannot tell the tool which media item you want. Older threads.net links are recognized and normalized to the current post shape."),
            ("Why a visible clip can be unavailable", "A browser can show content after sign-in or through client-side requests while the public page metadata contains no video. This extractor does not emulate an account or bypass that gap. It only follows a secure media URL on Meta's expected media hosts."),
            ("What a successful result contains", "When a public video is exposed, the result offers its source MP4 file. Resolution, duration and file size may be unknown because the page metadata does not provide those values. The tool does not invent extra quality buttons."),
        ),
        (("Can it download private Threads posts?", "No. It reads only public page metadata without an account."),
         ("Why are there no 720p or 1080p buttons?", "Threads page metadata often exposes just one source video URL, without a quality ladder.")),
    ),
    Guide(
        "dailymotion-video-quality", "Choosing Dailymotion video quality",
        "See how Dailymotion links are analyzed and why the available quality can differ from the number shown in a player.",
        "A Dailymotion video may have several streams, but a downloader should only show formats it can actually prepare. Analyze one public video to see its returned heights and file types.",
        "dailymotion-video-downloader",
        (
            ("Recognized video links", "Use a dailymotion.com/video/video-id link or its dai.ly short form. Playlist and channel pages identify collections, not one item. The URL detector normalizes these shapes before the extractor runs. Copy the address from the individual video's page for the clearest result."),
            ("Read the quality list after analysis", "The result can include MP4 or WebM options with different heights, depending on the source response. A 1080p player label is not a guarantee that an anonymous extractor receives a downloadable 1080p stream. Missing options are intentionally omitted."),
            ("Account and region limits", "A private, deleted or geographically blocked video may fail even when its link has the right shape. The service does not sign in or route around country restrictions. For a legitimate public video, retry its direct URL if a share link does not work."),
        ),
        (("Does every Dailymotion video have HD?", "No. Only heights returned for that particular video are shown."),
         ("Can I paste a Dailymotion playlist?", "Use the link to one video instead.")),
    ),
    Guide(
        "mp3-vs-m4a", "MP3 vs M4A for a video-to-audio conversion",
        "Compare MP3 conversion with source M4A audio and choose a file based on compatibility, source quality and size.",
        "Extracting audio and converting audio are different steps. A source may already provide M4A or WebM audio; an MP3 option is made from an accessible audio stream when the service can process it.",
        "youtube-to-mp3",
        (
            ("When MP3 is convenient", "MP3 plays on a wide range of devices and editing tools. Conversion is useful if your player needs that format. It cannot increase the detail of a low-quality source, and re-encoding may add loss compared with keeping an original compatible stream."),
            ("When an original track is preferable", "If the result offers M4A or another source audio file and your device supports it, that option can avoid an extra conversion. The exact track and bitrate depend on the source. The page never promises a fixed 320 kbps output."),
            ("Compare the actual choices", "Analyze the video, then look at the available extension, bitrate when known and estimated size when available. Use the dedicated audio or MP3 tool for the format you need. A silent or inaccessible video cannot produce a useful audio file."),
        ),
        (("Does converting to MP3 improve sound quality?", "No. Conversion cannot restore detail missing from the source audio."),
         ("Why is no MP3 listed?", "The source may have no accessible audio, or the item may be restricted or unavailable.")),
    ),
    Guide(
        "why-media-links-fail", "Why a public media link may fail to download",
        "Troubleshoot invalid links, private posts, missing audio, region limits, expired Stories and temporary source errors.",
        "A valid-looking URL is only the first requirement. The source also has to expose the media anonymously, and the requested file must be within the service's processing limits.",
        "universal-video-downloader",
        (
            ("Start with the exact item URL", "Copy the post or video permalink, not a profile, feed, playlist or search page. The supported host and path are validated before any extraction. Short links from supported platforms are accepted where the detector has a safe URL shape."),
            ("Check access without your account", "Open the link in a private browser window. If it requires login, belongs to a private account, has expired, or is unavailable in the server's region, SaveFromNet cannot bypass the restriction. Deleted and live media are also unsupported while unavailable."),
            ("If the format list is empty", "The extractor may see the post but receive no usable video, image or audio stream. A photo post will not offer video; a silent clip will not offer MP3. Source sites can change their public responses or temporarily block server traffic, so retry later if the item is truly public."),
        ),
        (("Can the site use my login to fetch it?", "No. The downloader does not accept account credentials or cookies."),
         ("Can I download DRM-protected or purchased media?", "No. The service does not bypass DRM, paywalls or other access controls.")),
    ),
)

BY_SLUG = {guide.slug: guide for guide in GUIDES}
