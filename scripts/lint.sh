#!/usr/bin/env bash

# Basic linting for SAFE reference implementation

echo "Running Python lint checks..."

if ! command -v flake8 &> /dev/null
then
    echo "flake8 not installed."
    echo "Install with: pip install flake8"
    exit 1
fi

flake8 poc/ tests/

echo ""
echo "Linting complete."
