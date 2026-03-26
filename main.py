import streamlit as st
from chatbot import chat_with_gpt

st.title("ChatGPT-5 Nano Restaurant Recommender")
st.write("Welcome to the GPT-5 Nano Chatbot! Type 'exit' or 'quit' to end the chat.")
st.write("Start with a prompt or write a message:")

system_prompt = {
    "role": "system",
    "content": "You are a helpful restaurant recommendation chatbot. "
               "You cannot handle requests that are not related to restaurants. "
                "If the user asks for something that is not related to restaurants, politely inform them that you can only provide restaurant recommendations. "
}

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    print("User input:", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_gpt(st.session_state.messages)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


