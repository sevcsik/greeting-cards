#!/usr/bin/env python3
"""Prepare web-optimized audio assets from source files."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source" / "audio"
OUTPUT_DIR = ROOT / "public" / "assets" / "audio"
BITRATE = "128k"

TRACKS = [
    {"source": "eva.m4a", "output": "track1.m4a"},
    {"source": "margo.m4a", "output": "track2.m4a"},
    {"source": "lilla.m4a", "output": "track3.m4a"},
    {"source": "kati.m4a", "output": "track4.m4a"},
]


def require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not on PATH.", file=sys.stderr)
        sys.exit(1)


def convert_audio(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    extension = source.suffix.lower()

    if extension == ".m4a":
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-c:a",
            "copy",
            str(destination),
        ]
    else:
        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(source),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            BITRATE,
            "-ar",
            "44100",
            "-ac",
            "2",
            str(destination.with_suffix(".mp3")),
        ]
        destination = destination.with_suffix(".mp3")

    print(f"Preparing {source.name} -> {destination.name}")
    subprocess.run(command, check=True, capture_output=True)


def main() -> int:
    require_ffmpeg()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    prepared = 0
    for track in TRACKS:
        source = SOURCE_DIR / track["source"]
        if not source.exists():
            print(f"Missing source file: {source}", file=sys.stderr)
            continue

        convert_audio(source, OUTPUT_DIR / track["output"])
        prepared += 1

    if prepared == 0:
        existing = sorted(OUTPUT_DIR.glob("track*.*"))
        if existing:
            print(f"No source files found; keeping {len(existing)} existing asset(s).")
            return 0
        print(f"No audio sources found in {SOURCE_DIR}", file=sys.stderr)
        return 1

    for stale in OUTPUT_DIR.glob("track*.mp3"):
        stale.unlink()

    print(f"Done. {prepared} file(s) written to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
