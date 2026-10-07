"""Single source of truth for the 25 public downloader experiences."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Tool:
    slug: str
    platform: str
    name: str
    description: str
    content_types: tuple
    format_note: str
    url_hint: str
    problem: str
    related: tuple = ()

    @property
    def path(self):
        return "/" + self.slug

    @property
    def heading(self):
        return {
            "youtube-to-mp3": "YouTube to MP3 Converter",
            "tiktok-to-mp3": "TikTok to MP3 Converter",
            "universal-video-downloader": "Universal Video Downloader & Converter",
        }.get(self.slug, self.name)

    @property
    def seo_title(self):
        return f"{self.heading} | SaveFromNet"

    @property
    def seo_description(self):
        return (self.description + " Analyze a public URL to see the formats actually available.")[:160]

    @property
    def faq(self):
        if self.slug == "youtube-to-mp3":
            return (
                ("How does the YouTube to MP3 converter work?", "Paste one public YouTube video or Short URL. After analysis, choose an MP3 option returned for that link. The server extracts available audio and converts it with ffmpeg before offering a temporary file."),
                ("Can I choose 320 kbps?", "Only choose from the options shown after analysis. A higher MP3 setting cannot add detail that is missing from the source audio, and no fixed 320 kbps result is promised."),
                ("Why is no MP3 option available?", "The video may be private, deleted, live, region restricted, age restricted, or blocked from anonymous extraction. A video without accessible audio also cannot be converted."),
                ("Does it work on a phone?", "The URL form works in a modern mobile browser. When processing finishes, save the temporary MP3 through your browser; the exact destination depends on your device."),
            )
        return (
            (f"Which links work with {self.name}?", self.url_hint),
            ("Which formats and qualities can I choose?", self.format_note + " Only formats returned by the source are displayed."),
            ("Why might a link fail?", self.problem + " Private, deleted, restricted, and live media cannot be processed."),
        )

    @property
    def seo_sections(self):
        return TOOL_SECTIONS.get(self.slug, ())

    @property
    def seo_links(self):
        return TOOL_SEO_LINKS.get(self.slug, ())


TOOL_SECTIONS = {
    "youtube-downloader": (
        ("One link can offer video and audio", (
            "Paste a public YouTube watch-page or Shorts URL to inspect that single upload. This general tool can show finished video choices alongside original audio and an MP3 conversion when the source provides a usable sound stream. The dedicated pages narrow the list when you already know the format you need.",
        )),
        ("Why options vary between uploads", (
            "YouTube can expose different containers, heights and audio tracks for different videos. SaveFromNet checks the actual source streams and the 512 MB processing limit before displaying choices. Playlists, rentals, private videos and live streams are outside this single-item public workflow.",
        )),
    ),
    "youtube-video-downloader": (
        ("Choose a complete video file", (
            "Paste a link to one public watch-page video. The analyzer checks its actual video streams and looks for compatible audio before showing a finished download. Some higher resolutions require the server to merge separate picture and sound streams.",
            "Compare the returned container, height and estimated size for this upload. A missing 1080p or 4K option means it was not available as a file this service can prepare within its 512 MB limit; the player label alone is not a download promise.",
        )),
        ("Use the right YouTube link", (
            "A youtube.com/watch?v= link or youtu.be short link identifies one video. Use the Shorts tool for a /shorts/ link and the audio tool when you only need sound. Playlists, purchases, private uploads and live streams are not available here.",
        )),
    ),
    "youtube-shorts-downloader": (
        ("Save one public Short", (
            "Copy the individual youtube.com/shorts/ URL, not a channel's Shorts tab. The analyzer validates the Short and returns the video or audio choices actually exposed for it. Choose from that result rather than assuming every vertical clip has the same resolution.",
        )),
        ("If a Short has no usable file", (
            "A removed, private, age-gated or live Short may be unavailable to an anonymous server. A video-only stream without accessible audio is not offered as a normal finished video. For a standard watch-page link, use the YouTube Video Downloader instead.",
        )),
    ),
    "youtube-to-mp3": (
        ("Convert a public YouTube video to MP3", (
            "Open a public video or Short that you own or may download, copy its complete URL, and paste it into the converter above. Analysis checks whether the source exposes an audio stream and returns only the choices available for that upload.",
            "Select an MP3 option to start the background job. The server extracts audio, converts it with ffmpeg, then provides a temporary download link. Keep this page open while processing; longer videos can take more time.",
        )),
        ("Understand the audio quality shown", (
            "A source audio stream may use M4A or WebM. MP3 is a conversion of that stream, not an original YouTube file. The result card shows the actual option and any size estimate the extractor can support; missing or unreliable sizes are left unknown.",
            "Changing the output bitrate cannot restore detail lost in the source. Compare the returned choices for the particular link instead of assuming every upload provides the same quality.",
        )),
        ("Fix common conversion problems", (
            "If the URL is rejected, use a complete youtube.com/watch, youtube.com/shorts or youtu.be link to one item. Playlists and arbitrary sites are not accepted on this page.",
            "If analysis fails, the post may have been removed, made private, restricted to a region or age group, or blocked for server access. If processing starts but times out, try a shorter public upload or another available audio option. The service does not bypass sign-in or access controls.",
        )),
        ("Use the converter on your device", (
            "The same form works in current phone, tablet and desktop browsers. The temporary file is saved by your browser, so its destination depends on your device settings. Completed files normally expire after about an hour and may disappear sooner if the processing container restarts.",
        )),
    ),
    "youtube-to-mp4": (
        ("What an MP4 result means", (
            "This page keeps the result focused on MP4 video choices returned for one public YouTube video or Short. Some MP4 picture streams arrive without sound; the server offers them as finished files only when it can obtain and merge compatible audio.",
            "The listed height and estimated size belong to the selected source streams. If YouTube supplies only WebM for a particular height, this tool does not relabel that file as MP4 or invent a conversion button.",
        )),
        ("Pick a resolution that is really available", (
            "Analyze the complete watch, Shorts or youtu.be link first. Compare the MP4 rows in the result card; long or high-bitrate uploads may exceed the 512 MB processing ceiling. The general YouTube downloader can show other available containers when MP4 is absent.",
        )),
    ),
    "instagram-downloader": (
        ("Choose a post or Reel, not a feed", (
            "The general Instagram tool accepts one public /p/ post or /reel/ URL. A post can contain an image, video or several carousel items; the result lists only accessible source items, up to 12. Stories and profiles have separate tools because they use different link shapes and access rules.",
        )),
        ("Anonymous access is the deciding factor", (
            "A post that opens inside your signed-in Instagram app may still be hidden from a server without an account. If the direct link asks a signed-out visitor to log in, SaveFromNet cannot retrieve it. No login details or private-account access are used.",
        )),
    ),
    "instagram-reels-downloader": (
        ("Use a direct Reel link", (
            "Paste one public instagram.com/reel/ link. A profile, feed or /p/ carousel URL describes different content and belongs in the general Instagram tool. The Reel page lists a video option only when the public extractor can reach its file.",
        )),
        ("Why a visible Reel may fail", (
            "Instagram can show a clip to a signed-in browser while withholding it from an anonymous server. Try opening the same link while signed out. SaveFromNet does not accept account cookies or bypass private profiles, deleted Reels or login gates.",
        )),
    ),
    "instagram-carousel-downloader": (
        ("A carousel contains separate items", (
            "Paste the individual public instagram.com/p/ post URL. The analyzer can list up to 12 accessible images or videos from that post, each as its own file choice. It does not label the whole carousel as one MP4 or create a ZIP that the source never supplied.",
        )),
        ("Check what was actually returned", (
            "A mixed carousel can have both images and videos; a single-image post may show only one item. Instagram sometimes exposes fewer items to anonymous access than the app displays to a signed-in account. If the post is private or login-gated, no result is promised.",
        )),
    ),
    "tiktok-downloader": (
        ("Video and photo posts need different results", (
            "Paste one public TikTok /@user/video/ or /photo/ post URL, or a supported short link. A video can expose a finished video file and accessible sound; a photo post can expose image items instead. The result card reflects that post's actual media, not a generic quality menu.",
        )),
        ("When TikTok blocks extraction", (
            "TikTok sometimes restricts requests from data-center networks even when a post plays on your phone. Removed, private or region-restricted posts can also fail. Use the individual public post link and try later if the source is temporarily unavailable; this service does not sign in or bypass restrictions.",
        )),
    ),
    "tiktok-to-mp3": (
        ("MP3 comes from the clip's sound", (
            "Use a public TikTok /@user/video/ link to one clip. If extraction returns an accessible audio stream, the server can convert it to MP3 and provide a temporary file. A photo post or silent video does not become a song just because its page has an MP3 tool.",
        )),
        ("Quality depends on the source", (
            "The result does not promise 320 kbps or a fixed file size. Re-encoding cannot restore sound detail that is absent from the original clip. If TikTok blocks the server, removes the post or requires sign-in, the tool explains the failure instead of displaying a fake download.",
        )),
    ),
    "facebook-video-downloader": (
        ("Copy the video post itself", (
            "A public facebook.com/watch?v= link, /videos/ post, /reel/ post or fb.watch short link can identify one video. A group feed or profile homepage is not a specific video. The analyzer presents only the file formats it can obtain from the linked post.",
        )),
        ("Public to you may still require login", (
            "A friends-only or group-only video can play in your account but cannot be reached by this anonymous service. Open the link while signed out to check access. SaveFromNet does not ask for Facebook credentials or work around publisher privacy settings.",
        )),
    ),
    "pinterest-video-downloader": (
        ("A Pin can be an image, GIF or video", (
            "Paste one pinterest.com/pin/ URL or pin.it short link. The result reflects the media Pinterest actually exposes for that Pin. An animated preview is not proof that an original GIF is available, and a still-image Pin will not produce a video row.",
        )),
        ("External links are a separate source", (
            "Some Pins primarily link to another website. This tool does not crawl that destination or claim its files as Pinterest downloads. Use a direct public Pin rather than a board or search-results page, then inspect the returned extension before starting a job.",
        )),
    ),
    "reddit-video-downloader": (
        ("Reddit may separate picture and sound", (
            "Paste a public post permalink under /r/.../comments/... or a redd.it short link. When Reddit exposes video and a compatible audio stream separately, the server can merge them into a finished file. The options shown depend on that post's streams, not a preset resolution list.",
        )),
        ("Check the post's access and host", (
            "Deleted, quarantined or adult-gated posts may not be available to anonymous extraction. A Reddit post can also point to an external video host rather than contain Reddit-hosted media. Copy the direct media post and choose another supported platform tool if the video lives elsewhere.",
        )),
    ),
    "threads-video-downloader": (
        ("One public source video", (
            "Use an individual threads.com/@username/post/ URL. This tool checks the public post metadata for a video hosted on Meta's expected media domains. When present, it offers that source MP4; the page may not expose a duration, file size or resolution ladder.",
        )),
        ("Why the result can be empty", (
            "A clip visible after signing in may not appear in the public metadata. Private posts and feed or profile URLs cannot be processed here. The tool does not manufacture 720p and 1080p choices when Threads exposes only one file.",
        )),
    ),
    "dailymotion-video-downloader": (
        ("Read the actual quality list", (
            "Paste a dailymotion.com/video/ or dai.ly link to one public upload. Analysis returns the available MP4 or WebM heights for that source. A quality label in the streaming player is not a guarantee that an anonymous downloader receives the same file.",
        )),
        ("Avoid collection and restricted links", (
            "Channel and playlist pages do not identify a single video for this tool. Private, deleted and region-blocked uploads also cannot be processed. If the link is valid but no format is returned, try the video's direct public URL rather than a collection page.",
        )),
    ),
    "universal-video-downloader": (
        ("One form for eight supported platforms", (
            "Paste one public video, photo, Reel, Short, Story, profile or Pin link from a supported platform. The URL detector checks its host and path, then sends that exact item to the appropriate extractor. A profile, board or feed is accepted only where a dedicated extractor explicitly supports it.",
        )),
        ("Understand the result before processing", (
            "The source decides whether the result contains video, audio or image choices. Missing resolutions, unknown file sizes and unavailable sound are not filled in with placeholders. Choose an actual returned option and save the temporary file when its background job finishes.",
        )),
    ),
}


TOOL_SEO_LINKS = {
    "youtube-downloader": (("/youtube-video-downloader", "Video-only choices"), ("/youtube-to-mp3", "Convert accessible audio")),
    "youtube-video-downloader": (("/guides/youtube-video-formats", "Understand YouTube formats"), ("/guides/video-file-size-estimates", "How file sizes are estimated"), ("/youtube-to-mp4", "MP4-only choices")),
    "youtube-shorts-downloader": (("/youtube-video-downloader", "Standard YouTube videos"), ("/youtube-to-mp3", "Shorts audio to MP3")),
    "youtube-to-mp3": (("/youtube-audio-downloader", "YouTube audio formats"), ("/guides/mp3-vs-m4a", "MP3 versus M4A")),
    "youtube-to-mp4": (("/youtube-video-downloader", "All YouTube video formats"), ("/guides/video-with-no-sound", "When a video has no sound")),
    "instagram-downloader": (("/instagram-reels-downloader", "Reels video"), ("/instagram-carousel-downloader", "Carousel items")),
    "instagram-reels-downloader": (("/instagram-video-downloader", "Other Instagram videos"), ("/guides/instagram-public-media", "Instagram link guide")),
    "instagram-carousel-downloader": (("/instagram-photo-downloader", "Single photo posts"), ("/guides/instagram-public-media", "Carousel and Story guide")),
    "tiktok-downloader": (("/guides/tiktok-photo-posts", "TikTok photo posts"), ("/tiktok-to-mp3", "Video audio to MP3"), ("/guides/tiktok-video-and-audio", "TikTok link guide")),
    "tiktok-to-mp3": (("/tiktok-downloader", "TikTok video and photos"), ("/guides/tiktok-video-and-audio", "TikTok audio guide")),
    "facebook-video-downloader": (("/guides/facebook-reels", "Public Facebook Reels"), ("/guides/facebook-public-videos", "Facebook link guide")),
    "pinterest-video-downloader": (("/guides/pinterest-images", "Save an image from a Pin"), ("/guides/pinterest-pin-media", "Images, GIFs and video")),
    "reddit-video-downloader": (("/guides/reddit-video-with-audio", "Reddit audio guide"), ("/universal-video-downloader", "Other supported platforms")),
    "threads-video-downloader": (("/guides/threads-video-availability", "Threads availability guide"), ("/universal-video-downloader", "Other supported platforms")),
    "dailymotion-video-downloader": (("/guides/dailymotion-video-quality", "Dailymotion quality guide"), ("/universal-video-downloader", "Other supported platforms")),
    "universal-video-downloader": (("/guides/temporary-download-links", "Temporary download links"), ("/guides/video-with-no-sound", "Why a file has no sound")),
}


TOOLS = [
    Tool("youtube-downloader", "youtube", "YouTube Downloader", "Analyze a public YouTube video or Short and save an available video or audio format.", ("video", "short"), "Video choices may include MP4 or WebM and extracted audio when the source provides it.", "Paste a youtube.com/watch, youtube.com/shorts, or youtu.be link to one item.", "YouTube may ask this server to sign in or block an unavailable video."),
    Tool("youtube-video-downloader", "youtube", "YouTube Video Downloader", "Choose a real video resolution from a public YouTube watch page.", ("video",), "The result lists only video heights and containers found for this upload.", "Use a youtube.com/watch?v= video link or youtu.be short link.", "A requested resolution may not exist for every upload."),
    Tool("youtube-shorts-downloader", "youtube", "YouTube Shorts Downloader", "Save a public vertical Short in a format the source actually offers.", ("short",), "Shorts formats vary; available video and audio options appear after analysis.", "Use a youtube.com/shorts/ link.", "A Short can be removed, made private, or blocked by the source."),
    Tool("youtube-to-mp3", "youtube", "YouTube to MP3", "Convert the audio of a public YouTube video into an MP3 file.", ("video", "short"), "MP3 is created from a source audio stream with ffmpeg; no fixed bitrate is promised.", "Use a public YouTube video or Short URL.", "A source without accessible audio cannot be converted."),
    Tool("youtube-audio-downloader", "youtube", "YouTube Audio Downloader", "Find source audio tracks and an MP3 conversion for a public YouTube upload.", ("video", "short"), "Original audio may be M4A or WebM; MP3 conversion appears when audio is present.", "Use a youtube.com/watch, music.youtube.com/watch, or youtu.be URL.", "Some music uploads are region or account restricted."),
    Tool("youtube-song-downloader", "youtube", "YouTube Song Downloader", "Save audio from a public song upload that you own or may download.", ("video", "short"), "Audio formats reflect the accessible upload, with MP3 conversion when possible.", "Paste the URL of one public YouTube song video.", "Official music content may have access, region, or rights restrictions."),
    Tool("youtube-to-mp4", "youtube", "YouTube to MP4", "Find available MP4 resolutions for a public YouTube video.", ("video", "short"), "Only MP4 streams found in the source results are offered; some need server-side audio merging.", "Paste a public YouTube video or Short link.", "Some uploads provide WebM only or lack a particular MP4 height."),
    Tool("youtube-music-downloader", "youtube", "YouTube Music Downloader", "Analyze a public YouTube Music track page for accessible audio.", ("video", "short"), "Original audio and MP3 conversion are shown only when an audio stream is returned.", "Use a public music.youtube.com/watch?v= link.", "Subscription-only or region-restricted tracks are unavailable without access."),
    Tool("youtube-movies-downloader", "youtube", "YouTube Movies Downloader", "Save a public YouTube movie upload only when you have permission.", ("video",), "The upload's real video and audio formats determine the choices; file size is limited to 512 MB.", "Use a public youtube.com/watch?v= link to one movie upload.", "Rentals, purchases, DRM, and age-gated titles are not supported."),
    Tool("instagram-downloader", "instagram", "Instagram Downloader", "Analyze a public Instagram post or Reel for video and image items.", ("post", "reel"), "Posts may expose original photos, carousel items, or videos depending on the source.", "Use a public instagram.com/p/ or instagram.com/reel/ URL.", "Instagram may require login even for some public posts."),
    Tool("instagram-video-downloader", "instagram", "Instagram Video Downloader", "Save a video item from a public Instagram post.", ("post", "reel"), "Video options appear only when the analyzed post contains accessible video.", "Use an Instagram post or Reel URL containing video.", "Photo-only posts have no video file to offer."),
    Tool("instagram-reels-downloader", "instagram", "Instagram Reels Downloader", "Analyze a public Instagram Reel and choose its accessible video format.", ("reel",), "The source extractor determines whether an MP4 video is available.", "Use an instagram.com/reel/ URL.", "Private, removed, or login-gated Reels cannot be retrieved."),
    Tool("instagram-photo-downloader", "instagram", "Instagram Photo Downloader", "Find original image items in a public Instagram post.", ("post",), "Image files may be JPEG, PNG, or WebP as exposed by the source.", "Use a public instagram.com/p/ photo post URL.", "A video-only post will not offer a photo download."),
    Tool("instagram-story-downloader", "instagram", "Instagram Story Downloader", "Check whether a public Instagram Story can be accessed without signing in.", ("story",), "An image or video option is shown only if the public Story extractor returns one.", "Use an instagram.com/stories/username/story-id/ URL.", "Most Stories require an account or expire quickly; this service does not sign in or bypass access controls."),
    Tool("instagram-carousel-downloader", "instagram", "Instagram Carousel Downloader", "Browse the available images and videos in one public Instagram carousel post.", ("post",), "Each accessible carousel item appears as its own original file choice, up to 12 items.", "Use an instagram.com/p/ link to a carousel post.", "A post may expose fewer items to anonymous visitors than it shows in the app."),
    Tool("instagram-profile-downloader", "instagram", "Instagram Profile Downloader", "Inspect up to 12 publicly accessible media items from an Instagram profile.", ("profile",), "Each accessible profile item is an individual image or video download.", "Use a public instagram.com/username/ profile link.", "Profile feeds often require login; private profiles are unavailable."),
    Tool("tiktok-downloader", "tiktok", "TikTok Downloader", "Save an accessible public TikTok video or photo post.", ("video", "photo"), "Video streams and converted audio appear only when returned by TikTok.", "Use a tiktok.com/@user/video/id, /photo/id, or vm.tiktok.com link.", "TikTok sometimes blocks data-center requests or removes posts."),
    Tool("tiktok-to-mp3", "tiktok", "TikTok to MP3", "Convert audio from a public TikTok video into MP3 when audio is available.", ("video",), "MP3 is generated from the returned audio stream; no invented bitrate is shown.", "Use a public TikTok video URL.", "Silent clips and unavailable posts cannot produce an MP3."),
    Tool("tiktok-story-downloader", "tiktok", "TikTok Story Downloader", "Inspect publicly accessible TikTok Stories for downloadable media.", ("story",), "The gallery extractor lists only Story items it can access anonymously.", "Use a tiktok.com/@username/stories URL.", "Stories expire and may require sign-in; inaccessible Stories cannot be downloaded."),
    Tool("facebook-video-downloader", "facebook", "Facebook Video Downloader", "Find video formats from a public Facebook video or Reel.", ("video",), "The result shows only source formats returned for that specific public post.", "Use facebook.com/watch?v=, a public /videos/ or /reel/ URL, or fb.watch.", "Friends-only videos, login walls, and removed posts are unavailable."),
    Tool("pinterest-video-downloader", "pinterest", "Pinterest and GIF Downloader", "Inspect one public Pin for its original image, GIF, or video.", ("pin",), "Pins may contain an image, GIF, or video; only the extracted source item is offered.", "Use a pinterest.com/pin/id/ or pin.it short link.", "Some Pins link away to external sites rather than hosting downloadable media."),
    Tool("reddit-video-downloader", "reddit", "Reddit Video Downloader", "Save a video attached to a public Reddit post.", ("post",), "Reddit may provide video and audio as separate streams, which are merged when needed.", "Use a reddit.com/r/community/comments/id/ or redd.it/id link.", "Deleted, quarantined, or adult-gated posts can be inaccessible."),
    Tool("threads-video-downloader", "threads", "Threads Video Downloader", "Check a public Threads post for a video exposed in its page metadata.", ("post",), "A source MP4 option appears only when Threads publishes a public video URL.", "Use a threads.com/@username/post/id URL.", "Threads often omits video metadata or requires login; those posts have no available format here."),
    Tool("dailymotion-video-downloader", "dailymotion", "Dailymotion Video Downloader", "Choose a format returned for one public Dailymotion video.", ("video",), "Available MP4 or WebM heights come from that video's extractor result.", "Use dailymotion.com/video/id or dai.ly/id.", "Private, geo-blocked, and removed videos cannot be processed."),
    Tool("universal-video-downloader", "universal", "Universal Video Downloader", "Paste a public link from a supported platform and automatically route it to its extractor.", ("video", "short", "post", "pin", "reel", "photo", "story", "profile"), "The analyzed source decides which real video, audio, or image formats appear.", "Use one public URL from YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads, or Dailymotion.", "The source may block, remove, or restrict individual posts."),
]

BY_SLUG = {tool.slug: tool for tool in TOOLS}
PLATFORMS = ("youtube", "instagram", "tiktok", "facebook", "pinterest", "reddit", "threads", "dailymotion")


def related_tools(tool):
    same = [other for other in TOOLS if other.platform == tool.platform and other.slug != tool.slug]
    return (same[:5] + [BY_SLUG["universal-video-downloader"]])[:6] if tool.platform != "universal" else TOOLS[:8]
