"""
confidence.py

Calculates a confidence score for chatbot responses and determines
whether the query should be handed off to a human support agent.
"""

# Gemini fallback phrases

_FALLBACK_PHRASES = [
    "i'm sorry, i don't have that information",
    "i'm sorry, i couldn't find that information",
    "i don't know",
    "not available in the provided documents",
    "insufficient information",
]

def _response_has_fallback(response: str) -> bool:
    """
    Return True if Gemini could not answer the user's question.
    """

    if not response or not response.strip():
        return True

    response = response.lower()

    return any(
        phrase in response
        for phrase in _FALLBACK_PHRASES
    )

# Confidence Calculation

def calculate_confidence(
    intent: str,
    similarities: list[float] | None,
    response: str,
    records_found: bool = True,
) -> dict:
    """
    Calculate confidence score (0-100) and determine whether
    the chatbot should hand off the conversation to a human.

    Parameters
    ----------
    intent : str
        Either:
            "knowledge_base"
            "customer_database"

    similarities : list[float] | None
        Similarity scores returned from pgvector.

    response : str
        Gemini-generated response.

    records_found : bool
        Used only for customer_database intent.

    Returns
    -------
    {
        "confidence": int,
        "human_handoff": bool
    }
    """

    confidence = 0

    # KNOWLEDGE BASE
     
    if intent == "knowledge_base":

        similarities = similarities or []

        if similarities:

            top_similarity = max(similarities)
            average_similarity = sum(similarities) / len(similarities)

            # Retrieval score
            # Max contribution:
            # Top similarity      -> 60
            # Average similarity  -> 25
            retrieval_score = (
                top_similarity * 60
                + average_similarity * 25
            )

            # Bonus only for strong retrieved chunks
            chunk_bonus = sum(
                2
                for similarity in similarities
                if similarity >= 0.75
            )

            confidence = retrieval_score + chunk_bonus

        else:
            confidence = 0

        # Penalize if Gemini couldn't answer
        if _response_has_fallback(response):
            confidence *= 0.6

    # CUSTOMER DATABASE

    elif intent == "customer_database":

        if not records_found:
            confidence = 25

        elif _response_has_fallback(response):
            confidence = 60

        else:
            confidence = 95

    # UNKNOWN INTENT

    else:
        raise ValueError(f"Unknown intent: {intent}")

    # Clamp to valid range
    confidence = round(
        max(0, min(confidence, 100))
    )

    human_handoff = confidence < 80

    return {
        "confidence": confidence,
        "human_handoff": human_handoff,
    }