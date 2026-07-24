#!/usr/bin/env python3
"""Generate QR codes for the site root and per-track deep links."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "site.config.json"
OUTPUT_DIR = ROOT / "qrcodes"
TRACK_COUNT = 4


def load_base_url() -> str:
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        base_url = config.get("baseUrl")
        if base_url:
            return base_url.rstrip("/")

    print(
        "Missing baseUrl in site.config.json. "
        "Set githubUsername and repositoryName first.",
        file=sys.stderr,
    )
    sys.exit(1)


def write_qr_code(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#041018", back_color="#ffffff")
    image.save(destination)
    print(f"Generated {destination.name} -> {url}")


def main() -> int:
    base_url = load_base_url()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_qr_code(f"{base_url}/", OUTPUT_DIR / "main.png")

    for track_number in range(1, TRACK_COUNT + 1):
        write_qr_code(
            f"{base_url}/?track={track_number}",
            OUTPUT_DIR / f"track-{track_number}.png",
        )

    print(f"Done. QR codes saved to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
