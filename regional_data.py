"""Official requirements and published tax rates behind the US, UK, Australia and EU tools.

Each value here is rendered on its page and read by the browser scripts, so the
displayed rule and the calculation always match. Sources are linked on the pages.
"""

# Printed passport photo rules. Head height is measured from the bottom of the
# chin. "skull" means the top of the head, not the top of the hair (UK and
# Australian guidance); "hair" follows the US digital guidance, which includes hair.
PASSPORT_SPECS = {
    "us": {
        "country": "United States",
        "document": "US passport",
        "photo_mm": [50.8, 50.8],
        "photo_px": [600, 600],
        "photo_label": "2 × 2 inches (51 × 51 mm)",
        "head_mm": [25.4, 34.9],
        "head_label": "1 to 1⅜ inches (25–35 mm) from chin to top of head",
        "target_head_mm": 31,
        "head_basis": "hair",
        "top_ratio": 0.32,
        "background": "Plain white or off-white, with no shadows",
        "background_kind": "white",
        "sheet": {"label": "6 × 4 inch print (6 photos)", "px": [1800, 1200], "gap_px": 0},
        "print_note": "Order a standard 4 × 6 inch photo print on matte or glossy photo paper, then cut along the photo edges.",
        "online": {"label": "Online passport renewal upload", "min_kb": 54, "max_kb": 10240,
                   "formats": ["JPEG", "PNG", "HEIC", "HEIF"], "min_px": None,
                   "note": "Upload the original photo. The renewal service crops it; do not crop, edit or filter it yourself."},
        "official_url": "https://travel.state.gov/content/travel/en/passports/how-apply/photos.html",
        "official_label": "US Department of State passport photo requirements",
    },
    "uk": {
        "country": "United Kingdom",
        "document": "UK passport",
        "photo_mm": [35, 45],
        "photo_px": [413, 531],
        "photo_label": "35 mm wide × 45 mm high",
        "head_mm": [29, 34],
        "head_label": "29–34 mm from chin to crown (top of the head, not the hair)",
        "target_head_mm": 31.5,
        "head_basis": "skull",
        "top_ratio": 0.35,
        "background": "Plain light colour such as cream or light grey, in clear contrast to you",
        "background_kind": "light",
        "sheet": {"label": "6 × 4 inch print (8 photos)", "px": [1800, 1200], "gap_px": 24},
        "print_note": "HM Passport Office asks for professionally printed photos on plain white photo paper. Use a photo lab, not a home inkjet printer.",
        "online": {"label": "Online passport application upload", "min_kb": 50, "max_kb": 10240,
                   "formats": None, "min_px": [600, 750],
                   "note": "Upload the original, unedited photo showing your head, shoulders and upper body. HM Passport Office crops it for you."},
        "official_url": "https://www.gov.uk/photos-for-passports",
        "official_label": "GOV.UK passport photo rules",
    },
    "au": {
        "country": "Australia",
        "document": "Australian passport",
        "photo_mm": [35, 45],
        "photo_px": [413, 531],
        "photo_label": "35 mm wide × 45 mm high (allowed: 35–40 × 45–50 mm)",
        "head_mm": [32, 36],
        "head_label": "32–36 mm from chin to crown (top of the head)",
        "target_head_mm": 34,
        "head_basis": "skull",
        "top_ratio": 0.4,
        "background": "Plain white or light grey that contrasts with your face",
        "background_kind": "light",
        "sheet": {"label": "6 × 4 inch print (8 photos)", "px": [1800, 1200], "gap_px": 24},
        "print_note": "The Australian Passport Office asks for dye-sublimation prints on heavy glossy paper (at least 200 gsm). Photo kiosks usually print this way; inkjet prints are not accepted.",
        "online": None,
        "official_url": "https://www.passports.gov.au/help/passport-photos",
        "official_label": "Australian Passport Office photo guidelines",
    },
}

