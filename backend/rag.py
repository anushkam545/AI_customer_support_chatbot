import os
from dotenv import load_dotenv
from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

load_dotenv()

# Model loaded once, reused across calls
_model: SentenceTransformer | None = None

def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
        _model = SentenceTransformer(model_name)
    return _model

def _get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    return create_client(url, key)

def generate_embedding(text: str) -> list[float]:
    """Encode text into a 384-dim vector using BAAI/bge-small-en-v1.5."""
    return _get_model().encode(text, normalize_embeddings=True).tolist()

def search_knowledge_base(user_question: str, top_k: int = 5) -> list[dict]:
    """
    Embed user_question and return the top_k most relevant chunks
    from knowledge_chunks via the match_knowledge_chunks RPC function.

    Requires sql/04_create_match_documents_function.sql to be run once
    in the Supabase SQL editor before use.
    """
    embedding = generate_embedding(user_question)

    response = _get_client().rpc(
        "match_knowledge_chunks",
        {
            "query_embedding": embedding,
            "match_count":     top_k,
        },
    ).execute()

    return [
        {
            "source_file": row["source_file"],
            "page_number": row["page_number"],
            "question":    row["question"],
            "content":     row["content"],
            "urls":        row["urls"] or [],
            "similarity":  round(float(row["similarity"]), 4),
        }
        for row in (response.data or [])
    ]