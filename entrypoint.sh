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

# Read metadata
METADATA=$(cat "$INPUT_DIR/metadata.json")
TITLE=$(echo "$METADATA" | jq -r '.title')
AUTHOR=$(echo "$METADATA" | jq -r '.author')
LANGUAGE=$(echo "$METADATA" | jq -r '.language')

# Prepare output directory
OUTPUT_DIR="/app/output"
mkdir -p "$OUTPUT_DIR"

# Generate ePub
python3 <<EOF
from ebooklib import epub
import os

# Metadata
title = "$TITLE"
author = "$AUTHOR"
language = "$LANGUAGE"

# Create book
book = epub.EpubBook()
book.set_identifier("id123456")
book.set_title(title)
book.set_language(language)
book.add_author(author)

# Add chapters
chapter_dir = os.path.join("$INPUT_DIR", "chapters")
for chapter_file in sorted(os.listdir(chapter_dir)):
    if chapter_file.endswith(".xhtml"):
        with open(os.path.join(chapter_dir, chapter_file), "r", encoding="utf-8") as f:
            content = f.read()
        chapter = epub.EpubHtml(
            title=chapter_file.replace(".xhtml", ""),
            file_name=chapter_file,
            lang=language
        )
        chapter.content = content
        book.add_item(chapter)
        book.spine.append(chapter)

# Add cover
cover_path = os.path.join("$INPUT_DIR", "cover.jpg")
if os.path.exists(cover_path):
    with open(cover_path, "rb") as cover_file:
        book.set_cover("cover.jpg", cover_file.read())

# Add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Write to file
output_path = os.path.join("$OUTPUT_DIR", f"{title}.epub")
epub.write_epub(output_path, book, {})
print(f"ePub file created: {output_path}")
EOF
