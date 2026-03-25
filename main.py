import streamlit as st
from chatbot import chat_with_gpt

st.title("ChatGPT-5 Nano Restaurant Recommender")
st.write("Welcome to the GPT-5 Nano Chatbot! Type 'exit' or 'quit' to end the chat.")
st.write("Start with a prompt or write a message:")
# prompts = [
#     "Find the best restaurants in Baltimore, Maryland.",
#     "What are some good places to eat in Baltimore?",
#     "Can you recommend any restaurants in Baltimore?",
#     "Where can I find good food in Baltimore?",
#     "What are the 5 top-rated restaurants in Baltimore?",
#     "Are there any hidden gems for dining in Baltimore?",
#     "What are the best places to eat in Baltimore according to reviews?",
#     "Can you suggest some popular restaurants in Baltimore?",
#     "Where can I find the best cuisine in Baltimore?",
#     "What are the must-try restaurants in Baltimore?"
# ]
system_prompt = {
    "role": "system",
    "content": "You are a helpful restaurant recommendation chatbot. "
               "You cannot handle requests that are not related to restaurants. "
                "If the user asks for something that is not related to restaurants, politely inform them that you can only provide restaurant recommendations. "
}
# for i, prompt in enumerate(prompts, 1):
#     st.write(f"{i}. {prompt}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = chat_with_gpt(st.session_state.messages)
        st.write(response)
        # st.markdown(response)
        # print("Chatbot response:", response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


