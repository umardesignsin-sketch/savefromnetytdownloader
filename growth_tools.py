"""Small, working utility pages with distinct search intent and honest limits."""

from dataclasses import dataclass

from site_pages import Page, Section


@dataclass(frozen=True)
class GrowthTool:
    slug: str
    kind: str
    name: str
    faq: tuple[tuple[str, str], ...]

    @property
    def path(self):
        return "/" + self.slug


GROWTH_TOOLS = (
    GrowthTool("calculator", "calculator", "Free Online Calculator", (
        ("What can this calculator solve?", "Enter decimal arithmetic with addition, subtraction, multiplication, division, parentheses and percent. It also has a square-root button."),
        ("Are my calculations uploaded?", "No. Calculations run in your browser and are not sent to SaveFromNet."),
        ("Why does an expression show an error?", "Check for unmatched parentheses, missing numbers or division by zero. The calculator does not evaluate code or variables."),
    )),
    GrowthTool("translator", "translator", "Free Text Translator", (
        ("Which languages can I translate?", "This short-text tool supports English, Spanish and French in either direction. Select both languages before translating."),
        ("Is my text private?", "Your text is sent to MyMemory to produce a translation. Do not enter confidential or sensitive information."),
        ("How much text can I enter?", "Up to 500 characters per request. The upstream free service can also impose its own limits or become unavailable."),
    )),
    GrowthTool("english-to-spanish-translator", "translator", "English to Spanish Translator", (
        ("Can I translate Spanish back to English?", "Yes. Use the Swap button to change the direction, or open the general translator for French."),
        ("Does it translate full documents?", "No. This page handles short text of up to 500 characters per request and does not accept document uploads."),
        ("Who processes the text?", "MyMemory processes the text to return a translation. Avoid private or sensitive text."),
    )),
    GrowthTool("us-weather-forecast", "weather", "US Weather Forecast", (
        ("Where does the forecast come from?", "Forecast periods come from the United States National Weather Service. The ZIP code location is resolved through Zippopotam.us."),
        ("Can I search outside the United States?", "No. This page currently accepts five-digit US ZIP codes only because its forecast source covers US locations."),
        ("Is this an emergency alert service?", "No. Forecast data can be delayed or unavailable. Follow the National Weather Service directly for current warnings."),
    )),
    GrowthTool("portrait-background-remover", "background", "Portrait Background Remover", (
        ("Which photos work best?", "Photos with a clear person in the foreground work best. The model is trained to separate people and may not isolate products, pets or complex objects."),
        ("Is my photo uploaded?", "No. The image is processed in your browser. The segmentation model and runtime download from Google's model host and jsDelivr on first use."),
        ("Which file can I save?", "The result is a transparent PNG. Check the preview because fine hair, glass and crowded scenes can produce imperfect edges."),
    )),
)

BY_SLUG = {tool.slug: tool for tool in GROWTH_TOOLS}