# Standard VAT rates of the 27 member states, as published for 2026 (checked
# October 2026). Some regions, such as Madeira, the Azores and certain Greek
# islands, apply lower rates; the standard mainland rate is listed.
EU_VAT_RATES = (
    ("AT", "Austria", 20), ("BE", "Belgium", 21), ("BG", "Bulgaria", 20),
    ("HR", "Croatia", 25), ("CY", "Cyprus", 19), ("CZ", "Czechia", 21),
    ("DK", "Denmark", 25), ("EE", "Estonia", 24), ("FI", "Finland", 25.5),
    ("FR", "France", 20), ("DE", "Germany", 19), ("GR", "Greece", 24),
    ("HU", "Hungary", 27), ("IE", "Ireland", 23), ("IT", "Italy", 22),
    ("LV", "Latvia", 21), ("LT", "Lithuania", 21), ("LU", "Luxembourg", 17),
    ("MT", "Malta", 18), ("NL", "Netherlands", 21), ("PL", "Poland", 23),
    ("PT", "Portugal", 23), ("RO", "Romania", 21), ("SK", "Slovakia", 23),
    ("SI", "Slovenia", 22), ("ES", "Spain", 21), ("SE", "Sweden", 25),
)
EU_VAT_CHECKED = "October 2026"

UK_VAT_RATES = (("Standard rate", 20), ("Reduced rate", 5), ("Zero rate", 0))
AU_GST_RATE = 10

# State-level sales tax rates as of 1 January 2026 (Tax Foundation). Local city,
# county and district taxes are added on top in most states.
US_STATE_SALES_TAX = (
    ("AL", "Alabama", 4), ("AK", "Alaska", 0), ("AZ", "Arizona", 5.6),
    ("AR", "Arkansas", 6.5), ("CA", "California", 7.25), ("CO", "Colorado", 2.9),
    ("CT", "Connecticut", 6.35), ("DE", "Delaware", 0), ("DC", "District of Columbia", 6),
    ("FL", "Florida", 6), ("GA", "Georgia", 4), ("HI", "Hawaii", 4),
    ("ID", "Idaho", 6), ("IL", "Illinois", 6.25), ("IN", "Indiana", 7),
    ("IA", "Iowa", 6), ("KS", "Kansas", 6.5), ("KY", "Kentucky", 6),
    ("LA", "Louisiana", 5), ("ME", "Maine", 5.5), ("MD", "Maryland", 6),
    ("MA", "Massachusetts", 6.25), ("MI", "Michigan", 6), ("MN", "Minnesota", 6.875),
    ("MS", "Mississippi", 7), ("MO", "Missouri", 4.225), ("MT", "Montana", 0),
    ("NE", "Nebraska", 5.5), ("NV", "Nevada", 6.85), ("NH", "New Hampshire", 0),
    ("NJ", "New Jersey", 6.625), ("NM", "New Mexico", 4.875), ("NY", "New York", 4),
    ("NC", "North Carolina", 4.75), ("ND", "North Dakota", 5), ("OH", "Ohio", 5.75),
    ("OK", "Oklahoma", 4.5), ("OR", "Oregon", 0), ("PA", "Pennsylvania", 6),
    ("RI", "Rhode Island", 7), ("SC", "South Carolina", 6), ("SD", "South Dakota", 4.2),
    ("TN", "Tennessee", 7), ("TX", "Texas", 6.25), ("UT", "Utah", 6.1),
    ("VT", "Vermont", 6), ("VA", "Virginia", 5.3), ("WA", "Washington", 6.5),
    ("WV", "West Virginia", 6), ("WI", "Wisconsin", 5), ("WY", "Wyoming", 4),
)
US_SALES_TAX_AS_OF = "January 1, 2026"

# Per-calculator settings rendered into the page and read by tax-tools.mjs.
TAX_CALCULATORS = {
    "uk": {"tax": "VAT", "locale": "en-GB", "currency": "GBP",
           "rates": [{"label": f"{name} ({rate}%)", "rate": rate} for name, rate in UK_VAT_RATES]},
    "eu": {"tax": "VAT", "locale": "en-IE", "currency": None,
           "rates": [{"label": f"{name} ({rate}%)", "name": name, "rate": rate, "code": code} for code, name, rate in EU_VAT_RATES]},
    "au": {"tax": "GST", "locale": "en-AU", "currency": "AUD",
           "rates": [{"label": f"GST ({AU_GST_RATE}%)", "rate": AU_GST_RATE}]},
    "us": {"tax": "sales tax", "locale": "en-US", "currency": "USD", "local_rate": True,
           "rates": [{"label": f"{name} ({rate}% state rate)", "name": name, "rate": rate, "code": code}
                     for code, name, rate in US_STATE_SALES_TAX]},
}
