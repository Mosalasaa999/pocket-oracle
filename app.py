import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

st.set_page_config(page_title="Pocket Oracle", page_icon="⚡")
st.title("⚡ Pocket Oracle")
st.caption("AI Lease Analyzer - Live Beta")

# SECURE KEY RETRIEVAL
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("⚠️ Secrets not configured.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Upload Lease/OTP (PDF)", type=("pdf"))

if uploaded_file:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    st.success(f"✅ Loaded {len(reader.pages)} pages.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Ready. Ask me anything."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
            full_prompt = f"Contract: {text} Question: {prompt}"
            response = model.generate_content(full_prompt)
            msg = response.text
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
        except Exception as e:
            st.error(f"Error: {e}")
