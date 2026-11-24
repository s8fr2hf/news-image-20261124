#!/usr/bin/env python3
"""Entry program for news-image-20261124.

The image is drawn by render.py in this same repository. This program
re-renders it and writes it to $MAKEFUN_OUTPUT_DIR/entry.png (or
/output/entry.png), then validates the result: PNG magic, at most
1 MiB, exactly 1024 x 1024. Standard library only. Deterministic:
two runs produce byte-identical output.
"""

import os
import shutil
import subprocess
import sys

MAX_BYTES = 1048576
EXPECTED_SIZE = (1024, 1024)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    # Re-render the front page into a scratch directory, then move it
    # into place so a failed render never leaves a stale file behind.
    tmp_dir = os.path.join(out_dir, ".render-tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp_dir)
    subprocess.run([sys.executable, os.path.join(here, "render.py")],
                   check=True, env=env)

    src = os.path.join(tmp_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    shutil.rmtree(tmp_dir, ignore_errors=True)

    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    # Read width and height from the PNG IHDR chunk (bytes 16-24).
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != EXPECTED_SIZE:
        raise SystemExit("entry.png is %dx%d, expected 1024x1024"
                         % (width, height))

    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    print("wrote %s (%dx%d, %d bytes)" % (dest, width, height, len(data)))


if __name__ == "__main__":
    main()
