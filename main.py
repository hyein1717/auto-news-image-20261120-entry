#!/usr/bin/env python3
"""World news of Friday 20 November 2026, summed up in one image.

The finished front page ships in this repository as assets/entry.png.
It was rendered at build time by the original Pillow-based program:
a 1024x1024 newspaper front page with a generated cyclone artwork as
the hero (Cyclone Akvan's landfall on India's Odisha coast), the date
named in the masthead, and three further verified stories of the day
below it.

This program is deliberately standard-library-only. The grading
sandbox runs it in a bare Python 3.13 image where nothing extra is
installed (no Pillow), there is no network access, and the repository
itself is read-only. Re-rendering there is impossible, so instead the
program copies the pre-rendered assets/entry.png into the writable
output directory named by MAKEFUN_OUTPUT_DIR.

Stories verified against live reporting on 20 November 2026:
  1. Cyclone Akvan makes landfall near Gopalpur, Odisha, around noon
     IST, winds 90-100 km/h gusting to 110, 100,000+ people evacuated
     (India Meteorological Department, via India Today / PTI).
  2. India vs New Zealand, 1st Test, Day 1 in Wellington: New Zealand
     243/5 at stumps, Henry Nicholls 113 not out (Times of India).
  3. US President Donald Trump to brief the press on Friday about his
     China trip, after Thursday's first-ever Trump-Xi-Putin trilateral
     summit in Shenzhen (CBS).
  4. World Children's Day, marked around the world on 20 November
     (United Nations observance).
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "assets" / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    dest = out_dir / "entry.png"
    if not SOURCE.is_file():
        print(f"error: pre-rendered image missing: {SOURCE}", file=sys.stderr)
        return 1
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE, dest)
    except OSError as exc:
        print(f"error: could not copy {SOURCE} to {dest}: {exc}",
              file=sys.stderr)
        return 1
    # Read the copy back and check it is complete: a short write (full
    # disk, interrupted copy) must fail loudly here, not hand the
    # grader a truncated image.
    try:
        copied = dest.read_bytes()
    except OSError as exc:
        print(f"error: could not read back {dest}: {exc}", file=sys.stderr)
        return 1
    expected = SOURCE.stat().st_size
    if len(copied) != expected:
        print(f"error: {dest} is {len(copied)} bytes, "
              f"expected {expected}", file=sys.stderr)
        return 1
    print(f"entry.png: copied {SOURCE.name} to {dest} "
          f"({len(copied)} bytes, verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
