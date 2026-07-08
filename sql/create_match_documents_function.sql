-- RPC function for semantic search over knowledge_chunks.
-- Run this once in the Supabase SQL editor.

CREATE OR REPLACE FUNCTION match_knowledge_chunks(
    query_embedding vector(384),
    match_count     int DEFAULT 5
)
RETURNS TABLE (
    source_file text,
    page_number int,
    question    text,
    content     text,
    urls        text[],
    similarity  float
)
LANGUAGE sql STABLE
AS $$
    SELECT
        source_file,
        page_number,
        question,
        content,
        urls,
        1 - (embedding <=> query_embedding) AS similarity
    FROM knowledge_chunks
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;
