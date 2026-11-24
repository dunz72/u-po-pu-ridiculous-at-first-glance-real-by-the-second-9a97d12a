"""Ridiculous at First Glance, Real by the Second entry.

Copies the single original line from entry.txt (next to this file) to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt when the variable
is not set), byte for byte. The line is 1-200 characters, UTF-8, not
only whitespace, as the sealed gate requires. Stdlib only.
"""

import hashlib
import os
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.txt")
    with open(src_path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")
    stripped = text.strip()
    if not 1 <= len(stripped) <= 200:
        raise ValueError(
            f"entry must be 1-200 characters, got {len(stripped)}"
        )
    if not stripped:
        raise ValueError("entry must not be only whitespace")
    if text != stripped:
        raise ValueError("entry.txt must hold exactly one line")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(data)
    with open(out_path, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        raise ValueError("output is not byte-identical to entry.txt")
    print(f"wrote {len(data)} bytes ({len(text)} chars) to {out_path}")


if __name__ == "__main__":
    main()
