"""Small, working utility pages with distinct search intent and honest limits."""

from dataclasses import dataclass

from regional_data import EU_VAT_CHECKED, PASSPORT_SPECS, TAX_CALCULATORS, US_SALES_TAX_AS_OF
from site_pages import Page, Section


@dataclass(frozen=True)
class GrowthTool:
    slug: str
    kind: str
    name: str
    faq: tuple[tuple[str, str], ...]
    region: str = ""   # country tools: "US", "UK", "AU" or "EU"
    preset: str = ""   # key into PASSPORT_SPECS or TAX_CALCULATORS
    summary: str = ""  # one-line card description

    @property
    def path(self):
        return "/" + self.slug

    @property
    def passport_spec(self):
        return PASSPORT_SPECS.get(self.preset) if self.kind == "passport" else None

    @property
    def tax_config(self):
        return TAX_CALCULATORS.get(self.preset) if self.kind == "tax" else None


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

# Country tools for US, UK, Australian and EU visitors. Requirements and rates come
# from regional_data.py, which the pages and browser scripts share.
REGIONAL_TOOLS = (
    GrowthTool("us-passport-photo", "passport", "US Passport Photo Maker", (
        ("Can I use this to renew my passport online?", "For online renewal the State Department asks for your original, unedited photo and crops it itself. Use Check for online renewal to test the file, then upload that original file, not the cropped 2 × 2 version."),
        ("Where can I print the 6 × 4 sheet?", "Order a standard 4 × 6 inch photo print from a pharmacy or photo lab on matte or glossy photo paper. The sheet holds six 2 × 2 inch photos; cut along the edges and check that the head measures 1 to 1⅜ inches from chin to top of head."),
        ("Is my photo uploaded?", "No. The photo is checked and cropped in your browser. On first use the browser downloads the face and person models from Google's model host and the MediaPipe runtime from jsDelivr."),
    ), region="US", preset="us", summary="2 × 2 inch photo, print sheet and online-renewal check"),
    GrowthTool("uk-passport-photo", "passport", "UK Passport Photo Checker and Maker", (
        ("Should I crop my photo for an online application?", "No. HM Passport Office wants an unedited photo of your head, shoulders and upper body, at least 600 × 750 pixels and 50 KB to 10 MB, and crops it for you. Check your original here, then upload that file."),
        ("When do I need printed 35 × 45 mm photos?", "Paper applications need printed photos 45 mm high and 35 mm wide, with your head 29–34 mm from chin to crown. HM Passport Office asks for professional-quality prints on plain white photo paper, so take the sheet to a photo lab."),
        ("Is my photo uploaded?", "No. Checking and cropping run in your browser. The face and person models download from Google's model host and the runtime from jsDelivr on first use."),
    ), region="UK", preset="uk", summary="Check an online photo or make 35 × 45 mm prints"),
    GrowthTool("australian-passport-photo", "passport", "Australian Passport Photo Maker", (
        ("Can I use this photo to renew online?", "No. Australian online renewal retrieves your photo with a photo code from a participating photo provider. Use this tool when your application needs printed photos."),
        ("How should I print the photos?", "The Australian Passport Office asks for dye-sublimation prints on heavy glossy paper of at least 200 gsm, not inkjet prints. Photo kiosks commonly print this way. The 6 × 4 inch sheet holds eight 35 × 45 mm photos."),
        ("Is my photo uploaded?", "No. The photo is checked and cropped in your browser. The face and person models download from Google's model host and the runtime from jsDelivr on first use."),
    ), region="AU", preset="au", summary="35 × 45 mm photos on a 6 × 4 print sheet"),
    GrowthTool("uk-vat-calculator", "tax", "UK VAT Calculator", (
        ("How do I work out VAT from a price that includes VAT?", "Choose Remove VAT. At 20%, the VAT inside a VAT-inclusive price is one-sixth of it; the calculator divides by 1.2 for the net amount and rounds to the nearest penny."),
        ("Which VAT rate should I use?", "Most goods and services are standard-rated at 20%. Some, such as home energy and children's car seats, are 5%. Zero-rated items, such as most food and children's clothes, are 0%. HMRC's guidance lists the rate for each type of goods or service."),
        ("When does a business have to register for VAT?", "GOV.UK says you must register when your VAT-taxable turnover over the last 12 months goes over £90,000. Check HMRC guidance for your own situation."),
    ), region="UK", preset="uk", summary="Add or remove VAT at 20%, 5% or 0%"),
    GrowthTool("eu-vat-calculator", "tax", "EU VAT Calculator", (
        ("Which VAT rates are included?", f"The standard VAT rate of each of the 27 EU member states, as published for 2026 and checked in {EU_VAT_CHECKED}. Reduced rates depend on the product, so choose Custom rate to enter one."),
        ("Does it handle cross-border sales?", "No. It does the arithmetic for one rate. Rules such as the reverse charge for business customers and the One-Stop Shop for online sales to consumers in other countries can change which rate applies."),
        ("Can I type amounts with a decimal comma?", "Yes. Amounts such as 1.234,50 and 12,50 are read in the European format. Results are shown with a full stop as the decimal mark."),
    ), region="EU", preset="eu", summary="Standard VAT rates for all 27 member states"),
    GrowthTool("australian-gst-calculator", "tax", "Australian GST Calculator", (
        ("How do I work out GST from a GST-inclusive price?", "Choose Remove GST. At 10%, the GST inside a GST-inclusive price is one-eleventh of it; the calculator divides by 1.1 for the price before GST."),
        ("Which sales are GST-free?", "The ATO lists GST-free sales such as most basic food, some education courses and some health services. Choose Custom rate and enter 0 for a GST-free item."),
        ("When does a business need to register for GST?", "The ATO requires registration when your GST turnover is $75,000 or more, or $150,000 or more for a non-profit organisation."),
    ), region="AU", preset="au", summary="Add or remove 10% GST"),
    GrowthTool("us-sales-tax-calculator", "tax", "US Sales Tax Calculator", (
        ("Why is the result different from my receipt?", "Most states let cities, counties and special districts add their own sales tax. Enter your local rate so the calculator uses the same combined rate as your receipt."),
        ("Which states have no statewide sales tax?", "Alaska, Delaware, Montana, New Hampshire and Oregon. Some Alaska localities still charge a local sales tax."),
        ("How current are the state rates?", f"The state-level rates are as of {US_SALES_TAX_AS_OF}, from the Tax Foundation's compilation. Your state revenue department publishes the current rate if it has changed."),
    ), region="US", preset="us", summary="State rates plus your local rate"),
)

