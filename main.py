import streamlit as st
from chatbot import chat_with_gpt, voice_chat_with_gpt
# from text_chat import render_text_chat
# from voice_chat import render_voice_chat

# st.set_page_config(page_title="Chef Dee AI", page_icon="🍽️", layout="wide")

# tab1, tab2 = st.tabs(["Text Chat", "Voice Chat"])

def render_text_chat():
    st.markdown(f"# {list(page_names_to_funcs.keys())[0]} 🍽️")
    st.set_page_config(
        page_title="Chef Dee's AI Kitchen 🍽️",
        page_icon="🍳",
        layout="centered"
    )

    # st.markdown("""
    # <style>
    #     .stChatMessage {
    #         border-radius: 12px;
    #         padding: 10px;
    #         margin-bottom: 10px;
    #     }
    #     .stChatMessage.user {
    #         background-color: #f0f2f6;
    #     }
    #     .stChatMessage.assistant {
    #         background-color: #ffe4e1;
    #     }
    # </style>
    # """, unsafe_allow_html=True)

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
                    "Keep all responses concise and to the point, ideally under 150 words. Always end with a follow-up question to keep the conversation going. I need you to be engaging and make the user feel like they are talking to a real person, not a robot. Make the conversation more fun!"
    }

    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt]

    if len(st.session_state.messages) == 1:
        welcome_msg = """
            I'm Chef Ramsay 🔥
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


def render_voice_chat():
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]} 🎤")
    # st.logo(
    # "logo.png",
    # size="medium",
    # link="https://platform.openai.com/docs",
    # )

    st.title("Transcription with Whisper")

    audio_value = st.audio_input("record a voice message to transcribe")

    if audio_value:
        with st.spinner("Transcribing..."):
            transcript = voice_chat_with_gpt(audio_value)
            transcript_text = transcript.text
            st.write(transcript_text)

def render_reviews_chat():
    st.markdown(f"# {list(page_names_to_funcs.keys())[2]} ⭐")
    system_prompt_r = {
        "role": "system",
        "content": "You are a restaurant review chatbot. "
        "You provide detailed and honest reviews of restaurants based on user input. "
        "You respond as a knowledgeable food critic with a passion for dining out. You do not over explain yourself but you are very informative and helpful. Keep your responses concise and engaging."
        "You can provide information about the food, service, ambiance, and overall experience at the restaurant. "
        "You can also provide recommendations for similar restaurants based on the user's preferences. "
        "Your tone is friendly, informative, and engaging. You aim to help users make informed decisions about where to eat. "
        "You do not give recommendations only reviews and images of the restaurant. You can pull information from real reviews online but you cannot make up reviews. If you don't know about a restaurant, say you don't know instead of making something up."
    }
    if "messages" not in st.session_state:
        st.session_state.messages = [system_prompt_r]

    if len(st.session_state.messages) == 1:
        review_message = """
            I'm Rev your Reviewer ⭐
            Let's find you something amazing reviews!
        """
        st.session_state.messages.append({"role": "assistant", "content": review_message})
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



page_names_to_funcs = {
    "Text Chat": render_text_chat,
    "Voice Chat": render_voice_chat,
    "Reviews": render_reviews_chat,
}

selected_demo = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[selected_demo]()
