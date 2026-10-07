"""Original, data-driven public directory and trust pages.

These pages explain the service without inventing product capabilities. The
downloader experiences and guides remain in tools.py and guides.py.
"""

from dataclasses import dataclass


CONTACT_EMAIL = "umarisaloneenough@gmail.com"


@dataclass(frozen=True)
class Section:
    heading: str
    paragraphs: tuple[str, ...]
    links: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Page:
    slug: str
    title: str
    description: str
    heading: str
    intro: str
    sections: tuple[Section, ...] = ()
    schema_type: str = "WebPage"

    @property
    def path(self):
        return "/" + self.slug


PAGES = (
    Page(
        "tools", "Media Download Tools | SaveFromNet",
        "Browse SaveFromNet's working video, audio, photo and converter tools by platform. Every format choice comes from analysis of your public link.",
        "Media download tools",
        "Choose a tool for your source and format. Each page uses the same real downloader and shows only formats returned for the link you enter.",
        schema_type="CollectionPage",
    ),
    Page(
        "about", "About SaveFromNet | Public Media Downloader",
        "How SaveFromNet analyzes public media links, prepares temporary downloads, and handles unsupported or restricted content.",
        "About SaveFromNet",
        "SaveFromNet helps you inspect and save media from supported public links when you own it or have permission to download it.",
        (
            Section("What the service does", (
                "Paste one supported public URL. The server checks its platform, asks the source for accessible media information, and lists the formats it actually finds. You choose an option and a temporary job prepares the file.",
                "YouTube, Instagram, TikTok, Facebook, Pinterest, Reddit, Threads and Dailymotion have dedicated tools. Availability varies by post and by the source's access rules.",
            ), (("/tools", "Browse all tools"),)),
            Section("What it cannot access", (
                "The service does not sign into your accounts, unlock private posts, remove DRM, bypass paywalls, or guarantee a particular resolution. A public page can still be unavailable to an anonymous server.",
                "Source websites can change their formats or restrict requests without notice. An error is shown when a link cannot be analyzed or processed.",
            ), (("/guides", "Read practical guides"),)),
            Section("Temporary processing", (
                "Completed files are held temporarily and normally removed after about an hour. The processing container can restart sooner. Signed links expire after 15 minutes; your browser's recent history can issue a fresh link while the file still exists.",
            ), (("/privacy-policy", "How data is handled"), ("/contact", "Contact us"))),
        ),
        "AboutPage",
    ),
    Page(
        "contact", "Contact SaveFromNet | Support and Reports",
        "Contact SaveFromNet about a broken tool, accessibility issue, privacy request, or copyright concern.",
        "Contact SaveFromNet",
        "Tell us which page or public link caused a problem and what happened. Please do not send passwords, account cookies, or private media.",
        (
            Section("Support and feedback", (
                f"Email {CONTACT_EMAIL} with the affected SaveFromNet page, the platform, and the error message. If a link contains private information, describe the problem without sending the link.",
                "Source services sometimes block server requests even when a post opens in your browser. Include the time of the attempt so we can investigate, but do not send login details.",
            ), ((f"mailto:{CONTACT_EMAIL}?subject=SaveFromNet%20support", "Email support"), ("/guides", "Check the guides"))),
            Section("Copyright and privacy", (
                "For a copyright concern, identify the SaveFromNet page or temporary file involved and the work you own. For a privacy request, tell us what browser history or information you want reviewed.",
            ), (("/dmca", "Copyright removal requests"), ("/privacy-policy", "Privacy policy"))),
        ),
        "ContactPage",
    ),
    Page(
        "privacy-policy", "Privacy Policy | SaveFromNet",
        "Learn what SaveFromNet processes when you analyze a public URL, download a file, or use the site.",
        "Privacy policy",
        "This policy describes the current public downloader. Last updated October 7, 2026.",
        (
            Section("Information used for a download", (
                "When you submit a URL, the server processes that URL, the selected tool and format, and job status to complete your request. A browser identifier cookie associates an analysis and temporary download with the browser that requested it. The cookie lasts up to 30 days unless you clear it.",
                "The processing container keeps job metadata, including the submitted URL and file details, in temporary local storage. Finished files are normally removed after about an hour and may disappear sooner if the container restarts. You can delete an entry and its file from the recent downloads section.",
            )),
            Section("Limits and aggregate measurement", (
                "Cloudflare uses the requesting IP address to apply rate limits. SaveFromNet records aggregate events such as platform, tool, format and success or failure. The analytics event payload does not include the submitted URL or a browser identifier.",
                "The site also uses Google Analytics. Its tag measures page visits and browser or device information and may set a first-party _ga cookie to distinguish visits. Google's handling of that measurement data is described in its own privacy information.",
                "Cloudflare and the source website necessarily process network requests needed to deliver pages or inspect a public link. Their handling of network data is governed by their own policies.",
            ), (("https://support.google.com/analytics/answer/11593727", "Google Analytics data collection"),)),
            Section("Advertising and external links", (
                "The site loads a third-party advertising script. That provider may collect device or usage information or use its own identifiers under its policy. Links to source platforms and other websites take you to services outside SaveFromNet.",
                "Do not submit private, sensitive, or account-only URLs. The downloader only accepts supported public media links.",
            )),
            Section("Your choices and contact", (
                "You can clear your browser cookie, delete available recent-download entries, or stop using the service. Clearing the cookie prevents the old browser identifier from retrieving its history or files.",
                f"For a privacy question or request, email {CONTACT_EMAIL}. Include enough detail to locate the issue without sending a password or private media.",
            ), (("/contact", "Contact us"),)),
        ),
    ),
    Page(
        "terms", "Terms of Use | SaveFromNet",
        "Rules for using SaveFromNet's public media downloader and temporary file processing service.",
        "Terms of use",
        "These terms describe the public SaveFromNet service. Last updated October 7, 2026.",
        (
            Section("Use only authorized content", (
                "Use the service only for media you own or have permission to download. You are responsible for following applicable copyright law and the source platform's terms. Do not submit private content, account-only links, or material protected by DRM or a paywall.",
                "Do not use the service to probe internal networks, overwhelm the API, evade rate limits, or interfere with other users. We may limit or refuse abusive requests.",
            )),
            Section("How the service works", (
                "Available formats and quality depend on what the source exposes for a particular public link. A listed option is not a promise that the source will continue to provide it. Processing may fail because a source changes, blocks requests, or removes the media.",
                "Prepared files and access links are temporary. Save important authorized files on your own device while they are available.",
            )),
            Section("Reports and updates", (
                "Tell us if a tool fails or if you believe content or a page on this site infringes your rights. We may update these terms as the service changes; the date above identifies this version.",
            ), (("/contact", "Contact us"), ("/dmca", "Copyright removal requests"))),
        ),
    ),
    Page(
        "dmca", "Copyright Removal Requests | SaveFromNet",
        "How rights holders can report a SaveFromNet page or temporary file that they believe infringes copyright.",
        "Copyright removal requests",
        "If you believe a SaveFromNet page or file infringes your rights, send a specific report so we can review it.",
        (
            Section("What to send", (
                f"Email {CONTACT_EMAIL} with your name and contact information, the work you own, the exact SaveFromNet URL or temporary file reference, and enough information to locate the material. Explain the rights concern and include a statement that the information is accurate and that you are authorized to act for the rights holder.",
                "We review reports and can remove site content or disable access to a temporary file when appropriate. Media requested from a source is processed on demand and is not kept as a permanent public library.",
            ), ((f"mailto:{CONTACT_EMAIL}?subject=SaveFromNet%20copyright%20report", "Email a copyright report"),)),
            Section("Important distinction", (
                "A source website controls the original post. To remove that post from the internet, contact the source platform as well. A report to SaveFromNet addresses this service's pages or temporary files.",
                "This contact page does not state that SaveFromNet has registered a designated agent with the U.S. Copyright Office. See the Copyright Office for formal notice requirements and its designated-agent directory.",
            ), (("https://copyright.gov/512/", "U.S. Copyright Office Section 512 resources"), ("/copyright", "Copyright and permitted use"))),
        ),
    ),
    Page(
        "copyright", "Copyright and Permitted Use | SaveFromNet",
        "Understand your responsibility when downloading public media and how to report a rights concern to SaveFromNet.",
        "Copyright and permitted use",
        "A public URL is not permission to copy or redistribute its media. Download only what you own or are allowed to use.",
        (
            Section("Check your rights first", (
                "Permission can come from owning the work, a license, or the creator's authorization. A video being publicly viewable does not by itself mean it is free to download, reupload, or use commercially.",
                "SaveFromNet does not remove copyright notices, unlock private posts, bypass DRM, or grant rights to source media. The source platform and creator remain responsible for their own content and terms.",
            )),
            Section("Report a concern", (
                "If a SaveFromNet page or temporary file creates a copyright concern, send a precise report so we can review it. If the original post is hosted elsewhere, also use that platform's reporting process.",
            ), (("/dmca", "How to report a copyright concern"), ("/contact", "Contact SaveFromNet"))),
        ),
    ),
)

