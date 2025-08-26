import streamlit as st

st.set_page_config(page_title="GenAI Bot", layout="centered")
st.title("Mini GenAI Chatbot")
st.markdown("Type something and I'll just print it back!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Type your question here : ")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    response = f"User asked: **{query}**"

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
