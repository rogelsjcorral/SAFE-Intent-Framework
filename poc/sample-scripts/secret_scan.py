# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Rogel S.J. Corral

#!/usr/bin/env python3

"""
PoC secret scanner.

Purpose:
Scan logs for common credential patterns to detect
accidental leakage into evidence artifacts.
"""

import argparse
import re
from pathlib import Path

PATTERNS = {
    "AWS_KEY": r"AKIA[0-9A-Z]{16}",
    "PRIVATE_KEY": r"-----BEGIN .*PRIVATE KEY-----",
    "TOKEN": r"(api[_-]?key|token|password)\s*[:=]"
}


def scan_file(path):

    text = path.read_text(errors="ignore")

    hits = []

    for name, regex in PATTERNS.items():
        if re.search(regex, text):
            hits.append(name)

    return hits


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True)
    args = parser.parse_args()

    directory = Path(args.dir)

    for file in directory.rglob("*"):
        if file.is_file():

            hits = scan_file(file)

            if hits:
                print(f"Secret pattern detected in {file}: {hits}")
                return 1

    print("No secret patterns detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
