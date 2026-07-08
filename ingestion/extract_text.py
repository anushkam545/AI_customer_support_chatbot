"""
extract_text.py

Read all PDFs from the knowledge_base folder.
Merge pages belonging to the same PDF while preserving page locations.
Extract URLs from the document.
"""
import re
from pathlib import Path
import fitz

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"

URL_PATTERN = re.compile(r"https?://[^\s\)\]\>\",]+")

def extract_urls(text: str) -> list[str]:
    """Extract unique URLs while preserving order."""
    return list(dict.fromkeys(URL_PATTERN.findall(text)))

def extract_all_pdfs() -> list[dict]:
    """
    Read every PDF from knowledge_base/.

    Returns:
    [
        {
            "source_file": "...",
            "text": "...",
            "page_map": [
                {"page":1,"start":0},
                {"page":2,"start":1850},
                ...
            ],
            "urls":[...]
        }
    ]
    """

    pdf_files = sorted(KNOWLEDGE_BASE_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {KNOWLEDGE_BASE_DIR}"
        )
    documents = []
    for pdf_path in pdf_files:
        print(f"Reading: {pdf_path.name}")
        document = fitz.open(pdf_path)
        full_text = ""
        page_map = []
        all_urls = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text().strip()
            if not text:
                continue
            page_map.append({
                "page": page_number,
                "start": len(full_text)
            })

            full_text += text + "\n\n"
            all_urls.extend(extract_urls(text))

        document.close()

        documents.append({
            "source_file": pdf_path.name,
            "text": full_text.strip(),
            "page_map": page_map,
            "urls": list(dict.fromkeys(all_urls))
        })

    print(f"\nProcessed {len(documents)} PDF(s)")

    return documents