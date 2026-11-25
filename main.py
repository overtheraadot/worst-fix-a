#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message.

Writes one commit-message line to /output/entry.txt. The joke: a
performance fix for slow search that "fixes" it by returning nothing
at all -- instantly. No trailing newline is written, so the file holds
exactly the line and nothing else.
"""

import os
import sys

ENTRY = "fix: search was too slow, so it now returns nothing instantly"

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 100


def validate(text: str) -> str:
    """Return the entry or raise ValueError if it fails the gate."""
    text = text.strip()
    if not text:
        raise ValueError("entry is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the 100 cap")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.encode("utf-8").decode("utf-8"):
        raise ValueError("entry is not valid UTF-8")
    return text


def main() -> int:
    try:
        text = validate(ENTRY)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Verify what actually landed on disk: exact bytes, char count,
    # single line, no trailing newline. A write that silently differs
    # from the validated text must fail loudly, not pass quietly.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    if written != text:
        print("error: file contents differ from validated entry",
              file=sys.stderr)
        return 1
    if len(written) > MAX_CHARS or "\n" in written:
        print("error: written file fails the gate", file=sys.stderr)
        return 1
    print(text)
    print(f"wrote {len(written)} chars ({len(raw)} bytes) to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