GROWTH_TOOLS = GROWTH_TOOLS + REGIONAL_TOOLS

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


REGIONAL_PAGES = (
    Page("us-passport-photo", "US Passport Photo Maker – 2×2 Inch Photo & Checker | SaveFromNet",
         "Make a 2 × 2 inch US passport photo and a 4 × 6 print sheet in your browser, or check a photo before you renew online.",
         "US Passport Photo Maker", "Crop your photo to the State Department's 2 × 2 inch format and print six copies on one 4 × 6 sheet, or check the original file for an online renewal.",
         (Section("Take a photo that can be cropped correctly", (
             "Stand in front of a plain white or off-white wall with even light and no shadows. Face the camera with a neutral expression or a natural smile, both eyes open, and remove eyeglasses: the State Department does not accept glasses in passport photos. Ask someone else to take the photo from about four feet away, so your head, shoulders and some space above your head are in the frame.",
             "Choose Make printed photos and select the photo. The tool finds your face, estimates your chin and the top of your head, and scales the photo so the head measures about 31 mm (1¼ inches) in a 2 × 2 inch frame, inside the 1 to 1⅜ inch range. The preview shows green lines for that range and a red chin line, so you can see whether the estimate is right before you download."),
             (("https://travel.state.gov/content/travel/en/passports/how-apply/photos.html", "State Department photo requirements"),)),
          Section("Printing, mailing and online renewal", (
             "Download the 6 × 4 inch sheet and order a standard 4 × 6 photo print on matte or glossy photo paper. It contains six 2 × 2 inch photos; cut along the edges and attach one as your form instructs. The photo must be in colour and taken within the last six months.",
             "Online renewal works differently: you upload the original photo, and the renewal service crops it. Choose Check for online renewal to test your original file against the 54 KB to 10 MB size limit and the framing and background guidance, then upload that same file. Acceptance is always decided by the passport agency; this tool checks the common causes of rejection but cannot guarantee approval."),
             (("https://travel.state.gov/en/passports/renew-replace/online/upload-digital-photo.html", "Uploading a photo for online renewal"), ("/portrait-background-remover", "Portrait background remover"))),
          ), schema_type="WebApplication"),
    Page("uk-passport-photo", "UK Passport Photo Checker & 35×45mm Maker | SaveFromNet",
         "Check a photo for a UK online passport application, or make 35 × 45 mm printed passport photos on a 6 × 4 sheet.",
         "UK Passport Photo Checker and Maker", "Check that your photo suits HM Passport Office's online rules, or crop it to 35 × 45 mm for a paper application.",
         (Section("Applying online: check, don't crop", (
             "For an online application, HM Passport Office wants the original photo: in colour, unaltered by software, at least 600 pixels wide and 750 pixels tall, between 50 KB and 10 MB, against a plain light-coloured background that contrasts with you. Include your head, shoulders and upper body. The service crops the photo itself, so cropping it beforehand can make it fail.",
             "Choose Check for online application and select the photo you plan to upload. The tool checks the file size and pixel dimensions, whether your head and shoulders are in view, whether your eyes are open and your mouth is closed, and whether the background looks plain and light. Nothing is changed; upload the same original file."),
             (("https://www.gov.uk/photos-for-passports", "GOV.UK passport photo rules"),)),
          Section("Paper applications: 35 × 45 mm prints", (
             "Printed photos must be 45 mm high and 35 mm wide, with your head 29–34 mm from the bottom of the chin to the crown, meaning the top of the head rather than the top of the hair. Choose Make printed photos: the tool aims for about 31.5 mm and lays out eight photos on a 6 × 4 inch sheet with cut guides.",
             "HM Passport Office asks for professionally printed photos on plain white photo paper, two identical copies, with no border. Take the downloaded sheet to a photo lab rather than printing it on a home inkjet printer, then check the head size on the print with a ruler."),
             (("/image-cropper", "Image cropper"),)),
          ), schema_type="WebApplication"),
    Page("australian-passport-photo", "Australian Passport Photo Maker – 35×45mm Print | SaveFromNet",
         "Make 35 × 45 mm Australian passport photos with a 32–36 mm face height, laid out on a 6 × 4 inch sheet for printing.",
         "Australian Passport Photo Maker", "Crop a photo to the Australian Passport Office's size and face-height rules, then print eight copies from one 6 × 4 inch sheet.",
         (Section("Size, face height and background", (
             "Australian passport photos must be 35–40 mm wide and 45–50 mm high, with the face 32–36 mm from the chin to the crown. This tool makes the 35 × 45 mm size, the smallest allowed, and aims for a 34 mm face. Use a plain white or light grey background that contrasts with your face, and keep the photo less than six months old.",
             "Choose Make printed photos and select a front-facing photo with space above your head and your shoulders visible. The preview marks the allowed face-height range in green and the chin in red. If the estimate misses the top of your head, retake the photo with your hair away from your forehead."),
             (("https://www.passports.gov.au/help/passport-photos", "Australian Passport Office photo guidelines"),)),
          Section("Printing and when this tool does not apply", (
             "The Passport Office asks for good-quality colour prints made by dye-sublimation on heavy glossy paper of at least 200 gsm. Inkjet prints are not accepted. Order the downloaded 6 × 4 inch sheet from a photo kiosk or lab, cut out two photos and check the face height with a ruler.",
             "Online renewal does not take an uploaded photo: it retrieves your photo through a photo code from a participating provider. Photo retouching is not permitted, so this tool only crops and resizes; it does not alter your face or background."),
             (("/portrait-background-remover", "Portrait background remover"),)),
          ), schema_type="WebApplication"),
    Page("uk-vat-calculator", "UK VAT Calculator – Add or Remove 20% VAT | SaveFromNet",
         "Add VAT to a net price or remove VAT from a gross price at the UK's 20%, 5% or 0% rates, with results to the penny.",
         "UK VAT Calculator", "Work out VAT at the standard 20%, reduced 5% or zero rate. Add VAT to a net price, or find the VAT inside a price that already includes it.",
         (Section("Add or remove VAT", (
             "To add VAT, enter the price before VAT and choose the rate: at 20%, a £100 net price becomes £120 with £20 VAT. To remove VAT, enter the VAT-inclusive price: at 20%, VAT is one-sixth of the total, so £120 contains £20 VAT and a £100 net price. Results update as you type and are rounded to the nearest penny.",
             "Choose Custom rate for anything other than the three UK rates, for example when checking an invoice from another country."),
             (("https://www.gov.uk/vat-rates", "GOV.UK VAT rates"),)),
          Section("Which rate applies", (
             "Most goods and services are standard-rated at 20%. The 5% reduced rate covers items such as domestic electricity and gas, children's car seats and smoking-cessation products. Zero-rated items, such as most food, children's clothes and footwear, and books and newspapers, carry 0% VAT. Exempt and out-of-scope items are different from zero-rated ones; HMRC's guidance explains each.",
             "Businesses must register for VAT when taxable turnover over the last 12 months goes over £90,000. This calculator does arithmetic only and is not tax advice; check HMRC guidance or an accountant for your circumstances."),
             (("https://www.gov.uk/guidance/rates-of-vat-on-different-goods-and-services", "HMRC VAT rates on goods and services"), ("/eu-vat-calculator", "EU VAT calculator"))),
          ), schema_type="WebApplication"),
    Page("eu-vat-calculator", "EU VAT Calculator – 2026 Rates for All 27 Countries | SaveFromNet",
         "Calculate VAT for any EU member state using its 2026 standard rate, or enter a reduced rate. Add or remove VAT instantly.",
         "EU VAT Calculator", "Choose an EU country to use its standard VAT rate, then add VAT to a net price or remove it from a gross price.",
         (Section("Standard VAT rates across the EU", (
             f"EU law sets a minimum standard VAT rate of 15% and no maximum, so rates range from 17% in Luxembourg to 27% in Hungary. The table below lists each member state's standard rate as published for 2026, checked in {EU_VAT_CHECKED}. Some regions, such as Madeira, the Azores and certain Greek islands, apply lower rates; the mainland rate is shown.",
             "Reduced rates vary by country and product, for example food, books or accommodation. Choose Custom rate and enter the reduced rate from the national tax authority when an item is not standard-rated."),
             (("https://taxation-customs.ec.europa.eu/taxation/vat/vat-directive/vat-rates_en", "European Commission VAT rates"), ("https://ec.europa.eu/taxation_customs/tedb/", "Taxes in Europe Database"))),
          Section("Adding, removing and checking invoices", (
             "To add VAT, enter the net amount: at Germany's 19%, €100 becomes €119. To remove VAT, enter the gross amount: €119 at 19% contains €19 of VAT. You can type amounts with a decimal comma, such as 1.234,50. Results are rounded to the nearest cent.",
             "The calculator does not decide which country's VAT applies. Cross-border business sales may use the reverse charge, and online sales to consumers in other member states may use the One-Stop Shop at the customer's rate. Check national guidance before invoicing."),
             (("/uk-vat-calculator", "UK VAT calculator"),)),
          ), schema_type="WebApplication"),
    Page("australian-gst-calculator", "Australian GST Calculator – Add or Remove 10% GST | SaveFromNet",
         "Add 10% GST to a price or work out the GST inside a GST-inclusive price, rounded to the cent.",
         "Australian GST Calculator", "Add GST to a price before tax, or find the GST included in a price, at Australia's 10% rate.",
         (Section("How GST is calculated", (
             "GST is a broad-based 10% tax on most goods, services and other items sold or consumed in Australia. To add GST, multiply the GST-exclusive price by 1.1: $100 becomes $110. To find the GST in a GST-inclusive price, divide by 11: $110 includes $10 GST. Enter an amount and the results update as you type.",
             "Choose Custom rate and enter 0 for GST-free sales, or another rate when checking an overseas invoice."),
             (("https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst", "ATO: GST"),)),
          Section("GST-free sales and registration", (
             "Some sales are GST-free, including most basic food, though food eaten on the premises is taxable and the ATO's food lists decide individual items. Businesses must register for GST when GST turnover is $75,000 or more, or $150,000 or more for non-profit organisations, and register within 21 days of reaching the threshold.",
             "This calculator does arithmetic only and is not tax advice. Use the ATO's guidance or a registered tax agent for decisions about your business."),
             (("https://www.ato.gov.au/businesses-and-organisations/gst-excise-and-indirect-taxes/gst/when-to-charge-gst-and-when-not-to/gst-free-sales", "ATO: GST-free sales"),)),
          ), schema_type="WebApplication"),
    Page("us-sales-tax-calculator", "US Sales Tax Calculator by State (2026 Rates) | SaveFromNet",
         "Calculate US sales tax with any state's 2026 base rate plus your local rate. Add tax to a price or find the pre-tax price.",
         "US Sales Tax Calculator", "Choose your state, add your city or county rate, and see the sales tax and total for a purchase.",
         (Section("State plus local sales tax", (
             f"The United States has no national sales tax. Forty-five states and the District of Columbia charge a statewide sales tax, listed below as of {US_SALES_TAX_AS_OF}, and most also let cities, counties and special districts add local rates. Choose your state, then enter your local rate to match the combined rate on a receipt.",
             "Alaska, Delaware, Montana, New Hampshire and Oregon have no statewide sales tax, though some Alaska localities charge one. Some items, such as groceries or prescription drugs, are taxed at a lower rate or exempt in many states; choose Custom rate when an item is taxed differently."),
             (("https://taxfoundation.org/data/all/state/sales-tax-rates/", "Tax Foundation state and local sales tax rates"),)),
          Section("Add tax or find the pre-tax price", (
             "To add sales tax, enter the price before tax: $100 at a combined 8.25% becomes $108.25. To work backwards from a total, choose Price includes tax and enter the total. Results are rounded to the nearest cent, as most registers do.",
             "Rates change, and your state revenue department publishes the official current rate for an address. This calculator does arithmetic only and is not tax advice."),
             (("/calculator", "Free online calculator"),)),
          ), schema_type="WebApplication"),
)

GROWTH_PAGES = GROWTH_PAGES + REGIONAL_PAGES
