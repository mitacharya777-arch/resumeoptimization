"""
Utility functions for parsing different file formats.
"""

from typing import Optional

# Try to import optional dependencies
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False


def parse_pdf(file_path: str) -> Optional[str]:
    """Extract text from PDF file."""
    if not PDFPLUMBER_AVAILABLE:
        raise ImportError("pdfplumber is not installed. Install it with: pip install pdfplumber")
    
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None


def parse_docx(file_path: str) -> Optional[str]:
    """Extract text from DOCX file."""
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx is not installed. Install it with: pip install python-docx")
    
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return None


def parse_text_file(file_path: str) -> Optional[str]:
    """Extract text from plain text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error parsing text file: {e}")
        return None


def parse_resume(file_path: str) -> Optional[str]:
    """Parse resume from various file formats."""
    file_path_lower = file_path.lower()
    
    if file_path_lower.endswith('.pdf'):
        return parse_pdf(file_path)
    elif file_path_lower.endswith('.docx') or file_path_lower.endswith('.doc'):
        return parse_docx(file_path)
    elif file_path_lower.endswith('.txt'):
        return parse_text_file(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return None

