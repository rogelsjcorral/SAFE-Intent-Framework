# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Rogel S.J. Corral

#!/usr/bin/env python3

"""
PoC execution script.

Purpose:
Simulate applying a change to targets.
"""

import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--targets-file", required=True)
    args = parser.parse_args()

    with open(args.targets_file) as f:
        targets = [line.strip() for line in f if line.strip()]

    for t in targets:
        print(f"Applied change to {t}")


if __name__ == "__main__":
    main()
