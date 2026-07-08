import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

VALID_INTENTS = {"customer_database", "knowledge_base"}
DEFAULT_INTENT = "knowledge_base"
 
# Prompt
 
CLASSIFICATION_PROMPT = """\
You are an intent classifier for Bookleaf Publishing's customer support system.

Your only job is to read a customer's question and decide which data source is
needed to answer it. You must reply with EXACTLY one of these two strings and
nothing else:

  customer_database
  knowledge_base

Rules:

Return "customer_database" when the question requires personalised information
about a specific customer's account, such as:
- Book publishing status or current stage
- Manuscript submission or review progress
- Book live date or final submission date
- ISBN assigned to their book
- Royalty status or payment details
- Add-on services purchased
- Support ticket status or history
- Any detail tied to a specific customer record

Return "knowledge_base" when the question requires general information about
Bookleaf Publishing that applies to all customers, such as:
- How the publishing process works
- Editing, proofreading, or cover design services explained
- Royalty payment schedules or policies
- Manuscript formatting guidelines
- ISBN or copyright policies
- Marketing services overview
- General FAQs or company procedures

Do not explain your answer. Do not add punctuation. Output only the single
intent string.

Customer question: {question}
"""

# Classifier
 
def classify_intent(user_question: str) -> str:
    """
    Classify whether a question should be answered from the customer database
    or the knowledge base. Returns 'customer_database' or 'knowledge_base'.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in .env")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=model_name)
    prompt = CLASSIFICATION_PROMPT.format(question=user_question.strip())

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0,
                max_output_tokens=16,
            ),
        )

        # finish_reason 2 = SAFETY, 3 = RECITATION, etc. — no valid Part
        if (
            not response.candidates
            or response.candidates[0].finish_reason not in (0, 1)  # 0=UNSPECIFIED, 1=STOP
        ):
            return DEFAULT_INTENT

        raw = response.text.strip().lower()
        if raw not in VALID_INTENTS:
            return DEFAULT_INTENT
        return raw

    except ResourceExhausted:
        # Quota hit — don't crash the request, just use the default route.
        return DEFAULT_INTENT

    except (ValueError, AttributeError, IndexError):
        # response.text raises ValueError when no valid Part exists
        return DEFAULT_INTENT