#!/bin/bash

set -e

# Default input directory
INPUT_DIR="/app/input"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input-dir) INPUT_DIR="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Validate input directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: Specified input directory '$INPUT_DIR' does not exist."
    exit 1
fi

# Validate metadata file
if [ ! -f "$INPUT_DIR/metadata.json" ]; then
    echo "Error: Metadata file '$INPUT_DIR/metadata.json' is missing."
    exit 1
fi

# Prepare output directory
OUTPUT_DIR="/app/output"
mkdir -p "$OUTPUT_DIR"

# Call Python script to generate ePub
python3 /app/generate.py --input-dir "$INPUT_DIR" --output-dir "$OUTPUT_DIR"
