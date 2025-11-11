import streamlit as st
import os
from vector_store import build_faiss, load_faiss
from qa_engine import load_qa

# --- Azure-safe Streamlit Config ---
st.set_page_config(page_title="📑 Policy Chatbot", layout="centered")

# Ensure these env vars are applied before Streamlit starts
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_ENABLECORS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLEXsrfProtection"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION"] = "false"

# --- Safe upload directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
INDEX_DIR = os.path.join(BASE_DIR, "indexes")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# --- Title ---
st.title("📑 Policy Chatbot")

# ---- File Upload Section ----
uploaded = st.file_uploader("📄 Upload a PDF file", type=["pdf"])

if uploaded is not None:
    try:
        # Secure filename handling
        safe_filename = os.path.basename(uploaded.name)
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded.getbuffer())

        st.success(f"✅ {safe_filename} uploaded successfully!")

        # Build FAISS index
        index_path = os.path.join(INDEX_DIR, safe_filename.replace(".pdf", ""))
        build_faiss(file_path, index_path=index_path)

        st.session_state["active_index"] = index_path
        st.session_state["qa_chain"] = load_qa(index_path)
        st.success("Index built successfully — start chatting below!")

    except Exception as e:
        st.error(f"⚠️ Upload failed: {e}")

# ---- Chat Window ----
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask me anything about the policy..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if "qa_chain" in st.session_state:
        try:
            qa_chain = st.session_state["qa_chain"]
            raw = qa_chain.invoke(prompt)
            answer = raw.content if hasattr(raw, "content") else str(raw)
            st.session_state["messages"].append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        with st.chat_message("assistant"):
            st.write("⚠️ Please upload a PDF first.")
