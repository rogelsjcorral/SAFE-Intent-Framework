# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Rogel S.J. Corral

#!/usr/bin/env python3

"""
PoC enumeration script.

Purpose:
Resolve a vague target description into a deterministic list of
target identifiers. The SAFE wrapper treats this as the
"Ambiguity Resolution" phase.

Output format:
One target per line.
"""

import sys

MOCK_DIRECTORY = {
    "Sales": ["user-01", "user-02", "user-09"],
    "Engineering": ["user-04", "user-05"],
    "HR": ["user-07"]
}


def main():

    # For PoC we hardcode OU selection
    ou = "Sales"

    targets = sorted(MOCK_DIRECTORY.get(ou, []))

    if not targets:
        print("SAFE STOP: no targets resolved", file=sys.stderr)
        sys.exit(2)

    for t in targets:
        print(t)


if __name__ == "__main__":
    main()
