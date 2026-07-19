"""
Troy Hokanson - Locked PDF Header Module
=======================================

Single source of truth for the navy/gold/white header on every PDF resume,
cover letter, CV, or other PDF artifact bearing Troy's name.

Locked header requirements:
- Full-bleed navy #0D1B2A bar, zero whitespace above, left, or right.
- "Troy Hokanson" in white #FFFFFF Garamond-family bold, centered, 26 pt on page 1.
- Thin gold #C9A84C rule beneath the name.
- Gold Garamond contact row, pipe-separated, centered.
- No subtitle or role title between name and contact row.
- No footer by default.

Do not hand-roll the header in build scripts. Import draw_page1_header.
"""

import os
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import (
    TROY_NAME,
    TROY_PHONE,
    TROY_EMAIL,
    TROY_LOCATION,
    TROY_LINKEDIN,
    TROY_PORTFOLIO,
)

BRAND = {
    "navy": HexColor("#0D1B2A"),
    "gold": HexColor("#C9A84C"),
    "white": HexColor("#FFFFFF"),
    "steel": HexColor("#2D6A9F"),
    "black": HexColor("#141414"),
    "gray": HexColor("#555555"),
}

NAME = TROY_NAME or "Troy Hokanson"
_phone_digits = TROY_PHONE.replace(".", "").replace("-", "").replace(" ", "")
CONTACT_PARTS = [
    part
    for part in [
        TROY_LOCATION,
        TROY_PHONE if TROY_PHONE else None,
        TROY_EMAIL,
        TROY_LINKEDIN,
        "TroyHokanson.com",
    ]
    if part
]
CONTACT_LINKS = {
    **({TROY_PHONE: f"tel:+1{_phone_digits}"} if TROY_PHONE else {}),
    TROY_EMAIL: f"mailto:{TROY_EMAIL}",
    TROY_LINKEDIN: f"https://www.{TROY_LINKEDIN}"
    if TROY_LINKEDIN and not TROY_LINKEDIN.startswith("http")
    else TROY_LINKEDIN,
    "TroyHokanson.com": TROY_PORTFOLIO,
}

MARGIN = {
    "left": 0.6 * inch,
    "right": 0.6 * inch,
    "top_page1": 1.55 * inch,
    "top_pageN": 0.67 * inch,
    "bottom": 0.55 * inch,
}

PAGE1_BANNER_HEIGHT = 1.45 * inch
PAGEN_BANNER_HEIGHT = 0.42 * inch
SEPARATOR = "   |   "

_FONTS_REGISTERED = False


def _register_fonts():
    """Register Garamond-family and fallback fonts if available."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return

    candidates = {
        "Garamond-Bold": [
            "/usr/share/fonts/truetype/ebgaramond/EBGaramond-Bold.ttf",
            "/usr/share/fonts/ebgaramond/EBGaramond-Bold.ttf",
            "/home/user/workspace/templates/fonts/EBGaramond-Bold.ttf",
        ],
        "Garamond": [
            "/usr/share/fonts/truetype/ebgaramond/EBGaramond-Regular.ttf",
            "/usr/share/fonts/ebgaramond/EBGaramond-Regular.ttf",
            "/home/user/workspace/templates/fonts/EBGaramond-Regular.ttf",
        ],
    }

    for name, paths in candidates.items():
        for path in paths:
            if os.path.exists(path):
                try:
                    pdfmetrics.registerFont(TTFont(name, path))
                    break
                except Exception:
                    pass
    _FONTS_REGISTERED = True


def _safe_font(preferred, fallback):
    try:
        pdfmetrics.getFont(preferred)
        return preferred
    except Exception:
        return fallback


def draw_page1_header(c, pagesize, *, name=NAME, contact_parts=CONTACT_PARTS, contact_links=None):
    """Draw the full page-1 navy header."""
    _register_fonts()
    if contact_links is None:
        contact_links = CONTACT_LINKS

    page_w, page_h = pagesize
    band_h = PAGE1_BANNER_HEIGHT
    band_y = page_h - band_h

    c.setFillColor(BRAND["navy"])
    c.rect(-0.05 * inch, band_y - 0.05 * inch, page_w + 0.1 * inch, band_h + 0.1 * inch, fill=1, stroke=0)

    name_font = _safe_font("Garamond-Bold", "Helvetica-Bold")
    c.setFillColor(BRAND["white"])
    c.setFont(name_font, 26)
    name_y = band_y + band_h - 0.52 * inch
    c.drawCentredString(page_w / 2, name_y, name)

    c.setStrokeColor(BRAND["gold"])
    c.setLineWidth(0.90)
    rule_y = name_y - 0.17 * inch
    rule_inset = page_w * 0.225
    c.line(rule_inset, rule_y, page_w - rule_inset, rule_y)

    contact_font = _safe_font("Garamond", "Helvetica")
    c.setFillColor(BRAND["gold"])
    c.setFont(contact_font, 9.5)

    contact_text = SEPARATOR.join(contact_parts)
    text_w = c.stringWidth(contact_text, contact_font, 9.5)
    contact_y = rule_y - 0.25 * inch
    start_x = (page_w - text_w) / 2
    c.drawString(start_x, contact_y, contact_text)

    cursor_x = start_x
    sep_w = c.stringWidth(SEPARATOR, contact_font, 9.5)
    for index, part in enumerate(contact_parts):
        part_w = c.stringWidth(part, contact_font, 9.5)
        url = contact_links.get(part)
        if url:
            c.linkURL(url, (cursor_x, contact_y - 2, cursor_x + part_w, contact_y + 10), relative=0)
        cursor_x += part_w
        if index < len(contact_parts) - 1:
            cursor_x += sep_w


def draw_pageN_header(c, pagesize, *, name=NAME):
    """Draw the slim page-2+ navy header."""
    _register_fonts()
    page_w, page_h = pagesize
    band_h = PAGEN_BANNER_HEIGHT
    band_y = page_h - band_h

    c.setFillColor(BRAND["navy"])
    c.rect(-0.05 * inch, band_y - 0.05 * inch, page_w + 0.1 * inch, band_h + 0.1 * inch, fill=1, stroke=0)

    name_font = _safe_font("Garamond-Bold", "Helvetica-Bold")
    c.setFillColor(BRAND["white"])
    c.setFont(name_font, 16)
    c.drawCentredString(page_w / 2, band_y + band_h / 2 - 5, name)


def build_footer(canvas, doc, *, show_page_numbers=False):
    """No-op by design. Troy's current locked standard uses no footer."""
    return None


def clean_pdf_metadata(path, *, title="", subject="", keywords=""):
    try:
        import pypdf
    except ImportError:
        return

    reader = pypdf.PdfReader(path)
    writer = pypdf.PdfWriter(clone_from=reader)
    writer.add_metadata(
        {
            "/Author": "Troy Hokanson",
            "/Creator": "Adobe Acrobat Pro",
            "/Producer": "",
            "/Title": title or "",
            "/Subject": subject or "",
            "/Keywords": keywords or "",
        }
    )
    with open(path, "wb") as file_handle:
        writer.write(file_handle)


__all__ = [
    "BRAND",
    "NAME",
    "CONTACT_PARTS",
    "CONTACT_LINKS",
    "MARGIN",
    "PAGE1_BANNER_HEIGHT",
    "PAGEN_BANNER_HEIGHT",
    "draw_page1_header",
    "draw_pageN_header",
    "build_footer",
    "clean_pdf_metadata",
]
