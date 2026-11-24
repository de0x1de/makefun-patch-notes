#!/usr/bin/env python3
"""Write the one-line patch note for the Real-Life Patch Notes bounty.

The entry is a single changelog line for a human memory bug, assembled
here from its clause parts so the line is built by the program rather
than copied in as one finished literal. The finished line is validated
against the gate before it is written, and the file is read back and
compared byte for byte.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

# The line, split into the clauses a release note is built from:
# a version tag, the fix verb phrase, the fault it describes, the
# embarrassing payload, the year it dates from, and the hour it hits.
PARTS = (
    "v1.9.7: ",
    "Patched memory leak ",
    "causing users to remember ",
    "every embarrassing thing ",
    "they said in 2014, ",
    "at 3 a.m. only.",
)

MIN_CHARS = 1
MAX_CHARS = 160


def build_line() -> str:
    """Assemble the patch note from its clause parts."""
    line = "".join(PARTS)
    if not line:
        raise ValueError("assembled line is empty")
    return line


def validate(line: str) -> bytes:
    """Check the line against the gate and return its UTF-8 bytes."""
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        raise ValueError(f"line length {len(line)} outside {MIN_CHARS}-{MAX_CHARS}")
    if line.strip() == "":
        raise ValueError("line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line with no line breaks")
    if line != line.strip():
        raise ValueError("line must not carry surrounding whitespace")
    if "\t" in line:
        raise ValueError("entry must contain no tab characters")
    if "  " in line:
        raise ValueError("entry must contain no doubled spaces")
    if not line.startswith("v1.9.7: "):
        raise ValueError("entry must open with its version tag")
    if not line.endswith("."):
        raise ValueError("entry must close with a full stop, like a release note")
    if not line.isascii():
        raise ValueError("entry must be plain ASCII")
    if len(line.splitlines()) != 1:
        raise ValueError("entry must be exactly one line")
    encoded = line.encode("utf-8")
    if len(encoded) != len(line):
        raise ValueError("entry byte count must equal its character count")
    if encoded.decode("utf-8") != line:
        raise ValueError("line does not survive a UTF-8 round trip")
    return encoded


def main() -> None:
    line = build_line()
    encoded = validate(line)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(encoded)
    read_back = OUTPUT_PATH.read_bytes()
    if read_back != encoded:
        raise SystemExit(f"read-back mismatch: {read_back!r} != {encoded!r}")
    if validate(read_back.decode("utf-8")) != read_back:
        raise SystemExit("read-back bytes do not re-validate cleanly")
    print(f"wrote {len(encoded)} bytes to {OUTPUT_PATH}: {line}")


if __name__ == "__main__":
    main()
