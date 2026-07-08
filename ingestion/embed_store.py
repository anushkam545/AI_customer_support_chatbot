"""
embed_store.py

Generate embeddings and store chunks in Supabase pgvector.
Run this SQL once in Supabase before using:

    create extension if not exists vector;

    create table knowledge_chunks (
        id            bigserial primary key,
        source_file   text,
        page_number   int,
        question      text,
        content       text,
        urls          text[],
        embedding     vector(384),
        created_at    timestamptz default now()
    );
"""
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
TABLE = "knowledge_chunks"
BATCH_SIZE = 50

def embed_and_store(chunks):
    """Embed all chunks and insert them into Supabase."""
    if not chunks:
        print("No chunks to store.")
        return

    # Load model
    print("Loading embedding model...")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    # Generate embeddings
    print(f"Embedding {len(chunks)} chunks...")
    texts = [c["content"] for c in chunks]
    embeddings = model.encode(texts, batch_size=32, normalize_embeddings=True, show_progress_bar=True)

    print("URL:", SUPABASE_URL)
    print("KEY EXISTS:", SUPABASE_KEY is not None)
    print("KEY PREFIX:", SUPABASE_KEY[:20] if SUPABASE_KEY else None)

    # Connect to Supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Insert in batches
    total = len(chunks)
    for i in range(0, total, BATCH_SIZE):
        batch_chunks = chunks[i: i + BATCH_SIZE]
        batch_embeddings = embeddings[i: i + BATCH_SIZE]

        records = [
            {
                "source_file": chunk["source_file"],
                "page_number": chunk["page_number"],
                "question": chunk["question"],
                "content": chunk["content"],
                "urls": chunk["urls"],
                "embedding": embedding.tolist(),
            }
            for chunk, embedding in zip(batch_chunks, batch_embeddings)
        ]
        
        supabase.table(TABLE).insert(records).execute()
        print(f"Inserted {min(i + BATCH_SIZE, total)}/{total}")

    print("Done.")