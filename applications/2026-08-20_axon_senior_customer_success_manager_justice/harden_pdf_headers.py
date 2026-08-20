#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import fitz


APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR / "output"
RESUME_RENDER_DIR = OUTPUT_DIR / "rendered_training_v4"
COVER_RENDER_DIR = OUTPUT_DIR / "rendered_training_v3_cover"
NAVY = (13 / 255, 27 / 255, 42 / 255)
GOLD = (201 / 255, 168 / 255, 76 / 255)
HEADER_HEIGHT = 92.16
FONT_ROOT = Path(
    "/opt/codex/runtimes/codex-primary-runtime/dependencies/native/"
    "libreoffice-headless/libreoffice/share/fonts/truetype"
)
REGULAR_FONT = FONT_ROOT / "NotoSerif-Regular.ttf"
BOLD_FONT = FONT_ROOT / "NotoSerif-Bold.ttf"


def harden(source: Path, destination: Path) -> None:
    document = fitz.open(source)
    regular = fitz.Font(fontfile=str(REGULAR_FONT))
    bold = fitz.Font(fontfile=str(BOLD_FONT))
    contact_text = (
        "612-352-8647 | TroyHokanson@iCloud.com | "
        "https://linkedin.com/in/troyhokanson | troyhokanson.com"
    )
    links = [
        ("612-352-8647", "tel:6123528647"),
        ("TroyHokanson@iCloud.com", "mailto:TroyHokanson@iCloud.com"),
        ("https://linkedin.com/in/troyhokanson", "https://linkedin.com/in/troyhokanson"),
        ("troyhokanson.com", "https://troyhokanson.com"),
    ]
    for page in document:
        width = page.rect.width
        header = fitz.Rect(0, 0, width, HEADER_HEIGHT)
        page.add_redact_annot(header, fill=NAVY)
        page.apply_redactions()
        page.draw_rect(header, fill=NAVY, color=NAVY, overlay=True)

        page.insert_font(fontname="NotoSerif", fontfile=str(REGULAR_FONT))
        page.insert_font(fontname="NotoSerifBold", fontfile=str(BOLD_FONT))
        name = "Troy Hokanson"
        name_x = (width - bold.text_length(name, fontsize=26)) / 2
        page.insert_text(
            (name_x, 49), name, fontsize=26, fontname="NotoSerifBold", color=(1, 1, 1), overlay=True
        )
        page.draw_line(
            ((width - 336.6) / 2, 60),
            ((width + 336.6) / 2, 60),
            color=GOLD,
            width=0.75,
            overlay=True,
        )
        contact_x = (width - regular.text_length(contact_text, fontsize=9.5)) / 2
        page.insert_text(
            (contact_x, 76),
            contact_text,
            fontsize=9.5,
            fontname="NotoSerif",
            color=GOLD,
            overlay=True,
        )

        cursor = contact_x
        separator_width = regular.text_length(" | ", fontsize=9.5)
        for index, (text, uri) in enumerate(links):
            if index:
                cursor += separator_width
            text_width = regular.text_length(text, fontsize=9.5)
            page.insert_link(
                {
                    "kind": fitz.LINK_URI,
                    "from": fitz.Rect(cursor, 64, cursor + text_width, 79),
                    "uri": uri,
                }
            )
            cursor += text_width
    document.save(destination, garbage=4, deflate=True)
    document.close()


def main() -> None:
    files = [
        (
            RESUME_RENDER_DIR / "Hokanson_Resume_Axon_Sr_Customer_Success_Manager_Justice.pdf",
            OUTPUT_DIR / "Hokanson_Resume_Axon_Sr_Customer_Success_Manager_Justice.pdf",
        ),
        (
            COVER_RENDER_DIR / "Hokanson_Cover_Axon_Sr_Customer_Success_Manager_Justice.pdf",
            OUTPUT_DIR / "Hokanson_Cover_Axon_Sr_Customer_Success_Manager_Justice.pdf",
        ),
    ]
    for source, destination in files:
        harden(source, destination)
        print(destination)


if __name__ == "__main__":
    main()
