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


TOOL_SECTIONS = {
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
