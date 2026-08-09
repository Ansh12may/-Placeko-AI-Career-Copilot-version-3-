"""
Resume Parser Tool

Responsible for:
- Extracting raw text from PDF and DOCX resumes
- Performing basic text cleaning

This module performs NO:
- Semantic analysis
- Information extraction
- LLM reasoning
- ATS scoring
"""

import re
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


# =========================================================
# Text Cleaning
# =========================================================

def clean_text(text: str) -> str:
    """
    Normalize extracted resume text.
    """

    text = text.replace(
        "\r",
        "\n",
    )

    text = re.sub(
        r"\n+",
        "\n",
        text,
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    return text.strip()


# =========================================================
# PDF Extraction
# =========================================================

def extract_text_from_pdf(
    file_path: Path,
) -> str:
    """
    Extract text from a PDF using PyMuPDF.
    """

    with fitz.open(file_path) as document:

        pages: list[str] = []

        for page in document:
            pages.append(
                page.get_text()
            )

    return "\n".join(pages)


# =========================================================
# DOCX Extraction
# =========================================================

def extract_text_from_docx(
    file_path: Path,
) -> str:
    """
    Extract text from a DOCX file.
    """

    document = Document(
        file_path
    )

    paragraphs: list[str] = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(
        paragraphs
    )


# =========================================================
# Main Parser
# =========================================================

def parse_resume(
    file_path: str | Path,
) -> str:
    """
    Parse a resume file and return
    cleaned text.

    Supported formats:
    - PDF
    - DOCX
    """

    path = Path(file_path)

    # -----------------------------------------------------
    # Validate file existence
    # -----------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"Resume not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Resume path is not a file: {path}"
        )

    # -----------------------------------------------------
    # Determine file type
    # -----------------------------------------------------

    suffix = path.suffix.lower()

    # -----------------------------------------------------
    # Extract text
    # -----------------------------------------------------

    if suffix == ".pdf":

        raw_text = extract_text_from_pdf(
            path
        )

    elif suffix == ".docx":

        raw_text = extract_text_from_docx(
            path
        )

    else:

        raise ValueError(
            f"Unsupported file format: {suffix}. "
            "Only PDF and DOCX are supported."
        )

    # -----------------------------------------------------
    # Clean text
    # -----------------------------------------------------

    cleaned_text = clean_text(
        raw_text
    )

    # -----------------------------------------------------
    # Validate extraction
    # -----------------------------------------------------

    if not cleaned_text:
        raise ValueError(
            "Could not extract any text from the resume."
        )

    return cleaned_text