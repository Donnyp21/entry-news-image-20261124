"""Ship the news-image-20261124 front page.

The artwork (art.jpg, painted at build time by gen_image.py) is a
finished 1024x1024 JPEG of Tuesday 24 November 2026's world news:
Ukraine's sea drones sinking a Russian corvette off Libya, Russia
testing NATO skies, fourteen nations backing the ICJ Rohingya
ruling, a markets surge on the Nvidia U-turn, US sanctions on
Iranian exchange houses, and the rest of the day in brief.

This program is the graded entry. It does three things:

  1. reads art.jpg from beside itself,
  2. proves the bytes are a whole JPEG inside the contest caps
     (at most 1 MiB, at most 1024 pixels on a side), and
  3. writes them, unchanged, to entry.png in the output folder.

The rules tell PNG from JPEG by the first bytes, so the file keeps
the name entry.png while its bytes stay JPEG. Pure standard
library, no network, and the output is a byte-for-byte copy, so
two runs write identical files.
"""

import os
import sys
from pathlib import Path

LIMIT_BYTES = 1024 * 1024
LIMIT_SIDE = 1024
SOURCE_NAME = "art.jpg"
ENTRY_NAME = "entry.png"

# Markers with no length field and no payload: TEM, RST0..RST7,
# SOI and EOI.
BARE = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))
# Start-of-frame markers; their payload opens with the picture size.
FRAMES = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


class BadArtwork(Exception):
    """The artwork bytes fail one of the contest's checks."""


def segments(data):
    """Yield (marker, payload) for each segment of a JPEG stream."""
    if data[:2] != b"\xff\xd8":
        raise BadArtwork("missing the JPEG start-of-image marker")
    at = 2
    while at < len(data):
        if data[at] != 0xFF:
            raise BadArtwork(f"segment at byte {at} has no marker prefix")
        marker = data[at + 1]
        at += 2
        if marker in BARE:
            yield marker, b""
            if marker == 0xD9:
                return
            continue
        span = int.from_bytes(data[at:at + 2], "big")
        if span < 2 or at + span > len(data):
            raise BadArtwork("a segment length runs past the file's end")
        yield marker, data[at + 2:at + span]
        at += span
        if marker == 0xDA:  # start of scan: entropy data follows
            return
    raise BadArtwork("the stream ends before any end-of-image marker")


def picture_size(data):
    """(width, height) from the first start-of-frame segment."""
    for marker, payload in segments(data):
        if marker in FRAMES:
            if len(payload) < 5:
                raise BadArtwork("the frame segment is too short")
            height = int.from_bytes(payload[1:3], "big")
            width = int.from_bytes(payload[3:5], "big")
            return width, height
    raise BadArtwork("no start-of-frame segment in the stream")


def check(data):
    """Validate the artwork against the caps; return its size."""
    if not data:
        raise BadArtwork("the artwork file is empty")
    if len(data) > LIMIT_BYTES:
        raise BadArtwork(f"{len(data)} bytes is over the 1 MiB cap")
    if not data.endswith(b"\xff\xd9"):
        raise BadArtwork("no end-of-image marker: the JPEG is cut short")
    width, height = picture_size(data)
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        raise BadArtwork(f"{width}x{height} is over the 1024x1024 cap")
    return width, height


def output_dir():
    for var in ("MAKEFUN_OUTPUT_DIR", "MAKEFUN_OUTPUT"):
        if os.environ.get(var):
            return Path(os.environ[var])
    return Path("/output")


def run():
    folder = Path(__file__).resolve().parent
    try:
        data = (folder / SOURCE_NAME).read_bytes()
    except OSError as exc:
        print(f"cannot read {SOURCE_NAME}: {exc}", file=sys.stderr)
        return 1
    try:
        width, height = check(data)
    except BadArtwork as exc:
        print(f"artwork rejected: {exc}", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / ENTRY_NAME
    dest.write_bytes(data)
    if dest.read_bytes() != data:
        print("the written file's bytes differ from the artwork",
              file=sys.stderr)
        return 1
    print(f"{SOURCE_NAME}: {width}x{height}, {len(data)} bytes -> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
