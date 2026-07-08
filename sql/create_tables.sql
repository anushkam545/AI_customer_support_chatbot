-- ============================================================
-- Bookleaf Publishing — Database Schema
-- ============================================================

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id     VARCHAR(20)  PRIMARY KEY,          -- e.g. CUST001
    customer_name   VARCHAR(100) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    phone           VARCHAR(20),
    country         VARCHAR(60),
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Books
CREATE TABLE IF NOT EXISTS books (
    book_id                 VARCHAR(20)  PRIMARY KEY,  -- e.g. BOOK001
    customer_id             VARCHAR(20)  NOT NULL REFERENCES customers(customer_id),
    book_title              VARCHAR(255) NOT NULL,
    final_submission_date   DATE,
    book_live_date          DATE,
    royalty_status          VARCHAR(30)  NOT NULL DEFAULT 'Pending',
    -- Possible values: Pending | Processing | Paid | On Hold
    isbn                    VARCHAR(20)  UNIQUE,
    add_on_services         TEXT,
    -- Comma-separated: e.g. 'Editing, Cover Design, Marketing Package'
    manuscript_status       VARCHAR(40)  NOT NULL DEFAULT 'Under Review',
    -- Possible values: Under Review | Revision Requested | Approved | Final Approved
    current_stage           VARCHAR(50)  NOT NULL DEFAULT 'Manuscript Received'
    -- Possible values: Manuscript Received | Editing | Proofreading |
    --                  Cover Design | ISBN Assignment | Pre-Publishing Review | Live
);

-- Support Tickets
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id   VARCHAR(20)  PRIMARY KEY,              -- e.g. TKT001
    customer_id VARCHAR(20)  NOT NULL REFERENCES customers(customer_id),
    issue       TEXT         NOT NULL,
    status      VARCHAR(20)  NOT NULL DEFAULT 'Open',
    -- Possible values: Open | In Progress | Resolved | Closed
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Conversation History (AI chat logs)
CREATE TABLE IF NOT EXISTS conversation_history (
    conversation_id UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id     VARCHAR(20)  REFERENCES customers(customer_id),
    question        TEXT         NOT NULL,
    answer          TEXT         NOT NULL,
    confidence      NUMERIC(4,3),                      -- e.g. 0.923
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Documents (Knowledge Base for RAG)
CREATE TABLE IF NOT EXISTS documents (
    document_id UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    title       VARCHAR(255) NOT NULL,
    content     TEXT         NOT NULL,
    embedding   vector(384)            -- BAAI/bge-small-en-v1.5 → 384 dims
);

-- Index for fast cosine similarity search on document embeddings
CREATE INDEX IF NOT EXISTS idx_documents_embedding
    ON documents USING hnsw (embedding vector_cosine_ops);
