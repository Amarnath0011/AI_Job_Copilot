from pathlib import Path
from typing import BinaryIO

from pypdf import PdfReader


def extract_text_from_pdf(file_source: str | Path | BinaryIO) -> str:
    """Extract readable text from a PDF path or binary file-like object."""
    reader = PdfReader(file_source)
    pages = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)
    return "\n".join(pages)
