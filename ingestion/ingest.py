from extract_text import extract_all_pdfs
from chunk_text import chunk_documents
from embed_store import embed_and_store

documents = extract_all_pdfs()

chunks = chunk_documents(documents)

embed_and_store(chunks)

print("Knowledge base successfully ingested.")