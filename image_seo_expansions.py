"""Editorially reviewed conversion tasks backed by the shared image processor.

Each entry has a distinct input/output or same-format compression task. These
are not keyword aliases: the server validates the input and encodes the stated
output format before returning a real file.
"""

IMAGE_EXPANSIONS = (
    dict(
        slug="png-to-jpg", name="PNG to JPG Converter",
        description="Convert a still PNG into a JPG photo file with adjustable quality, flattening transparent pixels onto white.",
        input_formats=("PNG",), output_format="JPEG",
        explanation="This tool decodes one PNG image and encodes a new JPEG file. JPEG does not support transparent pixels, so transparent or partly transparent parts are placed against a white background before encoding. The result is a real .jpg file, not a renamed PNG.",
        tip="Use this for a photograph that must be accepted by a JPG-only website. Keep PNG for logos, screenshots or artwork that needs transparency or crisp edges.",
        faq=(("Will a transparent PNG stay transparent?", "No. JPG has no alpha channel. Transparent pixels become white in the converted file."),
             ("Is the JPG always smaller?", "No. Output size depends on the image and quality setting. The result shows the actual byte count before you save it."),
             ("Can I convert an animated PNG?", "This workflow accepts one still image. Multi-frame images are rejected instead of silently discarding frames.")),
        seo_sections=(("When PNG to JPG is useful", (
            "A camera image, product photo or document scan saved as PNG can be much larger than a JPG at a suitable quality level. Convert a copy when the recipient requires JPEG or when you need a photo-oriented format for broad compatibility. The quality slider changes the encoder setting; compare the actual result before deleting your original.",
            "A logo, diagram or screenshot may be better left as PNG. JPEG compression can introduce visible edges around text and line art, and it cannot keep a transparent background. This converter is for one still image at a time, up to the site's upload and pixel limits.",
        )), ("What the converter changes", (
            "SaveFromNet reads the PNG pixels, applies any orientation information, removes source metadata, places transparent pixels on white and writes a JPEG. It does not create extra detail or make a blurry source sharper. The output is returned directly to your browser and is not added to media download history.",
        ))),
    ),
    dict(
        slug="webp-to-jpg", name="WebP to JPG Converter",
        description="Turn a still WebP image into an actual JPG file for apps that do not accept WebP.",
        input_formats=("WEBP",), output_format="JPEG",
        explanation="A WebP image is decoded and written as JPEG at the quality you choose. JPEG cannot retain transparency, so any transparent areas are flattened onto white. Animated WebP files are rejected rather than converted to a single frame without warning.",
        tip="Choose JPG when a form or older editor rejects WebP. For a transparent graphic, use WebP to PNG instead.",
        faq=(("Why did the background turn white?", "JPG has no transparent pixels. This converter places WebP transparency on white before saving."),
             ("Can it convert animated WebP?", "No. Animated or multi-frame files are rejected so the motion is not silently lost."),
             ("Does conversion restore quality?", "No. Re-encoding cannot recover detail removed by the original WebP compression.")),
        seo_sections=(("Choose JPG for compatibility", (
            "Some upload forms and image editors accept JPG but not WebP. If you have a still WebP photo, this page produces a genuine JPEG that those destinations can read. The quality control lets you balance appearance and file size, and the result reports its measured size instead of promising a reduction.",
            "Before converting a WebP logo or product cutout, check whether it has transparency. The white background in the JPG is deliberate because JPEG has no alpha channel. If your destination needs a clear background, convert to PNG with the related WebP to PNG tool.",
        )), ("Still images and source limitations", (
            "SaveFromNet processes one still image in memory and strips source metadata. It cannot preserve WebP animation inside JPG, and it will reject a multi-frame upload. A low-resolution or heavily compressed source remains limited by its original pixels after conversion.",
        ))),
    ),
    dict(
        slug="jpg-to-webp", name="JPG to WebP Converter",
        description="Convert a JPG photo to WebP with a selectable output quality and real size comparison.",
        input_formats=("JPEG",), output_format="WEBP",
        explanation="The JPG is decoded and encoded again as a WebP still image. WebP may use fewer bytes at an acceptable visual quality, but a small or already optimized JPG can produce a larger result. The site shows both actual sizes.",
        tip="Start around quality 80 for a photo, then check fine texture and edges before replacing the original JPG.",
        faq=(("Will WebP always be smaller than JPG?", "No. It depends on the image and chosen quality; compare the displayed original and output byte sizes."),
             ("Can WebP fix JPG artifacts?", "No. The original JPG's lost detail and artifacts remain in the decoded pixels."),
             ("Does this preserve camera metadata?", "No. The image is rebuilt from pixels so source EXIF details, including location metadata, are not copied.")),
        seo_sections=(("Make a WebP copy of a photo", (
            "WebP is useful when a website or app accepts it and you want to compare a different photo encoder against your JPG. Upload one still JPG, choose a quality setting and save the WebP only if its visual result and measured byte size suit your destination. The converter never claims a fixed percentage saving.",
            "Converting does not add transparency to a JPG or recreate information its earlier compression removed. Retain your JPG if a recipient asks specifically for JPEG, or if you need the original for future editing.",
        )), ("Quality and delivery details", (
            "The service decodes the source, applies orientation, drops original metadata and writes a new WebP file in memory. Lower quality can reduce size but may soften texture or text. The returned file is downloaded from the response; it is not stored as a media job or published as a URL.",
        ))),
    ),
    dict(
        slug="heic-to-webp", name="HEIC to WebP Converter",
        description="Convert a still HEIC photo into a WebP image for a WebP-compatible website or editor.",
        input_formats=("HEIC",), output_format="WEBP",
        explanation="The server decodes a single HEIC image and re-encodes its pixels as WebP. The quality slider controls the WebP output; converting does not restore information already lost in the HEIC original.",
        tip="Use this when a destination accepts WebP but not HEIC. For the broadest photo compatibility, choose HEIC to JPG instead.",
        faq=(("Will this work with an iPhone Live Photo?", "Only the still HEIC image is supported. A video component or multi-frame file is not converted."),
             ("Is the output still HEIC?", "No. The server returns a real .webp file with WebP encoding."),
             ("Will it preserve transparency?", "WebP supports alpha, and the encoder keeps it when the decoded HEIC supplies an alpha channel. Check the result in your destination app.")),
        seo_sections=(("Move a HEIC still image into a WebP workflow", (
            "A photo captured as HEIC can be inconvenient when a content system accepts WebP but rejects HEIC. This converter produces a still WebP copy at a chosen quality. It is useful for a website image workflow where WebP is supported; it is not a way to preserve the motion of a Live Photo.",
            "If you are emailing a photo to someone whose app may not open WebP, JPG is often the safer destination. The related HEIC to JPG tool exists for that compatibility case. Keep the original HEIC until you have checked the WebP's appearance and size.",
        )), ("What happens during conversion", (
            "The image is decoded, corrected for orientation, rebuilt without source EXIF metadata and encoded as WebP. Animated or multi-frame input is rejected, and files over the stated upload or pixel limits cannot be processed. The finished copy is sent to your browser without permanent image storage.",
        ))),
    ),
    dict(
        slug="webp-to-heic", name="WebP to HEIC Converter",
        description="Convert a still WebP image into a real HEIC file with adjustable output quality.",
        input_formats=("WEBP",), output_format="HEIC",
        explanation="This tool decodes one WebP image and writes a new HEIC still image. HEIC compatibility varies by operating system and app, so choose it only when the destination explicitly supports HEIC.",
        tip="Keep the WebP original until you confirm the recipient can open the HEIC output; changing the extension alone would not convert it.",
        faq=(("Is the result a real HEIC file?", "Yes. The server uses an HEIC encoder and returns a .heic file, not a renamed WebP."),
             ("Can it convert an animated WebP?", "No. Animated or multi-frame uploads are rejected rather than losing motion silently."),
             ("Will transparency survive?", "The encoder can keep an alpha channel, but HEIC transparency support varies by app. Inspect the downloaded result.")),
        seo_sections=(("Use HEIC only where it is accepted", (
            "HEIC can be useful in a photo library or workflow that explicitly accepts it. For sharing on the open web, WebP or JPG may be easier for the recipient to use. Converting a WebP to HEIC cannot make the source sharper, and it may change fine detail because the image is encoded again.",
            "Upload one still WebP image, adjust quality and compare the actual output size with the original. A smaller file is possible but not guaranteed. If your next destination needs a broadly supported file, consider the related WebP to JPG or WebP to PNG tool instead.",
        )), ("A still-image conversion, not animation export", (
            "The image processor rejects animated WebP before conversion. It decodes and rebuilds the still pixels, removes original metadata and returns an HEIC file directly to your browser. There is no video or animation track in the result.",
        ))),
    ),
    dict(
        slug="jpg-compressor", name="JPG Compressor",
        description="Recompress a JPG photo as JPG, adjust quality and compare the real before-and-after size.",
        input_formats=("JPEG",), output_format="JPEG",
        explanation="Unlike the general image compressor that outputs WebP, this tool keeps JPEG as the output format. It decodes the source and writes a new JPG at your chosen quality while dropping original metadata.",
        tip="Try a moderate quality setting, inspect small text and textures, and keep the result only when the size and appearance meet your needs.",
        faq=(("Will the file stay JPG?", "Yes. The output is encoded as JPEG and downloaded with a .jpg extension."),
             ("Is a smaller file guaranteed?", "No. Already optimized images can become larger. The page reports actual input and output sizes."),
             ("Can repeated compression harm quality?", "Yes. Re-encoding a lossy JPG can add artifacts, especially at low quality settings. Keep the original for future edits.")),
        seo_sections=(("Reduce a JPG without changing its type", (
            "Some forms require JPEG and will not accept WebP. This compressor retains the JPG format while letting you choose an output quality. A lower setting can shrink a photo, but it also removes visual detail; inspect faces, text and high-contrast edges before saving the copy.",
            "A source photo that was already aggressively compressed may not shrink further. The result shows measured byte counts, so you can decide whether the conversion helped. This page does not report an invented percentage reduction or claim that a quality setting restores detail.",
        )), ("How the file is handled", (
            "SaveFromNet reads one still JPG of up to 8 MB and 20 megapixels, applies orientation, rebuilds pixels without source EXIF metadata and writes the new file in memory. The output is returned to your browser and is not added to the video downloader's temporary history.",
        ))),
    ),
    dict(
        slug="webp-compressor", name="WebP Compressor",
        description="Recompress a still WebP image as WebP with adjustable quality and measured output size.",
        input_formats=("WEBP",), output_format="WEBP",
        explanation="This tool decodes one still WebP and re-encodes it as WebP at the selected quality. It can preserve transparency when present; animated WebP is rejected. An already efficient original may not get smaller.",
        tip="Use a lower quality only after checking graphics, fine texture and transparent edges in the finished file.",
        faq=(("Does the output remain WebP?", "Yes. The returned file is encoded as WebP and uses a .webp extension."),
             ("Is animation preserved?", "No. Animated or multi-frame WebP is rejected, rather than silently taking only one frame."),
             ("Can the result be larger?", "Yes. Re-encoding is not guaranteed to reduce bytes; compare the actual before and after sizes shown on the page.")),
        seo_sections=(("Change WebP quality without switching formats", (
            "If a publishing system requires WebP, this page gives an existing WebP a dedicated same-format workflow. It accepts a still WebP and returns another WebP at your chosen quality. The general image compressor also accepts JPG, PNG and WebP, and both tools report real byte counts so you can judge the trade-off.",
            "WebP supports transparency, and the converted still image keeps an alpha channel when the source has one. Lower quality may affect the edges of graphics and small text. Animation is not supported; a multi-frame file produces an error instead of a misleading still download.",
        )), ("Check the result before replacing the source", (
            "An optimized WebP can become larger after re-encoding, even at a lower quality setting. The server rebuilds the pixels without copying source metadata and returns the new file directly to the browser. Keep your original until the new size and appearance are acceptable.",
        ))),
    ),
)
