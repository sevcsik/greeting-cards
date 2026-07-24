#!/usr/bin/env python3
"""Compose greeting card images with QR codes on the paper and a caption."""

from __future__ import annotations

import json
import unicodedata
from io import BytesIO
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

# White paper area on the template (px): left, top, right, bottom
PAPER_BOX = (176, 562, 720, 658)
PAPER_PADDING = 0.05
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
    image = qr.make_image(fill_color="#1b1410", back_color="#ffffff").convert("RGB")
    return image.resize((size, size), Image.Resampling.LANCZOS)


def paper_inner_box(paper_box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    left, top, right, bottom = paper_box
    width = right - left
    height = bottom - top
    pad_x = int(width * PAPER_PADDING)
    pad_y = int(height * PAPER_PADDING)
    return left + pad_x, top + pad_y, right - pad_x, bottom - pad_y


def compose_card(template: Image.Image, track_name: str, recipient: str, url: str) -> Image.Image:
    card = template.copy()
    draw = ImageDraw.Draw(card)

    inner = paper_inner_box(PAPER_BOX)
    inner_width = inner[2] - inner[0]
    inner_height = inner[3] - inner[1]
    qr_size = min(inner_width, inner_height)
    qr = make_qr_image(url, qr_size)

    qr_x = inner[0] + (inner_width - qr_size) // 2
    qr_y = inner[1] + (inner_height - qr_size) // 2

    # Subtle white backing for reliable scanning on textured paper.
    margin = max(4, qr_size // 40)
    draw.rectangle(
        (qr_x - margin, qr_y - margin, qr_x + qr_size + margin, qr_y + qr_size + margin),
        fill="#ffffff",
    )
    card.paste(qr, (qr_x, qr_y))

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

    for track_name, recipient in TRACKS:
        url = build_track_url(base_url, track_name)
        card = compose_card(template, track_name, recipient, url)
        output_path = OUTPUT_DIR / f"card-{slugify_filename(track_name)}.png"
        card.save(output_path, optimize=True)
        print(f"Generated {output_path.name} -> {url}")

    print(f"Done. Cards saved to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
