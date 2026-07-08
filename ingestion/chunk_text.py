"""
chunk_text.py

Split documents into FAQ-based chunks.
Falls back to overlapping chunks for long sections.
"""
import re

MAX_CHUNK_CHARS = 1200
OVERLAP_CHARS = 150

URL_PATTERN = re.compile(r"https?://[^\s\)\]\>\",]+")

def extract_urls(text: str) -> list[str]:
    """Extract URLs from a chunk."""
    return list(dict.fromkeys(URL_PATTERN.findall(text)))

def detect_question(text: str):
    """Return the first question found in a chunk."""

    for line in text.splitlines():
        line = line.strip()
        if line.endswith("?"):
            return line

    return None

def split_on_headings(text: str):
    """
    Split a document into FAQ sections.
    """
    lines = text.splitlines()

    sections = []
    current_section = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith("?") and current_section:
            sections.append("\n".join(current_section))
            current_section = [line]
        else:
            current_section.append(line)
    if current_section:
        sections.append("\n".join(current_section))

    return sections


def split_large_section(text: str):
    """
    Split a large section into overlapping chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + MAX_CHUNK_CHARS
        if end >= len(text):
            chunks.append(text[start:].strip())
            break
        split_at = text.rfind("\n", start, end)
        if split_at == -1:
            split_at = text.rfind(". ", start, end)
        if split_at == -1:
            split_at = end

        chunks.append(text[start:split_at].strip())
        start = split_at - OVERLAP_CHARS
        if start < 0:
            start = 0

    return chunks

def get_page_number(chunk_start: int, page_map: list):
    """
    Find the page where a chunk begins.
    """
    page = 1
    for item in page_map:
        if chunk_start >= item["start"]:
            page = item["page"]
        else:
            break

    return page

def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Convert extracted documents into semantic chunks.
    """
    chunks = []
    for document in documents:
        sections = split_on_headings(document["text"])
        for section in sections:
            if len(section) <= MAX_CHUNK_CHARS:
                section_chunks = [section]
            else:
                section_chunks = split_large_section(section)
            for chunk in section_chunks:

                chunk_start = document["text"].find(chunk)
                chunks.append({

                    "source_file": document["source_file"],
                    "page_number": get_page_number(
                        chunk_start,
                        document["page_map"]
                    ),

                    "question": detect_question(chunk),
                    "content": chunk,
                    "urls": extract_urls(chunk)
                })

    print(f"Total chunks created: {len(chunks)}")
    return chunks