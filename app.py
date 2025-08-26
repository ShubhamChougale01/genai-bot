import streamlit as st
from main import answer_query 

st.set_page_config(page_title="GenAI Bot", layout="centered")
st.title("AI Chatbot Capabilities")
st.markdown("""
---
1. Answer questions from a given PDF (Retrieval-Augmented Generation)  
2. Perform arithmetic operations  
3. Answer general questions by searching the web
""")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Type your question here...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    response = answer_query(query)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

