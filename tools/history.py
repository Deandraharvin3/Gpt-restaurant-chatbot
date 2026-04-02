import streamlit as st

st.title("🗄️ Your Chat History")

# Safely get the username, default to Guest if something goes wrong
username = st.session_state.get("user_name", "Guest")
st.caption(f"Viewing history for logged-in user: **{username}**")

# 1. Map readable names to your specific session state keys
history_maps = {
    "Chef Dee (Recommendations)": "chef_messages",
    "Rev (Vibe Check)": "rev_messages",
    "The Macro Hacker (Fitness)": "macro_messages",
    "Date Night Architect (Ambiance)": "date_messages",
    "Food Roulette (Indecisive)": "roulette_messages"
}

# 2. Map the avatars so the history looks identical to the live chat
avatar_maps = {
    "chef_messages": "👨‍🍳",
    "rev_messages": "🕶️",
    "macro_messages": "🥗",
    "date_messages": "🍷",
    "roulette_messages": "🎰"
}

# 3. UI for selecting which history to read
selected_persona = st.selectbox("Choose a conversation to review:", list(history_maps.keys()))
state_key = history_maps[selected_persona]
assistant_avatar = avatar_maps[state_key]

st.divider()

# 4. Render the history securely
# We check if the key exists AND if it has more than just the system prompt (index 0)
if state_key in st.session_state and len(st.session_state[state_key]) > 1:
    chat_container = st.container()
   
    with chat_container:
        # Slice from [1:] so the user NEVER sees the backend system rules
        for message in st.session_state[state_key][1:]:
            avatar = assistant_avatar if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
else:
    # Empty state UX
    st.info(f"No chat history found for {selected_persona} yet. Head back to the Dashboard to start chatting!")