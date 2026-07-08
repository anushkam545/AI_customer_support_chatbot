import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

MAX_RETRIES = 3

def _call_with_retry(model, prompt, config):
    """Call Gemini, retrying on transient 429s with backoff."""
    for attempt in range(MAX_RETRIES):
        try:
            return model.generate_content(prompt, generation_config=config)
        except ResourceExhausted as e:
            if attempt == MAX_RETRIES - 1:
                raise
            wait = getattr(e, "retry_delay", None)
            wait = wait.seconds if wait else 2 ** attempt  # fallback backoff
            time.sleep(wait + 1)

# Prompts
 
KNOWLEDGE_BASE_PROMPT = """\
You are a helpful customer support assistant for Bookleaf Publishing.
Answer the customer's question using ONLY the document context provided below.
If the context does not contain enough information to answer the question,
respond with: "I'm sorry, I don't have that information available. Please
contact our support team for further assistance."
Do not make up information. Do not reference sources outside the context.

--- DOCUMENT CONTEXT ---
{context}
--- END CONTEXT ---

Customer question: {question}
"""

CUSTOMER_DATABASE_PROMPT = """\
You are a helpful customer support assistant for Bookleaf Publishing.
Answer the customer's question using ONLY the customer information provided below.
If the information needed to answer the question is not present,
respond with: "I'm sorry, I couldn't find that information on your account.
Please contact our support team for further assistance."
Do not make up information. Do not reference data outside what is provided.

--- CUSTOMER INFORMATION ---
{data}
--- END CUSTOMER INFORMATION ---

Customer question: {question}
"""

# Helpers
 
def _format_chunks(retrieved_context: list[dict]) -> str:
    """Format RAG chunks into a readable context block."""
    if not retrieved_context:
        return "No relevant documents found."

    parts = []
    for i, chunk in enumerate(retrieved_context, start=1):
        part = f"[{i}] {chunk.get('title') or chunk.get('question') or 'Document'}\n"
        part += chunk.get("content", "")
        if chunk.get("source_file"):
            part += f"\n(Source: {chunk['source_file']}, Page {chunk.get('page_number', '?')})"
        parts.append(part)

    return "\n\n".join(parts)

def _format_database_result(database_result) -> str:
    """Format structured Supabase data into a readable block."""
    if not database_result:
        return "No customer data found."
    return json.dumps(database_result, indent=2, default=str)

 
# Main function

def generate_response(
    user_question:    str,
    intent:           str,
    retrieved_context: list[dict] | None = None,
    database_result:  dict | list | None = None,
) -> str:
    """
    Generate a support response using Gemini 2.5 Flash.

    - intent == 'knowledge_base'    → answer from retrieved document chunks
    - intent == 'customer_database' → answer from structured Supabase data
    """
    api_key    = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)

    if intent == "knowledge_base":
        context = _format_chunks(retrieved_context or [])
        prompt  = KNOWLEDGE_BASE_PROMPT.format(
            context=context,
            question=user_question,
        )
    else:  # customer_database
        data   = _format_database_result(database_result)
        prompt = CUSTOMER_DATABASE_PROMPT.format(
            data=data,
            question=user_question,
        )

    config = genai.GenerationConfig(
        temperature=0.2,     # slight flexibility for natural phrasing
        max_output_tokens=512,
    )

    try:
        response = _call_with_retry(model, prompt, config)
    except ResourceExhausted:
        # Daily/free-tier quota exhausted — retries won't help, fail soft.
        return (
            "I'm sorry, our assistant is temporarily busy. "
            "Please try again in a few minutes or contact support."
        )

    return response.text.strip()