#!/usr/bin/env python3
"""news-26 b28 — entry runner (STDLIB ONLY).

Layout V26: three heroes stacked down the left 45% column, a 2x5 card grid
in the right 55% column, and a full-width bottom band holding the world map
(left 40%) beside a three-column ALSO list (right 60%). 50 stories total.

The artwork is rendered at build time by gen.py (Pillow) into entry.png,
which is committed in this repo. The grader environment is stdlib-only, so
this runner deliberately imports nothing beyond the standard library: it
only copies the pre-rendered image into the grader output directory and
verifies the copy byte-for-byte before reporting success.

Output contract:
  - destination is $MAKEFUN_OUTPUT_DIR/entry.png (default "out/entry.png")
  - the copy must be a valid PNG, 1024x1024, with the expected sha256
  - exit code 0 means the entry image is in place and verified
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
DST = os.path.join(DST_DIR, "entry.png")

# sha256 of the committed entry.png, filled in after the final render.
EXPECTED_SHA256 = "85a3c7bf53cd0647b0a992a7a432a4d8dee64d8b06b83b272a4b4043d068004c"
EXPECTED_SIZE = 233366
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    """Stream a file through sha256 without loading it all at once."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Read width/height from the PNG IHDR chunk (stdlib struct only)."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError("PNG IHDR chunk missing")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_source():
    """Validate the committed artwork before copying it anywhere."""
    if not os.path.isfile(SRC):
        print("entry.png missing next to main.py", file=sys.stderr)
        return None
    size = os.path.getsize(SRC)
    if size != EXPECTED_SIZE:
        print(f"entry.png size {size} != expected {EXPECTED_SIZE}",
              file=sys.stderr)
        return None
    digest = sha256_of(SRC)
    if digest != EXPECTED_SHA256:
        print(f"entry.png sha mismatch: {digest}", file=sys.stderr)
        return None
    width, height = png_dimensions(SRC)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print(f"entry.png is {width}x{height}, expected "
              f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}", file=sys.stderr)
        return None
    return size, digest


def main():
    checked = check_source()
    if checked is None:
        return 1
    size, digest = checked
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    if sha256_of(DST) != digest:
        print("copy verification failed", file=sys.stderr)
        return 1
    print(f"wrote {DST} ({size} bytes, sha256 {digest})")
    print("entry: 50 stories, 1024x1024, layout V26 — heroes left, "
          "cards right, map + ALSO below")
    return 0


if __name__ == "__main__":
    sys.exit(main())
