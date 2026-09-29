import os
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Page Config Styling
st.set_page_config(
    page_title="Maison Hygia AI Support & Fellowship Desk",
    page_icon="🌿",
    layout="centered"
)

@st.cache_resource
def load_kb():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists("faiss_index"):
        return FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return None

vector_store = load_kb()

# Safety & Medical Guardrail Filter
def safety_guardrail(query: str) -> bool:
    critical_triggers = ["suicide", "self-harm", "overdose", "severe chest pain", "bleeding"]
    q_lower = query.lower()
    return any(trigger in q_lower for trigger in critical_triggers)

def retrieve_context(query: str) -> str:
    if not vector_store:
        return "Knowledge base not initialized."
    docs = vector_store.similarity_search(query, k=2)
    return "\n\n".join([doc.page_content for doc in docs])

def generate_local_rag_response(query: str, context: str) -> str:
    # Formats the retrieved RAG markdown chunks into a polished support response
    response = (
        f"🌿 **Maison Hygia AI Support Desk (Verified RAG Match):**\n\n"
        f"Based on your query regarding *\"{query}\"*, here are the relevant details from our verified catalog & guidelines:\n\n"
        f"---\n{context}\n---\n\n"
        f"*Is there anything specific regarding ingredients, usage instructions, or our shipping policies I can help clarify further?*"
    )
    return response

# --- UI Layout ---
st.markdown("# 🌿 Maison Hygia AI")
st.markdown("### *Holistic Wellness Support, Catalog Assistant & Fellowship Desk*")
st.markdown("---")

# Sidebar Configuration & Escalation Portal
with st.sidebar:
    st.markdown("### 🧭 Navigation & Control")
    st.write("**Role Representation:** Maison Hygia AI Fellowship Desk")
    
    if st.button("🚨 Escalate to Human Specialist"):
        st.session_state.escalated = True
        
    if st.session_state.get("escalated", False):
        st.error("⚠️ **Ticket Escalated:** A clinical support specialist has been pinged and will review your chat transcript shortly.")
        if st.button("Reset Escalation Status"):
            st.session_state.escalated = False
            st.rerun()
            
    st.markdown("---")
    st.markdown("### 💡 Quick Prompts")
    if st.button("Tell me about the Hydration Serum"):
        st.session_state.quick_query = "Tell me about the Hygia Glow Hydration Serum"
    if st.button("What is your return policy?"):
        st.session_state.quick_query = "What is your return policy?"
    if st.button("Sleep tincture directions"):
        st.session_state.quick_query = "How do I use the sleep tincture?"

# Initialize Chat State History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello and welcome to Maison Hygia. How may I support your wellness journey or assist you with our catalog today?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture User Input (including Sidebar quick buttons)
prompt = st.chat_input("Ask a wellness question or search catalog...")
if "quick_query" in st.session_state and st.session_state.quick_query:
    prompt = st.session_state.quick_query
    st.session_state.quick_query = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        if safety_guardrail(prompt):
            response_text = (
                "⚠️ **Safety Notice:** We care deeply about your well-being. Because your input mentions critical symptoms "
                "or distress, automated responses are disabled. Please reach out to emergency services immediately, or click "
                "**'Escalate to Human Specialist'** in the sidebar to talk with our clinical team."
            )
            st.markdown(response_text)
        elif "human" in prompt.lower() or "agent" in prompt.lower() or "specialist" in prompt.lower():
            response_text = "I am transferring your session to a human wellness expert right now. Please stand by."
            st.session_state.escalated = True
            st.markdown(response_text)
        else:
            with st.spinner("Searching Maison Hygia knowledge base..."):
                context = retrieve_context(prompt)
                response_text = generate_local_rag_response(prompt, context)
            st.markdown(response_text)
            
        st.session_state.messages.append({"role": "assistant", "content": response_text})