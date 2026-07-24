#!/usr/bin/env python3
"""Copy the source background image into the public assets folder."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source" / "img"
OUTPUT_DIR = ROOT / "public" / "assets" / "img"
OUTPUT_NAME = "background.jpg"
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def find_background() -> Path | None:
    for extension in EXTENSIONS:
        candidate = SOURCE_DIR / f"background{extension}"
        if candidate.exists():
            return candidate

    matches = sorted(
        path
        for path in SOURCE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in EXTENSIONS
    )
    return matches[0] if matches else None


def main() -> int:
    source = find_background()
    if source is None:
        print(f"No background image found in {SOURCE_DIR}", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / OUTPUT_NAME

    if source.suffix.lower() in {".jpg", ".jpeg"}:
        shutil.copy2(source, destination)
    else:
        import subprocess

        subprocess.run(
            ["ffmpeg", "-y", "-i", str(source), "-q:v", "2", str(destination)],
            check=True,
            capture_output=True,
        )

    print(f"Background copied: {source.name} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
