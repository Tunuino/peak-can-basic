#!/usr/bin/env python3
"""Reject legacy branding in tracked text files."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
forbidden = b"ruse" + b"fi"
files = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).split(b"\0")
violations = []
checked = 0
for item in files:
    if not item:
        continue
    relative = item.decode("utf-8", "surrogateescape")
    path = root / relative
    if not path.is_file() or path.is_symlink():
        continue
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        continue
    checked += 1
    if forbidden in data.lower():
        violations.append(relative)
print(f"Checked {checked} tracked text files")
if violations:
    print("Legacy branding:", *violations, sep="\n")
    sys.exit(1)
print("Branding check passed")
