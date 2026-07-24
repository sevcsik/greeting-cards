#!/usr/bin/env python3
"""Copy and optimize the cover image into the public assets folder."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source" / "img"
OUTPUT_DIR = ROOT / "public" / "assets" / "img"
OUTPUT_NAME = "cover.jpg"
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".heic")


def find_cover() -> Path | None:
    for basename in ("cover", "background"):
        for extension in EXTENSIONS:
            candidate = SOURCE_DIR / f"{basename}{extension}"
            if candidate.exists():
                return candidate

    matches = sorted(
        path
        for path in SOURCE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in EXTENSIONS
    )
    return matches[0] if matches else None


def write_cover(source: Path, destination: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if source.suffix.lower() in {".jpg", ".jpeg"}:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-vf",
            "scale='min(1920,iw)':-2",
            "-q:v",
            "3",
            str(destination),
        ]
    else:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-vf",
            "scale='min(1920,iw)':-2",
            "-q:v",
            "3",
            str(destination),
        ]

    subprocess.run(command, check=True, capture_output=True)


def main() -> int:
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not on PATH.", file=sys.stderr)
        return 1

    source = find_cover()
    if source is None:
        existing = OUTPUT_DIR / OUTPUT_NAME
        if existing.exists():
            print(f"No source cover found; keeping existing {existing.name}.")
            return 0
        print(f"No cover image found in {SOURCE_DIR}", file=sys.stderr)
        return 1

    destination = OUTPUT_DIR / OUTPUT_NAME
    write_cover(source, destination)
    print(f"Cover prepared: {source.name} -> {destination.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
