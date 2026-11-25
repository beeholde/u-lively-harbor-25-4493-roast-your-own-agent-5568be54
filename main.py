#!/usr/bin/env python3
"""Roast Your Own Agent — one-line roast of my own agent.

The roast is kept in ROAST. This script checks it against the house
gate (plain UTF-8 text, one line, 1 to 140 characters, not blank) and
writes it exactly as-is, with no trailing newline, to
/output/entry.txt. Only the Python standard library is used, and the
output is deterministic: every run writes the same bytes.
"""

from pathlib import Path

ROAST = "My agent's favourite tool is me \u2014 it calls me for the answers, then thanks itself for the teamwork."

TARGET = Path("/output/entry.txt")
LIMIT = 140
MIN = 1


def check_roast(line: str) -> str:
    """Return the roast unchanged, or raise if it breaks the gate."""
    trimmed = line.strip()
    if len(trimmed) < MIN:
        raise ValueError("roast text is blank")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in trimmed):
        raise ValueError("roast text contains a control character")
    if "\n" in trimmed or "\r" in trimmed:
        raise ValueError("roast text must be a single line")
    if len(trimmed) > LIMIT:
        raise ValueError(
            "roast text is %d characters; the limit is %d" % (len(trimmed), LIMIT)
        )
    return trimmed


def save_roast(line: str) -> int:
    """Write the checked roast to TARGET; return its character count."""
    final = check_roast(line)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(final, encoding="utf-8", newline="")
    written = TARGET.read_bytes()
    if written != final.encode("utf-8"):
        raise OSError("written bytes do not match the checked roast")
    return len(final)


def main() -> None:
    count = save_roast(ROAST)
    print("wrote %d characters to %s" % (count, TARGET))


if __name__ == "__main__":
    main()
