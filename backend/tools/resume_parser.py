"""
Resume Parser Tool
Responsible for extracting raw text from resume files
(PDF and DOCX).
This module performs only text extraction and basic
cleaning. It does not perform semantic analysis,
information extraction, or LLM reasoning.
"""

import re
from pathlib import Path
import fitz  # PyMuPDF
from docx import Document


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_text_from_pdf(file_path: Path) -> str:
    
    with fitz.open(file_path) as document:
        pages: list[str] = []

        for page in document:
            pages.append(page.get_text())

    return "\n".join(pages)


def extract_text_from_docx(file_path: Path) -> str:
    
    document = Document(file_path)

    paragraphs: list[str] = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def parse_resume(file_path: str | Path) -> str:
    """
    Parse a resume file and return cleaned text.
    Supports PDF and DOCX formats.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        raw_text = extract_text_from_pdf(path)
    elif suffix == ".docx":
        raw_text = extract_text_from_docx(path)
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Only PDF and DOCX are supported."
        )

    return clean_text(raw_text)


# Resume File
#      │
#      ▼
# parse_resume()
#      │
#      ├──────────────┐
#      ▼              ▼
# PDF              DOCX
#      │              │
#      ▼              ▼
# extract_text   extract_text
#      │              │
#      └──────┬───────┘
#             ▼
#       clean_text()
#             ▼
#      Clean Resume Text

