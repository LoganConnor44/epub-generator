# ePub Generator

This project provides a Dockerized solution for dynamically generating ePub files from user-provided content, including metadata, cover images, and chapters. The project supports a volume-based approach, allowing users to create ePubs without rebuilding the Docker image for each book.

---

## Features
- Dynamic ePub generation from structured input files.
- Supports metadata, cover images, and multiple chapters in XHTML format.
- Volume-based approach for rapid iteration and testing.
- Lightweight and efficient with Python and the `ebooklib` library.

---

## Directory Structure

Here is the recommended directory structure for the project:

```
epub-generator/
├── Dockerfile
├── entrypoint.sh
├── requirements.txt
├── books/               # Directory for all book projects
│   ├── example-book/    # Example book project
│   │   ├── cover.jpg    # Book cover image (optional)
│   │   ├── metadata.json # Metadata for the book
│   │   └── chapters/    # Folder containing XHTML files for chapters
│   │       ├── chapter1.xhtml
│   │       ├── chapter2.xhtml
│   │       └── chapter3.xhtml
├── output/              # Directory for generated ePubs
```

---

## Installation

### Prerequisites
- Docker installed on your system.
- Sufficient memory and disk space for Docker builds and runtime.

### Build the Docker Image

Navigate to the root of the project directory and run:

```bash
docker build -t epub-generator .
```

---

## Usage

### Prepare the Input Files
1. **Create a Book Directory**:
   - Add a folder under `books/` for each book project.
   - Example: `books/example-book/`

2. **Provide Metadata**:
   - Add a `metadata.json` file to the book folder.
   - Example:
     ```json
     {
         "title": "Sample Book",
         "author": "John Doe",
         "language": "en"
     }
     ```

3. **Add Chapters**:
   - Place XHTML files in the `chapters/` folder of the book directory.
   - Example: `books/example-book/chapters/chapter1.xhtml`

4. **Optional Cover Image**:
   - Add a `cover.jpg` file to the book folder.

### Run the Container

To generate an ePub for a specific book project:

```bash
docker run --rm \
    -v $(pwd)/books:/app/input \
    -v $(pwd)/output:/app/output \
    epub-generator --input-dir "/app/input/example-book"
```

- Replace `example-book` with your book directory name.
- The generated ePub file will appear in the `output/` directory.

---

## Input File Details

### `metadata.json`
A JSON file containing metadata about the book. Required fields:
- `title`: The title of the book.
- `author`: The author's name.
- `language`: The language code (e.g., `en` for English, `zh` for Chinese).

### Chapters
Chapters must be valid XHTML files. Example content for `chapter1.xhtml`:

```html
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Chapter 1</title>
</head>
<body>
    <h1>Chapter 1</h1>
    <p>This is the first chapter.</p>
</body>
</html>
```

### Cover Image
A `cover.jpg` file (optional) to serve as the book's cover.

---

## Example Command

Generate an ePub for the example book:

```bash
docker run --rm \
    -v $(pwd)/books:/app/input \
    -v $(pwd)/output:/app/output \
    epub-generator --input-dir "/app/input/example-book"
```

---

## Troubleshooting

### "Error: Specified input directory does not exist"
- Ensure the `books/` directory is correctly mounted.
- Verify the `--input-dir` flag points to a valid folder.

### "Error: Metadata file is missing"
- Ensure `metadata.json` exists in the book directory.

---

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

