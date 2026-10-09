"""Working media utilities with distinct tasks and one shared form."""

from dataclasses import dataclass

from site_pages import Page, Section


@dataclass(frozen=True)
class UtilityTool:
    slug: str
    name: str
    mode: str
    accept: str
    action: str
    hint: str


UTILITY_TOOLS = (
    UtilityTool("youtube-thumbnail-downloader", "YouTube Thumbnail Downloader", "thumbnail", "", "Get thumbnail", "Paste one public YouTube video or Shorts link."),
    UtilityTool("video-to-gif", "Video to GIF Converter", "upload", "video/mp4,video/webm,video/quicktime", "Create GIF", "Choose an MP4, WebM or MOV up to 3 minutes and 1080p. GIF output is limited to 10 seconds."),
    UtilityTool("mp4-to-mp3", "MP4 to MP3 Converter", "upload", "video/mp4", "Extract MP3", "Choose an MP4 with audio, up to 10 minutes long. This tool reads your uploaded file, not a video URL."),
    UtilityTool("video-trimmer", "Video Trimmer", "upload", "video/mp4,video/webm,video/quicktime", "Trim video", "Choose an MP4, WebM or MOV up to 3 minutes and 1080p; select a segment up to 60 seconds."),
    UtilityTool("audio-cutter", "Audio Cutter", "upload", "audio/mpeg,audio/mp4,audio/x-m4a,audio/wav,audio/wave", "Cut audio", "Choose an MP3, M4A or WAV up to 10 minutes long and select a segment up to 120 seconds."),
)
BY_SLUG = {tool.slug: tool for tool in UTILITY_TOOLS}


UTILITY_PAGES = (
    Page("youtube-thumbnail-downloader", "YouTube Thumbnail Downloader | SaveFromNet",
         "Get an actual image thumbnail for one public YouTube video or Short, without installing an app.",
         "YouTube Thumbnail Downloader",
         "Paste a direct YouTube video or Shorts link to save the image YouTube exposes for that video. Save only artwork you own or have permission to use.",
         (Section("Download the image for one video", (
             "The tool validates a YouTube watch, Shorts or youtu.be link, extracts its video ID, and requests an image from YouTube's thumbnail host. It tries the larger thumbnail first and uses the standard thumbnail when that version is unavailable.",
             "The returned JPG is the actual image served for the video. Image size and availability depend on YouTube; this tool does not create new frames or remove a watermark.")),
          Section("Where a thumbnail is useful", (
             "Creators may reuse their own thumbnail for a website, archive or video planning document. If a video is removed or YouTube does not serve its image, this tool returns an error instead of a made-up picture.",
             "A channel page or playlist is not one video. Paste the link to the individual upload and check the rights to the artwork before republishing it."), (("/youtube-video-downloader", "Open YouTube Video Downloader"),))),
         schema_type="WebApplication"),
    Page("video-to-gif", "Video to GIF Converter | SaveFromNet",
         "Turn a short section of your own MP4, WebM or MOV into a real animated GIF.",
         "Video to GIF Converter",
         "Upload a video clip, choose where the GIF starts, and save up to ten seconds as an animated image. This tool processes an uploaded file, not a social media URL.",
         (Section("Choose a short moment", (
             "Upload an MP4, WebM or MOV at most 16 MB, three minutes long, and 1080p. Enter a start time and a clip length of up to ten seconds. The server checks the real media streams before running ffmpeg, then returns the actual GIF bytes.",
             "GIF is limited to 480 pixels wide and 10 frames per second to keep the file practical. GIF does not carry sound; use Video Trimmer when you need to retain the clip's audio."), (("/video-trimmer", "Trim a video with audio"),)),
          Section("Understand the result", (
             "Animated GIFs may be larger than the original compressed video and have a limited color palette. The result gives the true output size. Uploaded media and temporary files are removed after processing.",
             "For a video from another platform, download it only if you have permission, then upload the file you are allowed to edit."),)),
         schema_type="WebApplication"),
    Page("mp4-to-mp3", "MP4 to MP3 Converter | SaveFromNet",
         "Extract the available audio from an MP4 file you own and save it as MP3.",
         "MP4 to MP3 Converter",
         "Choose a local MP4 video that contains an audio track. The tool extracts and encodes that audio as an MP3 file without promising a quality higher than the source.",
         (Section("Convert an uploaded MP4", (
             "Select an MP4 file no larger than 16 MB or longer than ten minutes. The processor checks that it is a genuine MP4 with audio, then uses ffmpeg to produce MP3. A silent video has nothing to extract and is rejected clearly.",
             "This tool handles files already on your device. To analyze a public YouTube URL you may download, use the YouTube to MP3 tool instead."), (("/youtube-to-mp3", "YouTube to MP3 Converter"),)),
          Section("Sound quality and privacy", (
             "MP3 is a new lossy encoding of the source track. A higher bitrate cannot restore missing detail. Compare the output by listening before discarding the original video.",
             "The upload is held only while the conversion runs; no permanent media library is created."),)),
         schema_type="WebApplication"),
    Page("video-trimmer", "Video Trimmer Online | SaveFromNet",
         "Cut a section from an MP4, WebM or MOV upload and download an MP4 clip.",
         "Video Trimmer",
         "Upload your own video, enter the start and end times, and save the selected section as MP4. The clip can be up to 60 seconds long.",
         (Section("Select the exact section", (
             "Choose a video at most 16 MB, three minutes long, and 1080p. Start and end times are seconds from the beginning of the file. The end must be after the start and within the verified source duration.",
             "The selected section is encoded as an MP4 with H.264 video and AAC audio when the source has sound. Encoding supports accurate cuts between keyframes but may change the output size."), (("/video-to-gif", "Turn a short clip into GIF"),)),
          Section("Limits and source rights", (
             "A cut is limited to 60 seconds to keep public processing bounded. Files that are damaged, over the size limit, or have no video stream are rejected.",
             "Use clips you own or may edit. The temporary input and output files are deleted after the response is prepared."),)),
         schema_type="WebApplication"),
    Page("audio-cutter", "Audio Cutter Online | SaveFromNet",
         "Cut a segment from an MP3, M4A or WAV upload and save the result as MP3.",
         "Audio Cutter",
         "Choose an audio file you own, enter start and end times, and save only the segment you need. The maximum cut is 120 seconds.",
         (Section("Cut a local audio file", (
             "Upload an MP3, M4A or WAV up to 16 MB and ten minutes long. The server verifies a real audio stream and duration, then encodes the chosen portion to MP3. Times are measured in seconds; the end must come after the start.",
             "A WAV recording can produce a smaller MP3, but MP3 encoding is lossy. For archival audio, keep your original file."), (("/mp4-to-mp3", "Extract audio from MP4"),)),
          Section("Private, temporary processing", (
             "The file is processed in an isolated temporary directory and removed when the cut completes. We do not build a stored audio library from uploads.",
             "This tool edits a local audio file; it does not fetch private tracks or bypass a streaming service's access controls."),)),
         schema_type="WebApplication"),
)
