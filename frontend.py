"""
streamlit_app.py
Light peach/pink UI for AI customer support backend.
"""
import requests
import streamlit as st

API_URL = "https://anushka26.app.n8n.cloud/webhook/ask"

SUGGESTED_QUESTIONS = [
    "What is the status of my book?",
    "How does the publishing process work?",
    "When will I receive my royalty payment?",
]

st.set_page_config(page_title="Bookleaf Support", page_icon="📚", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #fff5f2 0%, #ffe8ee 50%, #ffe0d6 100%);
    color: #3a2b30 !important;
}
p, span, label, div, li { color: #3a2b30 !important; }
h1, h2, h3 { color: #d1567a !important; }
div.stButton > button {
    background: #ffffff;
    color: #3a2b30 !important;
    border: 1px solid #f3b6c9;
    border-radius: 20px;
    padding: 6px 16px;
}
div.stButton > button:hover {
    background: #ffd6e0;
    border-color: #d1567a;
    color: #3a2b30 !important;
}
.stChatMessage {
    background: #fffaf7;
    border-radius: 14px;
    border: 1px solid #ffdce6;
    color: #3a2b30 !important;
}
input, textarea {
    color: #fff5f2 !important;
    background-color: #e8879f !important;
    caret-color: #fff5f2 !important;
}
input::placeholder, textarea::placeholder {
    color: #ffe6ec !important;
}
.badge {
    display:inline-block; padding:2px 10px; border-radius:12px;
    font-size:12px; font-weight:600; margin-left:8px;
}
.badge-high { background:#d9f2e0; color:#2f8f4e; }
.badge-low  { background:#ffe1e1; color:#c0392b; }
</style>
""", unsafe_allow_html=True)

st.title("📚 Bookleaf Support")
st.caption("Ask about your book, royalties, tickets, or our publishing process.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "email" not in st.session_state:
    st.session_state.email = ""
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

st.session_state.email = st.text_input("Your email", value=st.session_state.email, placeholder="you@example.com")

st.markdown("**Try asking:**")
cols = st.columns(len(SUGGESTED_QUESTIONS))
for col, q in zip(cols, SUGGESTED_QUESTIONS):
    if col.button(q, use_container_width=True):
        st.session_state.pending_question = q

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "confidence" in msg:
            badge_class = "badge-high" if msg["confidence"] >= 80 else "badge-low"
            st.markdown(
                f'<span class="badge {badge_class}">Confidence {msg["confidence"]}%</span>'
                + (' <span class="badge badge-low">Human review suggested</span>' if msg["human_handoff"] else ""),
                unsafe_allow_html=True,
            )

typed_question = st.chat_input("Type your question...")
question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if question:
    if not st.session_state.email:
        st.warning("Please enter your email first.")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"customer_email": st.session_state.email, "question": question},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["answer"],
                    "confidence": data["confidence"],
                    "human_handoff": data["human_handoff"],
                })
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
        st.rerun()