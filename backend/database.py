import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Client
 
def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    return create_client(url, key)
 
# Customers 

def get_customer_by_email(email: str) -> dict | None:
    """Fetch a single customer row by email address."""
    db = get_client()
    response = (
        db.table("customers")
        .select("*")
        .eq("email", email)
        .maybe_single()
        .execute()
    )
    return response.data

def get_customer(customer_id: str) -> dict | None:
    """Fetch a single customer row by customer_id (e.g. CUST001)."""
    db = get_client()
    response = (
        db.table("customers")
        .select("*")
        .eq("customer_id", customer_id)
        .maybe_single()
        .execute()
    )
    return response.data

# Books
 
def get_book(book_id: str) -> dict | None:
    """Fetch a single book row by book_id (e.g. BOOK001)."""
    db = get_client()
    response = (
        db.table("books")
        .select("*")
        .eq("book_id", book_id)
        .maybe_single()
        .execute()
    )
    return response.data

def get_book_by_customer(customer_id: str) -> list[dict]:
    """Fetch all books belonging to a customer."""
    db = get_client()
    response = (
        db.table("books")
        .select("*")
        .eq("customer_id", customer_id)
        .execute()
    )
    return response.data or []
 
# Support Tickets

def get_open_ticket(customer_id: str) -> dict | None:
    """Fetch the most recent Open or In-Progress ticket for a customer."""
    db = get_client()
    response = (
        db.table("support_tickets")
        .select("*")
        .eq("customer_id", customer_id)
        .in_("status", ["Open", "In Progress"])
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    data = response.data
    return data[0] if data else None

def _next_ticket_id() -> str:
    """Generate the next sequential ticket ID (e.g. TKT006)."""
    db = get_client()
    response = (
        db.table("support_tickets")
        .select("ticket_id")
        .order("ticket_id", desc=True)
        .limit(1)
        .execute()
    )
    if not response.data:
        return "TKT001"
    last_id: str = response.data[0]["ticket_id"]          # e.g. "TKT005"
    next_number = int(last_id.replace("TKT", "")) + 1
    return f"TKT{next_number:03d}"

def create_ticket(customer_id: str, issue: str) -> dict:
    """Insert a new Open support ticket and return the created row."""
    db = get_client()
    ticket = {
        "ticket_id":   _next_ticket_id(),
        "customer_id": customer_id,
        "issue":       issue,
        "status":      "Open",
    }
    response = (
        db.table("support_tickets")
        .insert(ticket)
        .execute()
    )
    return response.data[0]

# Conversation History
 
def save_conversation(
    customer_id: str,
    question:    str,
    answer:      str,
    confidence:  float,
) -> dict:
    """Persist a single Q&A exchange to conversation_history."""
    db = get_client()
    record = {
        "customer_id": customer_id,
        "question":    question,
        "answer":      answer,
        "confidence":  round(confidence, 3),
    }
    response = (
        db.table("conversation_history")
        .insert(record)
        .execute()
    )
    return response.data[0]

def get_recent_conversations(customer_id: str, limit: int = 5) -> list[dict]:
    """Fetch the most recent conversation turns for a customer."""
    db = get_client()
    response = (
        db.table("conversation_history")
        .select("question, answer, confidence, created_at")
        .eq("customer_id", customer_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []