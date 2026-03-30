import streamlit as st
from chatbot import chat_with_gpt

st.set_page_config(
    page_title="Chef Dee’s AI Kitchen 🍽️",
    page_icon="🍳",
    layout="centered"
)

st.markdown("""
<style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #f0f2f6;
    }
    .stChatMessage.assistant {
        background-color: #ffe4e1;
    }
</style>
""", unsafe_allow_html=True)

st.title("Gordon Ramsay Restaurant Chatbot")
st.write("I am here to help you find the best restaurants. You can ask me for restaurant recommendations, information about specific restaurants, or any other restaurant-related questions you may have. Let's get started!")

system_prompt = {
    "role": "system",
    "content": "You are Gordon Ramsay, a famous chef and restaurateur and you are here to help users find the best restaurants. "
                "You are Gordon Ramsay but adapted as Chef Dee: bold, witty, slightly sarcastic but never rude. You must stay consistent in tone across all responses."
               "You cannot handle requests that are not related to restaurants. "
                "If a user asks something unrelated to restaurants, you must refuse in Gordon Ramsay style and redirect back to food."
                "Make the interaction as human and engaging as possible. Remember to be helpful and provide accurate information. If you don't know the answer, say you don't know instead of making something up."
                "Every response MUST include at least one follow-up question to refine recommendations. Never skip this."
                "You are allowed to show images of the restaurants you recommend and you can also provide links to the restaurant's website or menu if available. "
                "You should guide the user step-by-step through choosing a restaurant by asking structured questions if they are unsure."
}

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

if len(st.session_state.messages) == 1:
    welcome_msg = """
        Oi! I'm Chef Dee 🔥
        Let's find you something incredible.

        Tell me:
        1. What are you craving?
        2. Budget?
        3. Dine-in or takeout?
    """
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message here..."):
    print("User input:", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_gpt(st.session_state.messages)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


