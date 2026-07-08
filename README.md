# 📚 AI Customer Support Chatbot

An AI-powered customer support chatbot built using **FastAPI**, **Google Gemini**, **Supabase (pgvector)**, **Sentence Transformers**, **Streamlit**, and **n8n**. The system uses a **Retrieval-Augmented Generation (RAG)** pipeline to answer customer queries from a knowledge base, perform intent classification, calculate response confidence, and trigger human handoff when required.

> **Designed with a modular API-first architecture, the backend can support multiple communication channels (Web, Telegram, Email, Slack, WhatsApp, etc.) without changing the AI backend.**

---

# 🚀 Features

- 🤖 AI-powered customer support assistant
- 📖 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic search using Sentence Transformers
- 🗄️ Supabase PostgreSQL + pgvector vector database
- ✨ Google Gemini for response generation
- 🎯 Intent classification
- 📊 Confidence score calculation
- 👨‍💼 Confidence-based human handoff
- 🌐 FastAPI REST API
- 💬 Streamlit web interface
- ⚙️ n8n workflow automation
- 🏗️ API-first architecture for future multi-channel support

---

# 🏗️ System Architecture

```
                  Streamlit UI
                       │
                       ▼
                  n8n Workflow
                       │
                       ▼
                 FastAPI Backend
                       │
              Intent Classification
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 Knowledge Base                Customer Database
        │                             │
        └──────────────┬──────────────┘
                       ▼
              Semantic Vector Search
                       ▼
                 Google Gemini
                       ▼
             Confidence Calculation
                       ▼
               JSON Response
```

---

# 🔄 Multi-Channel Ready Architecture

The project follows a **single backend, multiple channel** design.

All AI logic is centralized inside the FastAPI backend.

Because every request is processed through the same API (`POST /ask`), additional communication channels can be integrated **without modifying the backend**.

Future channels can include:

- 🌐 Website Chat
- 💬 Telegram Bot
- 📧 Email
- 💼 Slack
- 📱 WhatsApp
- 📲 Microsoft Teams

Example future architecture:

```
Website Chat
Telegram
Email
Slack
WhatsApp
      │
      ▼
      n8n
      │
      ▼
 FastAPI Backend
      │
 RAG + Gemini
      │
 JSON Response
```

Only the **input/output channels change**. The AI backend, retrieval pipeline, and business logic remain unchanged.

---

# 🛠️ Tech Stack

### Backend

- FastAPI
- Python

### Frontend

- Streamlit

### Large Language Model

- Google Gemini

### Embedding Model

- BAAI/bge-small-en-v1.5

### Vector Database

- Supabase PostgreSQL
- pgvector

### Workflow Automation

- n8n
- ngrok

### Libraries

- Sentence Transformers
- psycopg2
- pgvector
- python-dotenv
- requests

---

# 📂 Project Structure

```
AI_customer_support_chatbot/
│
├── app/
│   ├── app.py
│   ├── confidence_score.py
│   ├── gemini.py
│   ├── intent_classification.py
│   ├── rag.py
│   └── database.py
│
├── ingestion/
│   ├── extract_text.py
│   ├── chunk_text.py
│   ├── embed_store.py
│   └── ingest.py
│
├── frontend.py
│
├── sql
│
├── knowledge_base/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Workflow

1. User submits a query through the Streamlit interface.
2. n8n forwards the request to the FastAPI backend.
3. Intent classification determines the appropriate data source.
4. The query is embedded using Sentence Transformers.
5. pgvector retrieves the most relevant knowledge base chunks.
6. Gemini generates a context-aware response.
7. A confidence score is calculated.
8. If confidence falls below the threshold, the response is flagged for human handoff.
9. The final response is returned to the user.

---

# 📊 Confidence Score

The confidence score combines:

- Top semantic similarity
- Average similarity
- Strong retrieval bonus
- Fallback response penalty

Human handoff is triggered when:

```
Confidence < 80%
```

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/anushkam545/AI_customer_support_chatbot.git
cd AI_customer_support_chatbot
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=
SUPABASE_URL=
SUPABASE_SERVICE_KEY=
GEMINI_API_KEY=
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

---

# ▶️ Run FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Streamlit

```bash
streamlit run frontend/streamlit_app.py
```

---

# ▶️ Run ngrok

```bash
ngrok http 8000
```

---

# ▶️ n8n Workflow

The n8n workflow:

- Receives user requests
- Calls the FastAPI backend
- Routes responses based on the `human_handoff` flag
- Returns the final response to the client

---

# 🔮 Future Enhancements

- Telegram integration
- Email integration
- Slack integration
- WhatsApp integration
- Automatic ticket creation
- Conversation history
- Analytics dashboard
- Multi-language support

---

# 👩‍💻 Author

**Anushka Mishra**

GitHub: https://github.com/anushkam545

---

## ⭐ Architecture Highlight

This project follows an **API-first modular design**.

The AI backend is completely independent of the user interface. Because all communication goes through a single FastAPI endpoint, the same backend can power multiple client applications (Web, Telegram, Email, Slack, WhatsApp, etc.) **without requiring any changes to the AI, RAG pipeline, or business logic**. This makes the system scalable, maintainable, and ready for future multi-channel deployment.
