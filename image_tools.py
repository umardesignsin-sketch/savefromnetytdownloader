"""Data for real image upload tools; all use one guarded processing endpoint."""

from dataclasses import dataclass

from image_seo_expansions import IMAGE_EXPANSIONS


@dataclass(frozen=True)
class ImageTool:
    slug: str
    name: str
    description: str
    input_formats: tuple[str, ...]
    output_format: str
    explanation: str
    tip: str
    faq: tuple[tuple[str, str], ...]
    seo_sections: tuple[tuple[str, tuple[str, ...]], ...] = ()

    @property
    def path(self):
        return "/" + self.slug

    @property
    def title(self):
        return f"{self.name} Online | SaveFromNet"


IMAGE_TOOLS = (
    ImageTool("image-compressor", "Image Compressor",
              "Compress a JPG, PNG or WebP image into a WebP file with adjustable quality.",
              ("JPEG", "PNG", "WEBP"), "WEBP",
              "WebP uses lossy compression. Lower quality usually makes a smaller file, but fine detail may soften. The result shows the actual byte sizes so you can compare before saving.",
              "Try quality 75–85 for photos. A tiny or already optimized image may not get smaller.",
              (("Will the image always be smaller?", "No. The final size depends on the source image and chosen quality. We show the actual before and after sizes."),
               ("Does compression change the file type?", "Yes. This tool produces WebP, which supports photos and transparency."))),
    ImageTool("png-to-heic", "PNG to HEIC Converter",
              "Convert a PNG upload to a real HEIC image with adjustable output quality.",
              ("PNG",), "HEIC",
              "HEIC can use less space than PNG for photographic content. Conversion is lossy, so sharp graphics and transparency may look different after encoding.",
              "HEIC support varies by device and app. Keep the original PNG if you need broad compatibility.",
              (("Is this a real HEIC file?", "Yes. The server encodes HEIC and returns a .heic file; changing the filename alone would not convert it."),
               ("Can HEIC preserve transparency?", "The encoder can retain an alpha channel, but app support varies. Check your result in the software where you plan to use it."))),
    ImageTool("jpg-to-heic", "JPG to HEIC Converter",
              "Convert a JPG photo to HEIC and choose the output quality.",
              ("JPEG",), "HEIC",
              "The JPG is decoded and encoded again as HEIC. Re-encoding cannot restore detail already lost in the original JPG, but it can produce a compact copy.",
              "Compare the returned size and appearance before deleting your original JPG.",
              (("Will HEIC look exactly like my JPG?", "Lossy conversion can change fine detail. Choose a higher quality setting when appearance matters more than size."),
               ("Will every app open HEIC?", "No. HEIC support varies. Use the HEIC to JPG tool when a destination needs a widely supported file."))),
    ImageTool("heic-to-jpg", "HEIC to JPG Converter",
              "Turn an HEIC photo into a widely supported JPG file.",
              ("HEIC",), "JPEG",
              "JPG is useful for websites and apps that cannot read HEIC. The conversion decodes the HEIC image and makes a new JPG; transparent areas become white.",
              "A JPG may be larger than the source HEIC. The result reports the actual size.",
              (("Does JPG keep HEIC transparency?", "No. JPG has no alpha channel, so transparent pixels are placed on white."),
               ("Can I convert a Live Photo?", "Only a still HEIC image is supported. Video or multi-frame content is rejected."))),
    ImageTool("heic-to-png", "HEIC to PNG Converter",
              "Convert an HEIC still image into a lossless PNG file.",
              ("HEIC",), "PNG",
              "PNG preserves the pixels decoded from HEIC without adding another lossy encoding step. It cannot recover detail that the HEIC source already lost.",
              "PNG files are often larger than HEIC photos, especially at high resolutions.",
              (("Will PNG improve image quality?", "No. It preserves the decoded pixels but cannot recreate missing detail."),
               ("Is transparency retained?", "Yes, when the HEIC decoder exposes an alpha channel."))),
    ImageTool("png-to-webp", "PNG to WebP Converter",
              "Convert a PNG image into WebP with an adjustable quality setting.",
              ("PNG",), "WEBP",
              "WebP can retain transparent backgrounds while using lossy compression for smaller files. For logos or pixel art, inspect the result for edge changes.",
              "Choose a higher quality for text or graphics with crisp lines.",
              (("Does WebP support transparency?", "Yes. This conversion preserves the image's alpha channel when present."),
               ("Is WebP always smaller?", "No. The result card shows the real output size so you can decide."))),
    ImageTool("jpg-to-png", "JPG to PNG Converter",
              "Convert a JPG image to PNG without another lossy encoding step.",
              ("JPEG",), "PNG",
              "PNG stores the decoded JPG pixels losslessly. It does not remove existing JPG artifacts or make a photo sharper, and the file is often larger.",
              "Use PNG when an editor or workflow specifically requires it.",
              (("Will converting to PNG improve my JPG?", "No. Existing JPG compression artifacts remain in the pixels."),
               ("Why did the file get bigger?", "PNG stores pixels losslessly, which is commonly less compact for photographs."))),
    ImageTool("webp-to-png", "WebP to PNG Converter",
              "Convert a WebP still image into PNG for apps that need PNG files.",
              ("WEBP",), "PNG",
              "The tool decodes the WebP and writes PNG, keeping transparency where the source has it. It supports still images rather than animated WebP files.",
              "PNG output may be bigger than the WebP source.",
              (("Will animated WebP become animated PNG?", "No. Animated files are rejected so frames are not silently discarded."),
               ("Is transparency preserved?", "Yes, when it is present in the source image."))),
    ImageTool("image-resizer", "Image Resizer",
              "Resize a JPG, PNG or WebP image to a chosen width while preserving its aspect ratio.",
              ("JPEG", "PNG", "WEBP"), "SAME",
              "Enter the desired pixel width. Height is calculated from the original aspect ratio and Lanczos resampling produces the new image. The original file format is retained.",
              "Enter a width smaller than the source to reduce dimensions; this tool does not enlarge images.",
              (("Will the picture be stretched?", "No. Height changes in proportion to width."),
               ("Can I make a tiny image sharp by enlarging it?", "No. This tool only resizes down because enlarging cannot invent detail."))),
) + tuple(ImageTool(**item) for item in IMAGE_EXPANSIONS)

BY_SLUG = {tool.slug: tool for tool in IMAGE_TOOLS}