GROWTH_PAGES = (
    Page("calculator", "Free Online Calculator – Arithmetic & Percent | SaveFromNet",
         "Use a free calculator for arithmetic, percentages, parentheses and square roots. Results appear instantly in your browser.",
         "Free Online Calculator", "Solve everyday arithmetic with a clear, mobile-friendly calculator. Your expression stays on your device.",
         (Section("Calculate without sending your numbers away", (
             "Enter numbers with the keyboard or tap the keypad. The calculator supports +, −, ×, ÷, parentheses, decimals, percent and square root. Press equals or Enter to see the result. There is no account or API call for a calculation.",
             "Percent means divide by 100, so 25% is 0.25. To find 25 percent of 80, enter 80 × 25%. Use parentheses when several operations need a specific order.")),
          Section("Check the result before relying on it", (
             "This is a standard arithmetic calculator. It rejects incomplete expressions and division by zero instead of silently inventing a number. Long decimal results are rounded for display; it is not a scientific or financial precision instrument.",
             "For a file-size estimate based on bitrate and duration, use the separate video file size calculator."), (("/guides/video-file-size-estimates", "Video file size calculator"),))),
         schema_type="WebApplication"),
    Page("translator", "Free Text Translator – English, Spanish & French | SaveFromNet",
         "Translate short English, Spanish or French text in either direction. See a real translation returned by MyMemory.",
         "Free Text Translator", "Translate a short phrase between English, Spanish and French. Choose the source and target languages, then review the result.",
         (Section("Translate a phrase in three languages", (
             "Paste up to 500 characters, choose English, Spanish or French for each side, and press Translate. SaveFromNet passes the text to MyMemory's translation service and shows the actual response. The page does not generate a placeholder or claim to translate an entire document.",
             "Machine translation can miss context, names or idioms. Review the result before publishing or using it for important communication."), (("/english-to-spanish-translator", "English to Spanish translator"),)),
          Section("Privacy and availability", (
             "The submitted text leaves your browser and is processed by MyMemory. Do not enter private or sensitive material. Upstream rate limits and outages may temporarily stop translation; the tool will show an error when no translation is available.",
             "This translator is separate from the YouTube transcript tool, which reads existing captions and does not translate video audio."), (("/youtube-to-transcript", "YouTube transcript converter"),))),
         schema_type="WebApplication"),
    Page("english-to-spanish-translator", "English to Spanish Translator Online | SaveFromNet",
         "Translate short English text into Spanish and swap direction to translate Spanish into English.",
         "English to Spanish Translator", "Enter an English phrase and get a real Spanish translation. Swap languages when you need Spanish to English.",
         (Section("Translate English into Spanish", (
             "This page starts with English as the source and Spanish as the target. Paste up to 500 characters and select Translate. The result comes from MyMemory, so names, regional phrasing and ambiguous words still deserve a human review.",
             "Use Swap to reverse the direction. For French, open the general translator and select a different pair."), (("/translator", "Translate English, Spanish or French"),)),
          Section("Useful for short text", (
             "Try a message, sentence or short paragraph. This page does not translate files, web pages or private conversations automatically. Your text is sent to the translation provider when you press Translate, so avoid sensitive information.",
             "If the provider rejects a request or reaches a limit, we show an error instead of repeating your input as though it were a translation."),)),
         schema_type="WebApplication"),
    Page("us-weather-forecast", "US Weather Forecast by ZIP Code | SaveFromNet",
         "Check real National Weather Service forecast periods for a five-digit US ZIP code.",
         "US Weather Forecast", "Enter a US ZIP code to see the latest available National Weather Service forecast for that location.",
         (Section("Forecasts from a public weather source", (
             "Enter a five-digit US ZIP code. Zippopotam.us resolves the approximate location; the National Weather Service returns forecast periods for its coordinates. The result includes the location, forecast update time, temperatures, wind and the source's own description.",
             "A ZIP code covers an area, so the forecast point may not match your exact street. Open the source link for details and current watches or warnings."), (("https://www.weather.gov/", "National Weather Service"),)),
          Section("Coverage and safety limits", (
             "This tool covers US ZIP codes only. The underlying NWS API is public and can be temporarily unavailable. An unknown ZIP or location outside forecast coverage receives a clear error.",
             "Forecasts are informational, not an emergency alert system. For urgent weather decisions, follow official local guidance."),)),
         schema_type="WebApplication"),
    Page("portrait-background-remover", "Portrait Background Remover – Transparent PNG | SaveFromNet",
         "Remove the background from a photo of a person in your browser and download a transparent PNG.",
         "Portrait Background Remover", "Select a photo of a person, remove the surrounding background on your device, and save a transparent PNG.",
         (Section("Make a portrait cutout", (
             "Choose a JPG, PNG or WebP photo under 8 MB. The browser loads a portrait segmentation model, estimates which pixels belong to the person, and creates a transparent PNG you can preview before saving. The first run can take longer while the model downloads.",
             "The model is intended for people. It can miss fine hair, transparent accessories, objects held in front of the body or people in a crowded scene. It is not a general product-photo background remover."), (("/image-cropper", "Crop the result"),)),
          Section("Your photo stays in the browser", (
             "The photo is processed locally and is not uploaded to SaveFromNet. The browser downloads model files from Google and the MediaPipe runtime from jsDelivr. Close the page to discard the working image and preview.",
             "Save the resulting PNG if you need transparent edges. JPG cannot store transparency; use the PNG to JPG converter later only if you want a solid background."), (("/png-to-jpg", "PNG to JPG converter"),))),
         schema_type="WebApplication"),
)
