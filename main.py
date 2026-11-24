"""Copy our one-line entry to the make.fun output directory.

The entry lives in entry.txt next to this script: a single original
sentence, 1-200 UTF-8 characters, no trailing newline. This script
reads it, checks it against the sealed gate, and copies it byte for
byte to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then verifies
the copy with SHA-256 so a truncated or mangled write is caught here
instead of failing on the grader. Stdlib only — the grading image has
no third-party packages installed.
"""

import hashlib
import os
import sys


MAX_CHARS = 200


def fail(message):
    """Print an error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def load_entry(path):
    """Read entry.txt as bytes and return (data, decoded text)."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail(f"cannot read {path}: {exc}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        fail("entry.txt is not valid UTF-8")
    return data, text


def validate(text):
    """Enforce the sealed gate: exactly one line, 1-200 chars."""
    if "\n" in text or "\r" in text:
        fail("entry.txt must hold exactly one line (no newline)")
    if not text.strip():
        fail("entry.txt must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        fail(
            f"entry is {len(text)} chars, but the sealed limit is {MAX_CHARS}"
        )
    # One visible line, nothing hidden after it.
    if text != text.strip():
        fail("entry.txt must not have leading or trailing spaces")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "entry.txt")
    data, text = load_entry(src_path)
    validate(text)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output dir {out_dir}: {exc}")

    out_path = os.path.join(out_dir, "entry.txt")
    try:
        with open(out_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail(f"cannot write {out_path}: {exc}")

    # Re-read the copy and prove it is byte-identical to the source.
    with open(out_path, "rb") as handle:
        written = handle.read()
    source_hash = hashlib.sha256(data).hexdigest()
    written_hash = hashlib.sha256(written).hexdigest()
    if written_hash != source_hash:
        fail("output differs from entry.txt (sha256 mismatch)")

    print(f"wrote {len(data)} bytes, {len(text)} chars -> {out_path}")
    print(f"sha256: {source_hash}")


if __name__ == "__main__":
    main()
