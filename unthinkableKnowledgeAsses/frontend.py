import streamlit as st
import requests

# 1. Professional Page Configuration
st.set_page_config(
    page_title="Enterprise AI Knowledge Base",
    page_icon="🤖",
    layout="wide"
)

# 2. Sidebar for Status
with st.sidebar:
    st.title("⚙️ System Status")
    st.success("Backend: Connected (FastAPI)")
    st.success("Model: Llama 3.2 (Local)")
    st.divider()
    st.markdown("🔍 **Instructions:** Type a question about your uploaded PDFs in the chat box to begin.")

# 3. Main UI Header
st.title("📂 Industry RAG Assistant")
st.write("Secure, private, and local document intelligence.")
st.divider()

# 4. Chat History Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("How can I help you today?"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response (calling your FastAPI backend)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents..."):
            try:
                response = requests.get(f"http://127.0.0.1:8000/ask?query={prompt}")
                data = response.json()
                
                # Show the Answer
                st.markdown(data["answer"])
                
                # Show the Sources in a nice expander
                if "sources" in data and data["sources"]:
                    with st.expander("📚 View Sources"):
                        for source in data["sources"]:
                            st.write(f"- {source}")
                
                st.session_state.messages.append({"role": "assistant", "content": data["answer"]})
            except:
                st.error("Connection Error")