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
    related: tuple[str, ...] = ()

    @property
    def path(self):
        return f"/guides/{self.slug}"


GUIDES = (
    Guide(
        "how-to-copy-a-youtube-link", "How to copy a YouTube video or Shorts link",
        "Find the direct URL for one public YouTube video or Short, including phone share links, and avoid playlist or channel links.",
        "A downloader needs a link to one video, not a search result, channel, or feed. The steps below help you copy the right link for a public upload you own or have permission to save, then choose the matching SaveFromNet tool.",
        "youtube-downloader",
        (
            ("Copy a watch-page link on desktop", "Open the individual video and copy its address from the browser. A standard link contains youtube.com/watch?v= followed by the video's ID. You can also use the video's Share control to copy a youtu.be short link. Both forms point to one upload; a bare channel or search URL does not."),
            ("Use Share on iPhone or Android", "Open the individual video in YouTube or your phone browser, tap Share, then Copy link. Paste it into the downloader form. The copied address may contain extra share or timestamp parameters; SaveFromNet reads the video ID and removes those extras during URL normalization. You do not need to edit the link by hand."),
            ("Identify a Shorts link", "Open the specific Short and copy its Share link. A direct youtube.com/shorts/ URL includes the Short's ID. Use the YouTube Shorts Downloader for a video file, or the YouTube to MP3 Converter when accessible audio is what you need. A Shorts tab or feed is not an individual clip."),
            ("Avoid playlist and access problems", "A watch URL can include a playlist parameter, but SaveFromNet processes only the one video identified by its video ID. A playlist page, channel homepage, private upload, age-restricted video, rental, or live stream is not a supported finished file. If a direct link fails, check whether it opens publicly without signing in and whether the video is still available."),
        ),
        (("Does a youtu.be link work?", "Yes. A youtu.be link to one public video works when that video is accessible for anonymous analysis."),
         ("Should I remove the timestamp or share parameters?", "No. The URL detector normalizes supported video links and discards unrelated parameters before analysis."),
         ("Can I download a whole playlist from one link?", "No. The downloader prepares one eligible video at a time; it does not fetch an entire playlist.")),
        ("youtube-video-on-mobile", "youtube-shorts-on-phone", "youtube-mp3-on-phone"),
    ),
    Guide(
        "youtube-shorts-on-phone", "How to download YouTube Shorts on iPhone or Android",
        "Use a direct public Shorts link on your phone, choose a real video format, and find the file your browser saved.",
        "A YouTube Short is one video, not the whole Shorts feed. If you own the clip or have permission to save it, paste its direct link into the downloader below. The formats depend on that individual Short, and your phone browser handles the final save.",
        "youtube-shorts-downloader",
        (
            ("Copy the individual Short's link", "Open the Short, use its Share control to copy a link containing youtube.com/shorts/ and the video ID, then paste it into the form above. A creator's Shorts tab, playlist or search page does not identify one file. The downloader accepts the public Short only when it can be analyzed without signing in."),
            ("Choose a video that actually appears", "After analysis, compare the returned video rows. MP4 or WebM and the listed resolution depend on the source; a vertical preview does not guarantee a particular height. Tap Download for an available choice and keep the browser tab open while the temporary file is prepared. A long or high-bitrate result may hit the 512 MB processing limit."),
            ("Find the saved file on your phone", "Use the finished download link in the same browser. On iPhone or iPad, check that browser's downloads list and its configured Files app location. On Android, check the browser's downloads list or your device's Downloads location. Saving a file through a browser does not necessarily add it to Photos or the gallery; use your device's share or import action if you need it there."),
            ("When a Short has no download option", "Confirm the link points to the individual Short and opens publicly without signing in. A private, removed, age- or region-restricted Short may be unavailable. If you only need audio, the YouTube to MP3 converter can show an MP3 choice when that Short has accessible sound; it cannot create audio from a silent clip."),
        ),
        (("Can I download Shorts without an app?", "Yes. This page works in a current phone browser; no SaveFromNet app is required."),
         ("Why is the Short not in my photo gallery?", "The browser may save it to its downloads location. Locate the file there, then import or share it into your gallery app if you want."),
         ("Will every Short have an MP4 download?", "No. The result displays only file formats the source exposes and the service can prepare for that specific Short.")),
        ("youtube-video-on-mobile", "youtube-video-formats", "temporary-download-links"),
    ),
    Guide(
        "youtube-mp3-on-phone", "How to convert a YouTube video to MP3 on a phone",
        "Convert accessible audio from one public YouTube video or Short and save the finished MP3 in your phone browser.",
        "You can use the YouTube to MP3 converter in a phone browser for a video or Short you own or may download. The converter checks the actual audio track first. The MP3 is a new file made from that source audio, not an original audio format promised for every upload.",
        "youtube-to-mp3",
        (
            ("Paste a direct video or Shorts link", "Copy one public youtube.com/watch?v=, youtu.be, or youtube.com/shorts/ URL and paste it above. A playlist, creator channel, or YouTube Music album is not one eligible video. Select Download to analyze the link; the result shows an MP3 only if the source provides usable audio."),
            ("Understand the MP3 option", "Choose an MP3 row actually returned for the video. The server converts an accessible source track with ffmpeg and then gives your browser a temporary file link. A larger output bitrate cannot restore detail missing from the original stream. If you prefer a source M4A or WebM audio track when available, use the YouTube Audio Downloader instead."),
            ("Save the file and locate it", "Keep the tab open while the job prepares the MP3, then use its download link in the same browser. On iPhone or iPad, check the browser's downloads list and its chosen Files app location. On Android, check the browser's downloads list or Downloads location. An MP3 saved as a file does not automatically appear in every music library app."),
            ("Fix a missing or expired result", "If there is no MP3 choice, the video may be silent, private, removed, live, restricted or blocked from anonymous access. If a finished link expires, return to Recent downloads in the original browser while the temporary file still exists. These links are short lived; save the authorized file to your phone when it is ready."),
        ),
        (("Do I need to install a YouTube MP3 app?", "No. The converter runs through the browser and the browser saves the completed file."),
         ("Can I convert a YouTube Short to MP3?", "Yes, when the direct public Short exposes accessible sound. A silent Short has no audio to convert."),
         ("Why can I not find the MP3 in my music app?", "A browser download is a file first. Find it in the browser's downloads list or device file manager, then import it into a music app if that app supports imports.")),
        ("mp3-vs-m4a", "youtube-video-on-mobile", "temporary-download-links"),
    ),
    Guide(
        "youtube-video-on-mac", "How to download a YouTube video on Mac",
        "Use the browser-based YouTube video downloader on a Mac, compare available files, and find your completed download.",
        "If you need to download a public YouTube video you own or have permission to save, you can use SaveFromNet in a Mac browser. There is no separate Mac downloader app to install. The source determines which files appear, and your browser chooses where the finished file goes.",
        "youtube-video-downloader",
        (
            ("Copy a direct link to one video", "Open the specific public video and copy its youtube.com/watch?v= or youtu.be link. Paste that link into the downloader form above and select Analyze link. A channel, playlist, live stream, rental or private upload is not an eligible finished video. For a vertical /shorts/ link, use the dedicated YouTube Shorts downloader."),
            ("Choose a file your Mac can use", "Compare the video options returned for that link. MP4 is a practical first choice when available; WebM is another source format and may need a compatible player or editor. Resolution, audio availability and estimated size vary by upload. SaveFromNet does not create a missing 1080p or 4K option, and its processing limit is 512 MB per file."),
            ("Save and locate the finished video", "Choose a returned format and keep the page open while the temporary download is prepared. When it is ready, use the download link. Check your browser's downloads list or its configured download location if you cannot find the file; the browser may ask you where to save it. A completed file is stored on your Mac after the browser finishes saving it, while the server's temporary copy expires."),
            ("If the download does not start", "First confirm that the same video opens without signing in. If analysis reports a restriction, SaveFromNet cannot use your account to bypass it. If a large format is absent or processing reaches the file limit, choose a smaller option actually listed. If a temporary link has expired, return to the original browser session and use a fresh link when the file still exists."),
        ),
        (("Do I need a YouTube downloader app for Mac?", "No. This workflow runs in your Mac browser and saves the finished file through that browser."),
         ("Where did the video go on my Mac?", "Check the downloads list in the browser you used and its configured download destination. Your browser settings control the local folder."),
         ("Can I download a YouTube Short on Mac?", "Yes, use the YouTube Shorts downloader with a direct public /shorts/ link and choose a format returned for that Short."),
         ("Can I download a private or purchased video?", "No. The public downloader does not bypass sign-in, purchases, DRM, or other access restrictions.")),
        ("youtube-video-on-mobile", "youtube-video-formats", "youtube-hd-4k-downloads"),
    ),
    Guide(
        "youtube-video-on-mobile", "Download a YouTube video on iPhone or Android",
        "Use the YouTube video downloader in a phone browser, find the saved file, and troubleshoot mobile download limits.",
        "You can analyze a public YouTube watch-page video from a phone without installing a SaveFromNet app. The browser handles the final file save, so finding the download is a device step separate from preparing the video.",
        "youtube-video-downloader",
        (
            ("Copy the link to one video", "Open the individual YouTube video that you own or have permission to download and use its Share control to copy the link. A youtube.com/watch?v= address or a youtu.be short link identifies one standard video. A channel, playlist or live page does not identify a supported finished file. Paste the copied URL into the downloader form above and select Analyze link."),
            ("Choose a format your phone can use", "Wait for the actual video choices before tapping Download. MP4 is usually the simpler choice for broad phone compatibility when it appears; WebM playback depends on the device and app you use. The listed resolution and size come from the analyzed upload, so do not assume every phone or video will have the same 1080p or 4K option. Large files may exceed this service's 512 MB processing limit."),
            ("Save and find the completed file", "Keep the browser tab open while the file is prepared, then use its temporary download link. On iPhone or iPad, check the browser's downloads list and the Files app location configured for downloads. On Android, check the browser's download list or your device's Downloads location. Browser settings can change those destinations; saving the file does not automatically place it in the Photos gallery."),
        ),
        (("Do I need an app?", "No. Use the downloader in a current mobile browser; the browser handles the saved file."),
         ("Why is the file missing from Photos?", "A browser download is normally saved to its configured files location. Find it in browser downloads or your device's file manager, then import it into another app if needed."),
         ("Can I download a private video on my phone?", "No. The public extractor cannot use your YouTube sign-in or bypass private, age, region or purchase restrictions.")),
        ("youtube-hd-4k-downloads", "youtube-video-formats", "temporary-download-links"),
    ),
    Guide(
        "youtube-hd-4k-downloads", "Why a YouTube video may not have a 1080p or 4K download",
        "Check real HD and 4K video choices, separate audio streams, file size estimates, and the 512 MB processing limit.",
        "A 1080p or 4K label in YouTube's player is a playback choice, not a guarantee that a public downloader can prepare the same finished file. SaveFromNet inspects each permitted URL and only lists combinations that its processing service can handle.",
        "youtube-video-downloader",
        (
            ("Read the analyzed video rows, not a fixed quality chart", "Paste a direct public watch-page or youtu.be link to one upload you may save. After analysis, compare each returned row's container, height and size information. A row absent from the result cannot be selected. MP4 and WebM are different containers; a source may expose one but not the other at a particular resolution. Use the MP4-only tool only when that container is required."),
            ("High resolution video can need a separate audio track", "YouTube often serves higher resolution picture and audio as separate streams. SaveFromNet can offer a finished file when a compatible sound stream is accessible and the streams can be merged. It does not list a picture-only stream as a normal video download with sound. If the source has no usable audio partner, the desired HD row may be missing even when the picture appears in the player."),
            ("Length, bitrate and the 512 MB ceiling matter", "Resolution alone does not determine file size: duration, codec, video bitrate and audio bitrate all affect the finished file. SaveFromNet rejects known or strongly estimated results over 512 MB; a job with unknown size can still stop if it reaches that limit. For example, 25 minutes at a combined 19,000 kbps is roughly 3.6 GB before overhead, so a tiny 4K size estimate would be misleading. Try an available lower resolution for a long upload."),
        ),
        (("Can I force 4K if it is missing?", "No. Only an accessible and processable source combination can appear in the result. Changing the label would not create the file."),
         ("Does 1080p always have sound?", "Not as one source stream. The service needs compatible audio to prepare a finished video with sound."),
         ("Why does estimated size say unknown?", "The source may not report enough reliable bytes or bitrate data for the complete video and audio combination. Unknown is more accurate than an audio-only or invented total.")),
        ("youtube-video-formats", "video-file-size-estimates", "youtube-video-on-mobile"),
    ),
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
    Guide(
        "tiktok-photo-posts", "How to download public TikTok photo posts",
        "Use a direct TikTok photo-post link, understand individual image results, and troubleshoot posts that cannot be read anonymously.",
        "A TikTok photo post is not a video with a different label. Its direct /photo/ link can expose separate images, while a /video/ link is processed as a video. This guide explains what the working TikTok tool can actually save.",
        "tiktok-downloader",
        (
            ("Copy the individual photo-post link", "Open a public TikTok post and copy its tiktok.com/@creator/photo/numeric-id URL. A profile, hashtag feed or Story does not identify the same item. The URL detector sends a supported photo link to the image extractor rather than pretending it is a video stream."),
            ("Choose from the returned image items", "An accessible photo post can return multiple image files, shown separately in the result. SaveFromNet inspects up to 12 items and displays their source extensions when known; it does not fabricate an MP4 or offer a ZIP archive. Save only the items you own or may use."),
            ("Why a slideshow may not load", "A public-looking post may be removed, restricted by region or account, or blocked from data-center requests. Try the direct photo URL while signed out. The downloader does not use your TikTok credentials or bypass private access, and an unavailable source cannot produce image files."),
        ),
        (("Can I paste a video URL instead?", "Yes, the general TikTok tool also accepts public /video/ links, but it will show video formats rather than photo items."),
         ("Will a photo post provide MP3?", "Not through this photo workflow. The TikTok to MP3 tool accepts a video with accessible audio.")),
        ("tiktok-video-and-audio", "why-media-links-fail"),
    ),
    Guide(
        "facebook-reels", "How to download a public Facebook Reel",
        "Find a direct public Facebook Reel link, check anonymous access, and choose only video formats actually returned for it.",
        "Facebook Reels use the same real video-processing backend as other public Facebook videos. The important difference is the link: copy the individual Reel, then check which formats that post exposes without an account.",
        "facebook-video-downloader",
        (
            ("Use the Reel permalink", "Copy the public facebook.com/reel/ link from the individual Reel. A watch or fb.watch link to the same public video may also work, while a profile or group feed does not identify one downloadable item. Paste the direct link into the Facebook Video Downloader above."),
            ("Check access outside your account", "A Reel can play for you because you are signed in or belong to a group. Open its link in a signed-out window: if Facebook requires login, says it is unavailable, or limits it to friends, the anonymous server cannot retrieve it. SaveFromNet does not accept cookies or change sharing settings."),
            ("Read the actual result before saving", "A successful analysis reports the video's accessible container and resolution when the source provides them. HD is not guaranteed for every Reel. Choose one returned option, let the background job prepare it, and save the temporary file before it expires."),
        ),
        (("Is there a separate Reel extractor?", "The Facebook Video Downloader handles supported public /reel/ links through its existing Facebook extractor."),
         ("Can it save a friends-only Reel?", "No. Content that needs your Facebook session is unavailable to this public downloader.")),
        ("facebook-public-videos", "why-media-links-fail"),
    ),
    Guide(
        "pinterest-images", "How to save an image from a public Pinterest Pin",
        "Identify an individual Pin, distinguish a hosted image from a linked website, and inspect the image format returned by Pinterest.",
        "A Pinterest Pin can contain an image, GIF, or video, and some Pins mainly link to another website. SaveFromNet lists a file only when the public Pin itself exposes supported media.",
        "pinterest-video-downloader",
        (
            ("Copy one Pin, not a board", "Open the specific public Pin and copy its pinterest.com/pin/numeric-id/ URL or pin.it short link. A board or search page holds many Pins, so it is not an individual media URL. The downloader validates the Pin before contacting the source extractor."),
            ("Check the returned image type", "A still Pin may expose JPEG, PNG, or WebP; an animated Pin may expose a GIF or a video instead. The result reflects the source item and may not know its dimensions or size in advance. Choose the returned file rather than assuming every preview has an original GIF."),
            ("When the Pin only links elsewhere", "Some Pins use an image as a preview for an article or video on another website. This tool does not crawl the destination or claim to download its media. If Pinterest provides no accessible source file, there is no file to offer here."),
        ),
        (("Can I download every image on a board?", "No. Paste an individual public Pin link for each item you have permission to save."),
         ("Why did I get WebP instead of JPEG?", "The extension comes from the media returned for that Pin; the service does not rename another format as JPEG.")),
        ("pinterest-pin-media", "why-media-links-fail"),
    ),
    Guide(
        "video-file-size-estimates", "Video file size calculator and download estimates",
        "Estimate video file size from runtime and bitrate, then understand source-reported sizes, separate audio streams, and SaveFromNet's 512 MB limit.",
        "Resolution alone does not determine file size. Use the calculator below when you know the runtime and stream bitrates; the answer is an estimate, not a measured download. You can share a link that preserves your calculator inputs. SaveFromNet leaves size unknown when the source does not provide enough information for a defensible total.",
        "youtube-video-downloader",
        (
            ("A reported size is different from an estimate", "Some source formats include an explicit byte count; others offer only an approximate size or bitrate. An estimate based on bitrate also needs a valid duration. The calculator multiplies seconds by the combined video and audio bitrates, then divides by eight to convert bits to bytes. Variable bitrate, container overhead and processing can change the finished size. Unknown is more honest than a misleading tiny 4K file."),
            ("Video and audio may arrive separately", "A high-resolution video stream may contain picture only. When a compatible audio stream is available, the server combines them for the finished file. The displayed total must account for both streams; an audio-only size cannot stand in for the whole video. Actual output can still differ from an estimate."),
            ("The processing ceiling changes the choices", "SaveFromNet limits a prepared job to 512 MB. An option known or strongly estimated to exceed that ceiling is omitted. If a size is unknown, a job can still stop when the real file reaches the limit. Select a lower available resolution for a long upload."),
        ),
        (("Can a 25-minute 4K video really be tiny?", "A very small number beside a long 4K video is suspect unless the source reports that complete file size. At a combined 19,000 kbps, 25 minutes is about 3,563 MB before container overhead, not 23 MB. SaveFromNet leaves the total unknown when it cannot account for video and audio."),
         ("Does 1080p always use less space than 4K?", "Usually for the same encoding, but codec, bitrate, content, and audio can change the comparison. Check the options returned for your actual upload.")),
        ("youtube-video-formats", "reddit-video-with-audio"),
    ),
    Guide(
        "temporary-download-links", "How SaveFromNet temporary download links work",
        "Learn why signed file links expire, when recent history can refresh a link, and how temporary processing protects storage.",
        "A completed download is a temporary file, not a permanent hosted copy. Its link is signed for one browser and a short period, while the file itself normally disappears after about an hour or earlier if the processing container restarts.",
        "universal-video-downloader",
        (
            ("A link belongs to the browser that started the job", "After analysis and processing, SaveFromNet issues a signed URL bound to the anonymous browser cookie used for that job. The URL expires after 15 minutes. Sharing it with another browser or device will not give that browser access to your temporary file."),
            ("Refresh a link while the file still exists", "The Recent downloads section can request a fresh signed link for a completed job if its file remains in the active container. A link may expire even though the file is temporarily present. If the container restarted or cleanup removed the file, analyze and prepare the public source again."),
            ("Save the file before cleanup", "Completed files are normally removed after about an hour, but an idle container can stop sooner. Download the prepared file to your device when it is ready; do not use the temporary link as a permanent bookmark or storage service. You can also remove your own recent job entry."),
        ),
        (("Why does my link say expired?", "The 15-minute signature elapsed, the browser cookie changed, or the temporary file was cleared. Check Recent downloads in the original browser for a fresh link if available."),
         ("Can someone else open my link?", "The signed URL is bound to the browser cookie that started the job, so a different browser cannot use it.")),
        ("why-media-links-fail", "video-file-size-estimates"),
    ),
    Guide(
        "video-with-no-sound", "Why a downloaded video may have no sound",
        "Troubleshoot silent source clips, separate audio streams, and unavailable sound before choosing a video or MP3 result.",
        "A video page can show moving pictures without offering a usable audio track. Some platforms deliver picture and sound separately; others publish a genuinely silent clip. Inspect the returned choices before preparing a file.",
        "universal-video-downloader",
        (
            ("Check whether the original post has audio", "Play the public post while signed out and confirm that it really contains sound. A muted recording or silent animation cannot be made audible by conversion. If the media belongs to another supported platform, use its direct post URL so the correct extractor handles it."),
            ("Separate streams need a compatible partner", "YouTube and Reddit can supply video and audio as different streams. SaveFromNet combines compatible streams when both are accessible and does not offer a video-only source as a normal finished video with sound. Some source pages still expose only silent or incomplete media to anonymous visitors."),
            ("MP3 is not a repair for missing audio", "An MP3 option appears only when the extractor finds usable sound. If the result has no audio choice, check whether the post is restricted, removed, still live, or simply silent. Higher output bitrate cannot restore a track that does not exist."),
        ),
        (("Will changing from MP4 to WebM add sound?", "No. A container name does not create an audio track; the source must expose audio that can be combined or extracted."),
         ("Why does a Reddit video need merging?", "Reddit may publish picture and sound separately. The Reddit guide explains that source behavior in more detail.")),
        ("reddit-video-with-audio", "youtube-video-formats"),
    ),
)

BY_SLUG = {guide.slug: guide for guide in GUIDES}
