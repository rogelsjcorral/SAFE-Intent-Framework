#!/usr/bin/env bash

# Format Python code for SAFE reference implementation

echo "Formatting code with black..."

if ! command -v black &> /dev/null
then
    echo "black not installed."
    echo "Install with: pip install black"
    exit 1
fi

black poc/ tests/

echo ""
echo "Formatting complete."
