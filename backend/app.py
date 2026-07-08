"""
app.py
Main FastAPI application for AI customer support.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

from backend.intent_classification import classify_intent
from backend.rag import search_knowledge_base
from backend.database import get_customer_by_email, get_book_by_customer, get_open_ticket, save_conversation
from backend.gemini import generate_response
from backend.confidence_score import calculate_confidence

load_dotenv()

app = FastAPI()

class QuestionRequest(BaseModel):
    customer_email: str
    question: str

@app.post("/ask")
def ask(request: QuestionRequest):
    try:
        return _ask(request)
    except ResourceExhausted:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily over quota. Please try again shortly.",
        )


def _ask(request: QuestionRequest):

    # Step 1: Classify intent
    intent = classify_intent(request.question)

    # Step 2: Route based on intent
    if intent == "customer_database":

        # Resolve customer from email
        customer = get_customer_by_email(request.customer_email)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found.")

        customer_id = customer["customer_id"]

        # Gather all customer data
        books = get_book_by_customer(customer_id)
        ticket = get_open_ticket(customer_id)

        database_result = {
            "customer": customer,
            "books": books,
            "open_ticket": ticket,
        }

        # Generate answer
        answer = generate_response(
            user_question=request.question,
            intent=intent,
            database_result=database_result,
        )

        # Calculate confidence
        records_found = bool(customer)
        result = calculate_confidence(
            intent=intent,
            similarities=None,
            response=answer,
            records_found=records_found,
        )

        # Save conversation
        save_conversation(
            customer_id=customer_id,
            question=request.question,
            answer=answer,
            confidence=result["confidence"],
        )

    else:  # knowledge_base

        # Retrieve relevant chunks
        chunks = search_knowledge_base(request.question)

        # Generate answer
        answer = generate_response(
            user_question=request.question,
            intent=intent,
            retrieved_context=chunks,
        )

        # Calculate confidence
        similarities = [c["similarity"] for c in chunks if "similarity" in c]
        result = calculate_confidence(
            intent=intent,
            similarities=similarities,
            response=answer,
        )

        # Resolve customer_id for saving (best effort — email may not exist in DB)
        customer = get_customer_by_email(request.customer_email)
        customer_id = customer["customer_id"] if customer else request.customer_email

        save_conversation(
            customer_id=customer_id,
            question=request.question,
            answer=answer,
            confidence=result["confidence"],
        )

    return {
        "answer": answer,
        "intent": intent,
        "confidence": result["confidence"],
        "human_handoff": result["human_handoff"],
    }