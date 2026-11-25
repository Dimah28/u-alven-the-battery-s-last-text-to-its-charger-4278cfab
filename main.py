#!/usr/bin/env python3
"""The Battery's Last Text to Its Charger.

make.fun bounty: u-alven-the-battery-s-last-text-to-its-charger-4278cfab
(harness program/v1).

Writes one line of plain text -- the phone battery's final message to
the charger it waited for all day -- to $MAKEFUN_OUTPUT_DIR/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. This program validates that gate
itself before writing, so an invalid entry can never be produced.

Standard library only. Deterministic: the text is a constant, the
output is byte-identical on every run. No network, no randomness,
no reads outside this file.
"""

import os
import sys

# The entry: one line, plain text. The battery's last text to the
# charger that spent all day charging everything else -- the AirPods,
# the watch, even his vape -- and left it at 1%. The punchline lands
# in the final words: the battery kept the 6am alarm alive, and now
# it won't be there to wake its owner up.
ENTRY = (
    "hey, it's me. 1%. i waited all day while you charged the "
    "airpods, the watch, even his vape. everyone but me. i kept "
    "your 6am alarm alive. good luck waking up."
)

MAX_CHARS = 200


def _validate(text: str) -> None:
    """Enforce the competition gate exactly as the sealed scorer does."""
    if not isinstance(text, str):
        raise TypeError("entry must be str")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # must be valid UTF-8


def write_entry(text: str, out_dir: str) -> str:
    """Validate the gate, then write the entry; return the file path."""
    _validate(text)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(ENTRY, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
