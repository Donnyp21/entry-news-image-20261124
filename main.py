"""news-image-20261124 entry: Tuesday 24 November 2026's world news,
summed up in one picture.

The entry is a pre-made newspaper front page ("TUESDAY 24 NOVEMBER
2026") painted from scratch by gen_image.py -- PIL shapes and text,
no photographs, no borrowed artwork. Its stories were verified
against reporting dated 24 Nov 2026 by web search:

  LEAD: Ukraine says its naval drones sank the Russian corvette
  Merkury at the Benghazi naval base in Libya on 23 Nov -- the
  Black Sea fight reaching the Mediterranean. Libya demands
  explanations from Kyiv; the UN seeks a probe.
  1. Russia testing Article 5: 25 airspace violations against
  NATO members in 2026, four times the 2024 total; two missiles
  and a drone crashed in Poland on 20 Nov.
  2. ICJ Rohingya ruling: 14 countries (UK, Spain, Canada,
  Australia + 10) recognise the ruling that Myanmar committed
  genocide against the Rohingya.
  3. Markets surge on Nvidia reinstating Jensen Huang after
  Trump intervened: Kospi +6-7%, Nikkei +3.91%, Nasdaq +6.51%,
  S&P 500 +4.73%.
  4. US Treasury sanctions two dozen-plus Iranian exchange
  houses; Hormuz mines / Gulf strike tensions; Iran rules out
  negotiation until Washington meets 7 conditions.
  Strip: Putin reportedly open to Article 5-style security
  guarantees for Ukraine if no NATO troops deploy.
  Bottom strip: COP31 collapsed in Antalya over fossil-fuel
  wording (first failure since 2009; COP32 to Addis Ababa);
  Nepal quake 5.6 near the China border; factory fire in
  Cikande, Indonesia, with casualties; 9th measles death in
  Pennsylvania.

This program checks the finished artwork (art.jpg, beside this file)
against the competition's caps and copies it to the output directory
as entry.png. The rules tell PNG from JPEG by the file's first bytes,
so the name stays entry.png while the bytes stay JPEG.

Python 3.13 standard library only. No network. Deterministic: the
output is a byte-for-byte copy of art.jpg.
"""

import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576   # the rules cap the output at 1 MiB
MAX_SIDE = 1024         # and at 1024 x 1024 pixels
ARTWORK = "art.jpg"
OUTPUT_NAME = "entry.png"

# JPEG markers that carry no length field (SOI, EOI, TEM, RST0-7).
LONE_MARKERS = frozenset({0x01, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4,
                          0xD5, 0xD6, 0xD7, 0xD8, 0xD9})
# Start-of-frame markers, whose segment stores the picture's size.
FRAME_MARKERS = frozenset({0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                           0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF})


def dimensions(blob):
    """Return (width, height) of a JPEG held in memory."""
    if blob[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG: missing start-of-image marker")
    pos = 2
    while True:
        if pos + 2 > len(blob) or blob[pos] != 0xFF:
            raise ValueError("not a JPEG: segment header missing")
        marker = blob[pos + 1]
        pos += 2
        if marker in LONE_MARKERS:
            if marker == 0xD9:
                break
            continue
        if pos + 2 > len(blob):
            raise ValueError("not a JPEG: truncated segment")
        seg_len = struct.unpack_from(">H", blob, pos)[0]
        if seg_len < 2:
            raise ValueError("not a JPEG: bad segment length")
        if marker in FRAME_MARKERS:
            if pos + 7 > len(blob):
                raise ValueError("not a JPEG: truncated frame segment")
            height, width = struct.unpack_from(">HH", blob, pos + 3)
            return width, height
        pos += seg_len
    raise ValueError("not a JPEG: no start-of-frame segment found")


def is_complete(blob):
    """True when the bytes end with the JPEG end marker."""
    return blob[-2:] == b"\xff\xd9"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, ARTWORK)
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("MAKEFUN_OUTPUT")
               or "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)

    try:
        with open(source, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        return fail(f"cannot read {ARTWORK}: {exc}")
    nbytes = len(blob)
    if not 0 < nbytes <= MAX_BYTES:
        return fail(f"{ARTWORK} is {nbytes} bytes, outside 1..{MAX_BYTES}")
    try:
        width, height = dimensions(blob)
    except ValueError as exc:
        return fail(str(exc))
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail(f"{ARTWORK} is {width}x{height}, "
                    f"over the {MAX_SIDE}x{MAX_SIDE} cap")
    if not is_complete(blob):
        return fail(f"{ARTWORK} has no end-of-image marker")
    print(f"checked {ARTWORK}: {width}x{height}, {nbytes} bytes")

    shutil.copyfile(source, target)
    if os.path.getsize(target) != nbytes:
        return fail("the copy's size differs from the artwork")
    print(f"wrote {target}: {nbytes} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
