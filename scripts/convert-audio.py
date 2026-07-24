#!/usr/bin/env python3
"""Convert source WAV files to web-optimized MP3 (128 kbps)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source" / "audio"
OUTPUT_DIR = ROOT / "public" / "assets" / "audio"
BITRATE = "128k"


def require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or not on PATH.", file=sys.stderr)
        sys.exit(1)


def convert_wav_to_mp3(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
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
        str(destination),
    ]
    print(f"Converting {source.name} -> {destination.name}")
    subprocess.run(command, check=True, capture_output=True)


def main() -> int:
    require_ffmpeg()

    wav_files = sorted(SOURCE_DIR.glob("*.wav"))
    if not wav_files:
        existing_mp3 = sorted(OUTPUT_DIR.glob("*.mp3"))
        if existing_mp3:
            print(
                f"No WAV files in {SOURCE_DIR}; "
                f"keeping {len(existing_mp3)} existing MP3 file(s)."
            )
            return 0
        print(f"No WAV files found in {SOURCE_DIR}", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for index, wav_path in enumerate(wav_files, start=1):
        output_name = f"track{index}.mp3"
        convert_wav_to_mp3(wav_path, OUTPUT_DIR / output_name)

    print(f"Done. {len(wav_files)} file(s) written to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
