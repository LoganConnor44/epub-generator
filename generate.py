import os
import argparse
from ebooklib import epub
from lxml import etree, html

def clean_xhtml(content):
    """Clean and reformat XHTML content."""
    # Remove XML declaration if present
    if content.startswith('<?xml'):
        content = content.split('?>', 1)[-1].strip()

    # Parse and reformat content
    parser = html.HTMLParser(recover=True)
    tree = html.document_fromstring(content, parser=parser)
    return etree.tostring(tree, pretty_print=True, encoding="unicode")

def validate_xhtml(content, chapter_file):
    """Validate XHTML content."""
    try:
        parser = etree.XMLParser(recover=True)
        etree.fromstring(content.encode("utf-8"), parser=parser)
        print(f"{chapter_file} is valid XHTML.")
    except etree.XMLSyntaxError as e:
        print(f"Error in {chapter_file}: {e}")
        raise ValueError(f"Invalid XHTML in {chapter_file}")

def extract_title_from_xhtml(content, chapter_file):
    """Extract the <title> tag content from an XHTML file."""
    try:
        tree = etree.fromstring(content.encode("utf-8"))
        # Find the <title> element within the XHTML namespace
        title_element = tree.find(".//{http://www.w3.org/1999/xhtml}title")
        if title_element is not None and title_element.text:
            return title_element.text.strip()
        else:
            print(f"Warning: No <title> tag found in {chapter_file}, using 'Untitled'.")
            return "Untitled"
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XHTML for {chapter_file}: {e}")
        return "Untitled"

def main(input_dir, output_dir):
    # Read metadata
    metadata_file = os.path.join(input_dir, "metadata.json")
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = eval(f.read())  # You can replace eval with json.load for stricter parsing.
    
    title = metadata.get("title", "Untitled")
    author = metadata.get("author", "Unknown Author")
    language = metadata.get("language", "en")

    # Create ePub book
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)

    # Process chapters
    chapter_dir = os.path.join(input_dir, "chapters")
    if not os.path.exists(chapter_dir):
        raise FileNotFoundError(f"Chapters directory not found: {chapter_dir}")
    
    print(f"Adding chapters from: {chapter_dir}")

    toc = []  # To store chapters for the table of contents
    for chapter_file in sorted(os.listdir(chapter_dir)):
        chapter_path = os.path.join(chapter_dir, chapter_file)
        with open(chapter_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Validate and clean content
        validate_xhtml(content, chapter_file)
        cleaned_content = clean_xhtml(content)
        if not cleaned_content.strip():
            raise ValueError(f"Cleaned content for {chapter_file} is empty.")

        # Extract chapter title from the <title> tag
        chapter_title = extract_title_from_xhtml(cleaned_content, chapter_file)

        # Add chapter to the book
        chapter = epub.EpubHtml(
            title=chapter_title,
            file_name=chapter_file,
            lang=language
        )
        chapter.content = cleaned_content
        book.add_item(chapter)
        book.spine.append(chapter)  # Add chapter to the spine

        # Add chapter to ToC
        toc.append(chapter)
        print(f"Added chapter: {chapter_file} as '{chapter_title}' to the book")

    # Add table of contents
    book.toc = tuple(toc)  # Convert the list of chapters into a tuple for ToC

    # Add cover
    cover_path = os.path.join(input_dir, "cover.jpg")
    if os.path.exists(cover_path):
        with open(cover_path, "rb") as f:
            book.set_cover("cover.jpg", f.read())
        print("Cover added to the book.")
    else:
        print("No cover found. Skipping.")

    # Add navigation files
    book.add_item(epub.EpubNcx())  # Add NCX navigation
    book.add_item(epub.EpubNav())  # Add navigation view

    # Write the ePub
    output_path = os.path.join(output_dir, f"{title}.epub")
    epub.write_epub(output_path, book, {})
    print(f"ePub file created: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an ePub from XHTML files.")
    parser.add_argument("--input-dir", required=True, help="Input directory containing book metadata and chapters.")
    parser.add_argument("--output-dir", required=True, help="Output directory for the generated ePub file.")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
