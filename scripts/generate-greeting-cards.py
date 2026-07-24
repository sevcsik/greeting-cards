#!/usr/bin/env python3
"""Compose greeting card images with QR codes on the paper and a caption."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from urllib.parse import quote, urlencode, urlsplit, urlunsplit

import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.constants import ERROR_CORRECT_M

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "site.config.json"
TEMPLATE_PATH = ROOT / "source" / "img" / "greeting-template.png"
OUTPUT_DIR = ROOT / "qrcodes" / "cards"
FONT_PATH = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")

# Measured on greeting-template.png (896x1195).  The QR belongs in the
# marked centre of the paper, below the girl's hands and chin.
PAPER_BOX = (240, 590, 679, 940)
# A 320 px code nearly fills the paper height while retaining a scan margin.
QR_BOX = (288, 605, 608, 925)
# The paper's top edge slopes slightly downward towards the right.
QR_ROTATION_DEGREES = -1.5
TEXT_BOTTOM_OFFSET = 68

TRACKS = [
    ("Éva néni", "Éva néninek"),
    ("Margó", "Margónak"),
    ("Lilla", "Lillának"),
    ("Kati", "Katinak"),
]


def load_base_url() -> str:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    base_url = config.get("baseUrl")
    if not base_url:
        raise ValueError("Missing baseUrl in site.config.json")
    return base_url.rstrip("/")


def slugify_filename(name: str) -> str:
    normalized = unicodedata.normalize("NFD", name)
    without_accents = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )
    return without_accents.lower().replace(" ", "-")


def build_track_url(base_url: str, track_name: str) -> str:
    query = urlencode({"track": track_name}, quote_via=quote)
    parts = urlsplit(f"{base_url}/")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, ""))


def make_qr_image(url: str, size: int) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(
        fill_color="#1b1410",
        back_color="#ffffff",
    ).convert("RGB")
    return image.resize((size, size), Image.Resampling.LANCZOS)


def compose_card(template: Image.Image, recipient: str, url: str) -> Image.Image:
    card = template.copy()
    draw = ImageDraw.Draw(card)

    left, top, right, bottom = QR_BOX
    qr_size = right - left
    qr = make_qr_image(url, qr_size)

    # Preserve the paper beneath the light QR modules.  This gives the QR
    # code's light areas precisely the same colour and texture as the paper.
    dark_modules = qr.convert("L").point(
        lambda value: 255 if value < 128 else 0
    )
    qr = qr.rotate(
        QR_ROTATION_DEGREES,
        resample=Image.Resampling.NEAREST,
        expand=True,
        fillcolor="#ffffff",
    )
    dark_modules = dark_modules.rotate(
        QR_ROTATION_DEGREES,
        resample=Image.Resampling.NEAREST,
        expand=True,
        fillcolor=0,
    )
    qr_x = (left + right - qr.width) // 2
    qr_y = (top + bottom - qr.height) // 2
    card.paste(qr, (qr_x, qr_y), dark_modules)

    caption = f"Micitől {recipient}"
    font_size = 34
    font = ImageFont.truetype(str(FONT_PATH), font_size)
    text_width = draw.textlength(caption, font=font)
    text_x = (card.width - text_width) // 2
    text_y = card.height - TEXT_BOTTOM_OFFSET

    shadow = "#ffffff"
    for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        draw.text((text_x + dx, text_y + dy), caption, font=font, fill=shadow)

    draw.text((text_x, text_y), caption, font=font, fill="#3b2a22")
    return card


def main() -> int:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Missing template image: {TEMPLATE_PATH}")

    base_url = load_base_url()
    template = Image.open(TEMPLATE_PATH).convert("RGB")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Paper box: {PAPER_BOX}")
    print(
        f"QR box: {QR_BOX} ({QR_BOX[2] - QR_BOX[0]} px, "
        f"{QR_ROTATION_DEGREES}°)"
    )

    for track_name, recipient in TRACKS:
        url = build_track_url(base_url, track_name)
        card = compose_card(template, recipient, url)
        output_path = OUTPUT_DIR / f"card-{slugify_filename(track_name)}.png"
        card.save(output_path, optimize=True)
        print(f"Generated {output_path.name} -> {url}")

    print(f"Done. Cards saved to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