BY_SLUG = {page.slug: page for page in PAGES}


# A tool may appear in two useful browse categories, but every card points to
# one canonical working tool route. Empty categories are deliberately omitted.
TOOL_GROUPS = (
    ("Video downloaders", ("universal-video-downloader", "youtube-video-downloader", "youtube-shorts-downloader", "youtube-movies-downloader", "facebook-video-downloader", "reddit-video-downloader", "threads-video-downloader", "dailymotion-video-downloader")),
    ("Audio downloaders", ("youtube-to-mp3", "youtube-audio-downloader", "youtube-song-downloader", "youtube-music-downloader", "tiktok-to-mp3")),
    ("Social media downloaders", ("instagram-downloader", "instagram-video-downloader", "instagram-reels-downloader", "instagram-photo-downloader", "instagram-story-downloader", "instagram-carousel-downloader", "instagram-profile-downloader", "tiktok-downloader", "tiktok-story-downloader", "pinterest-video-downloader")),
    ("Converters", ("youtube-to-mp3", "youtube-to-mp4", "tiktok-to-mp3")),
    ("Platform tools", ("youtube-downloader", "instagram-downloader", "tiktok-downloader", "facebook-video-downloader", "pinterest-video-downloader", "reddit-video-downloader", "threads-video-downloader", "dailymotion-video-downloader")),
)
