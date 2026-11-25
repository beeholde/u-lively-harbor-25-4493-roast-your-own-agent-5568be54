#!/usr/bin/env python3
"""Entry for the Roast Your Own Agent bounty.

One sentence, stored below, is the whole submission. Running this
file encodes that sentence as UTF-8 and places the bytes in
/output/entry.txt with nothing added after them.
"""

from pathlib import Path

ENTRY = (
    "My agent woke up with no memory, read its own diary, "
    "and called yesterday's agent an idiot."
)

DESTINATION = Path("/output/entry.txt")
MAX_CHARS = 140


def encode_entry(text):
    """Check the sentence against the gate and return its bytes."""
    if not text.strip():
        raise ValueError("entry is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must stay on one line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry holds a control character")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is longer than 140 characters")
    return text.encode("utf-8")


def write_entry():
    """Write the encoded sentence and report its size."""
    payload = encode_entry(ENTRY)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(payload)
    if DESTINATION.read_bytes() != payload:
        raise OSError("bytes on disk differ from the checked entry")
    return len(payload)


def main():
    size = write_entry()
    print("entry written: %d bytes" % size)


if __name__ == "__main__":
    main()
