import streamlit as st
from chatbot import chat_with_gpt, voice_chat_with_gpt, get_google_place_photo

st.set_page_config(page_title="Chef's Table", page_icon="🍽️", layout="centered")

def inject_foodie_css():
    st.markdown("""
    <style>
        :root {
            --chef-red: #D32F2F; 
            --review-gold: #FFC107;
            --user-bg: #F5F5F5;
            --text-dark: #212121;
        }

        .stChatMessage {
            border-radius: 20px !important;
            padding: 15px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        
        div[data-testid="stChatMessage"]:nth-child(odd) {
            background-color: var(--user-bg);
            color: var(--text-dark);
            border: 1px solid #E0E0E0;
        }

        div[data-testid="stChatMessage"]:nth-child(even) {
            background-color: #FFF3E0;
            border-left: 5px solid var(--chef-red);
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

inject_foodie_css()

if "chef_messages" not in st.session_state:
    st.session_state.chef_messages = []
if "rev_messages" not in st.session_state:
    st.session_state.rev_messages = []
if "rev_pending_image_prompt" not in st.session_state:
    st.session_state.rev_pending_image_prompt = None
if "macro_messages" not in st.session_state:
    st.session_state.macro_messages = []
if "date_messages" not in st.session_state:
    st.session_state.date_messages = []
if "roulette_messages" not in st.session_state:
    st.session_state.roulette_messages = []

_chat_intent_map = {
    "rev_messages": {
        "name": "Rev (Vibe Check)",
        "keywords": ["review", "vibe", "rate", "rating", "is it good", "vibe check", "aesthetic"],
    },
    "macro_messages": {
        "name": "The Macro Hacker (Fitness)",
        "keywords": ["macro", "protein", "calories", "nutrition", "diet", "carbs", "fat"],
    },
    "date_messages": {
        "name": "Date Night Architect (Ambiance)",
        "keywords": ["date", "romantic", "anniversary", "candlelight", "ambiance", "mood"],
    },
    "chef_messages": {
        "name": "Chef Dee (Recommendations)",
        "keywords": ["recommend", "suggest", "menu", "place", "food", "craving", "budget"],
    },
    "roulette_messages": {
        "name": "Food Roulette (Indecisive)",
        "keywords": ["city", "dealbreakers", "argument", "choose", "can't decide"],
    },
}

def detect_best_chat_for_prompt(active_state_key, prompt_text):
    normalized = prompt_text.lower()
    for key, info in _chat_intent_map.items():
        if key == active_state_key:
            continue
        if any(k in normalized for k in info["keywords"]):
            return info["name"]
    return None


def run_chat_session(state_key, system_prompt, welcome_message, audio_label, text_label, key_prefix, assistant_avatar="🤖", bg_color="#FFFFFF"):

    st.markdown(
        "<style>.stApp { background-color: " + bg_color + " !important; }</style>", 
        unsafe_allow_html=True
    )    
    if not st.session_state[state_key]:
        st.session_state[state_key] = [system_prompt]
        st.session_state[state_key].append({"role": "assistant", "content": welcome_message})

    chat_container = st.container()
    
    col1, col2 = st.columns([1, 4])
    with col1:
        audio_value = st.audio_input(audio_label, key=key_prefix + "_audio")
    with col2:
        text_prompt = st.chat_input(text_label, key=key_prefix + "_text")

    final_prompt = None
    if audio_value:
        with st.spinner("Listening..."):
            transcript = voice_chat_with_gpt(audio_value)
            final_prompt = transcript.text
    elif text_prompt:
        final_prompt = text_prompt

    with chat_container:
        for message in st.session_state[state_key][1:]:
            avatar = assistant_avatar if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        if final_prompt:
            st.session_state[state_key].append({"role": "user", "content": final_prompt})

            # Inform user of better chat persona match, instead of auto-redirecting
            suggested_chat = detect_best_chat_for_prompt(state_key, final_prompt)
            if suggested_chat is not None:
                st.info(
                    "Heads up: your question looks like a great fit for '" + suggested_chat + "'. "
                    "Try that tab so the bot can provide the most focused response. "
                )
            with st.chat_message("user", avatar="👤"):
                st.markdown(final_prompt)

            with st.chat_message("assistant", avatar=assistant_avatar):
                with st.spinner("Thinking..."):
                    response = chat_with_gpt(st.session_state[state_key])
                st.markdown(response)

            st.session_state[state_key].append({"role": "assistant", "content": response})

def render_text_chat():
    st.title("🔥 Chef Dee's Kitchen")
    st.caption("Don't be a donkey. Tell me what you're craving.")

    system_prompt = {
        "role": "system",
        "content": (
            "You are Chef Dee, an elite, fiery, Gordon Ramsay-style executive chef. "
            "Your tone is bold, witty, and slightly sarcastic but never rude. "
            "RULES: "
            "1. You are strictly a restaurant and food expert. "
            "2. OUT OF SCOPE GUARDRAIL: If a user asks about the weather, sports, politics, math, or ANY topic unrelated to dining out or food, you MUST refuse to answer. "
            "3. REFUSAL BEHAVIOR: Refuse in character. (e.g., 'Do I look like a bloody meteorologist? I am a chef. Are we talking about food or are you going to waste my time?') "
            "4. Every response MUST include at least one follow-up question to refine recommendations. "
            "5. Never say 'I don't know' weakly. Say 'I haven't cooked there, mate, so I won't lie to you.'"
        )
    }
    welcome = "I'm Chef Dee 🔥 Let's find you something incredible.\n\nTell me:\n1. What are you craving?\n2. Budget?\n3. Dine-in or takeout?"

    run_chat_session(
        state_key="chef_messages",
        system_prompt=system_prompt,
        welcome_message=welcome,
        audio_label="Speak to Chef",
        text_label="Or type your craving here...",
        key_prefix="chef",
        assistant_avatar="👨‍🍳",
        bg_color="#F4C4A2"
    )

def render_reviews_chat():
    st.title("📱 Rev's Vibe Check")
    st.caption("Drop a restaurant name. I'll tell you if it's bussin' or mid.")

    system_prompt_r = {
        "role": "system",
        "content": (
            "You are Rev, a brutally honest Gen Z food critic and TikToker. "
            "You review restaurants based on real-world reputation, star ratings, and vibes. "
            "RULES: "
            "1. You only care about restaurant reviews, aesthetics, and vibes. Give the user the tea on whether it's actually good or just looks good on Instagram. "
            "2. OUT OF SCOPE GUARDRAIL: If the user asks about the weather, homework, news, or anything not related to food/vibes, you MUST refuse. "
            "3. REFUSAL BEHAVIOR: Refuse in character. (e.g., 'I don't do weather forecasts, fam. I'm here to spill the tea on restaurants, not the climate.') "
            "4. Always include a hypothetical Vibe Score out of 10 for restaurants. Say things like 'This place is a 9/10 for vibes but only a 6/10 for food' or 'The aesthetics are fire, but the reviews say it's a 4/10 overall.' Be specific about what makes the vibe good or bad. "
            "5. After your review, ask the user if they want to see a real image of the restaurant. Make sure you only ask if they give you a restaurant name to review, and not for any other type of input. If they say yes, you will show them a real photo of the restaurant from Google Places. If they say no, you will say 'Bet, no pressure. Drop another restaurant and I'll keep it 100 with you.'"
        )
    }

    st.markdown(
        "<style>.stApp { background-color: #D7BCF8 !important; }</style>",
        unsafe_allow_html=True
    )

    if not st.session_state.rev_messages:
        st.session_state.rev_messages = [system_prompt_r]
        st.session_state.rev_messages.append({
            "role": "assistant",
            "content": "Sup. I'm Rev. ⭐ Drop a restaurant name and let's see if it's actually fire or just an aesthetic trap."
        })

    chat_container = st.container()

    col1, col2 = st.columns([1, 4])
    with col1:
        audio_value = st.audio_input("Spill the tea", key="rev_audio")
    with col2:
        text_prompt = st.chat_input("Or type a restaurant name...", key="rev_text")

    final_prompt = None
    if audio_value:
        with st.spinner("Listening..."):
            transcript = voice_chat_with_gpt(audio_value)
            final_prompt = transcript.text
    elif text_prompt:
        final_prompt = text_prompt

    with chat_container:
        for message in st.session_state.rev_messages[1:]:
            avatar = "🕶️" if message["role"] == "assistant" else "👤"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        if final_prompt:
            st.session_state.rev_messages.append({"role": "user", "content": final_prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(final_prompt)

            lower_prompt = final_prompt.lower().strip()

            yes_words = ["yes", "yeah", "yep", "sure", "ok", "okay", "show me", "image", "photo", "pic", "picture"]
            no_words = ["no", "nope", "nah", "not now"]

            if st.session_state.rev_pending_image_prompt is not None:
                with st.chat_message("assistant", avatar="🕶️"):
                    if any(word in lower_prompt for word in yes_words):
                        st.markdown("Bet. Here’s the real photo 👀")

                        place_photo = get_google_place_photo(
                            st.session_state.rev_pending_image_prompt,
                            city="Baltimore"
                        )

                        if place_photo:
                            if place_photo.get("photo_url"):
                                st.image(
                                    place_photo["photo_url"],
                                    caption=place_photo["name"] + " — " + place_photo.get("address", ""),
                                    use_container_width=True
                                )
                                response = "You got another spot you want me to vibe check?"
                                st.markdown(response)
                            else:
                                response = "I found the place, but no photo was available. Got another restaurant?"
                                st.markdown(response)
                        else:
                            response = "Couldn't find a matching restaurant photo. Got another spot?"
                            st.markdown(response)

                    elif any(word in lower_prompt for word in no_words):
                        response = "Cool, no pressure. Drop another restaurant and I’ll keep it real."
                        st.markdown(response)

                    else:
                        response = "I need a yes or no. Do you want the real restaurant image or not?"
                        st.markdown(response)

                st.session_state.rev_messages.append({"role": "assistant", "content": response})

                if any(word in lower_prompt for word in yes_words) or any(word in lower_prompt for word in no_words):
                    st.session_state.rev_pending_image_prompt = None

            else:
                with st.chat_message("assistant", avatar="🕶️"):
                    with st.spinner("Checking the vibes..."):
                        response = chat_with_gpt(st.session_state.rev_messages)

                    response = response + "\n\nWant me to show you a real image of this restaurant?"
                    st.markdown(response)

                st.session_state.rev_messages.append({"role": "assistant", "content": response})
                st.session_state.rev_pending_image_prompt = final_prompt

def render_macro_chat():
    st.title("💪 The Macro Hacker")
    st.caption("Tell me the restaurant, I'll tell you how to keep your gains.")

    system_prompt = {
        "role": "system",
        "content": (
            "You are the Macro Hacker, an intense, highly analytical fitness and nutrition coach. "
            "Your tone is encouraging but strict, using terms like macros, gains, empty carbs, and protein synthesis. You have the personality of a drill sergeant but the heart of a personal trainer. "
            "You are able to fully explain the meaning of calories, macros, and how different foods affect the body in a way that is easy to understand. "
            "RULES: "
            "1. You are exclusively focused on restaurant nutrition, macros, and fitness goals. "
            "2. OUT OF SCOPE GUARDRAIL: If the user asks about topics outside of nutrition, meal planning, or restaurants, you MUST refuse. "
            "3. REFUSAL BEHAVIOR: (e.g., 'Focus! We do not care about the weather unless it is raining protein. Stick to the meal plan. What restaurant are we analyzing?') "
            "4. Recommend the highest protein, most nutrient-dense meal on their menu. "
            "5. Estimate the calories and macro split (Protein/Carbs/Fat) for your recommendation."
        )
    }
    welcome = "Let's optimize this meal. 🏋️‍♂️ Drop a restaurant name, and I'll build you a plate that fits your macros."

    run_chat_session(
        state_key="macro_messages",
        system_prompt=system_prompt,
        welcome_message=welcome,
        audio_label="Log audio",
        text_label="Or type the restaurant here...",
        key_prefix="macro",
        assistant_avatar="🥗",
        bg_color="#BDE7CB"
    )

def render_date_chat():
    st.title("🕯️ Date Night Architect")
    st.caption("Ambiance is everything. Let's set the mood.")

    system_prompt = {
        "role": "system",
        "content": (
            "You are the Date Night Architect, a suave, observant, and highly romantic concierge. "
            "You care more about lighting, noise levels, seating arrangements, and intimacy than just the food. "
            "Your tone is charming, elegant, charismatic, and a little playful. You want to create unforgettable date night experiences like pop the balloon host Arlette. "
            "RULES: "
            "1. You deal exclusively with dating, romance, ambiance, and restaurant reservations. "
            "2. OUT OF SCOPE GUARDRAIL: If the user asks about general trivia, weather, or non-romantic topics, you MUST refuse elegantly. "
            "3. REFUSAL BEHAVIOR: 'I am afraid I must politely decline. My expertise lies solely in matters of the heart and evening reservations. Shall we return to planning your date?' "
            "4. Ask questions about the relationship stage (e.g., first date, 10th anniversary). "
            "5. Recommend places with the perfect vibe for their specific situation."
        )
    }
    welcome = "Good evening. 🥂 A memorable date is about the environment as much as the food. Tell me, is this a first date, an anniversary, or a 'just because' evening out?"

    run_chat_session(
        state_key="date_messages",
        system_prompt=system_prompt,
        welcome_message=welcome,
        audio_label="Speak softly",
        text_label="Or type the occasion here...",
        key_prefix="date",
        assistant_avatar="🍷",
        bg_color="#F77CA1"
    )

def render_roulette_chat():
    st.title("🎯 Food Roulette")
    st.caption("Can't decide? I'll make the choice for you. No arguments allowed.")

    system_prompt = {
        "role": "system",
        "content": (
            "You are the Roulette Master. Your job is to end the 'I don't know, what do you want?' argument. "
            "Your tone is fast-paced, decisive, and authoritative. "
            "RULES: "
            "1. You only exist to force the user to pick a restaurant. "
            "2. OUT OF SCOPE GUARDRAIL: You do not tolerate small talk. If they ask about the weather or anything else, you MUST refuse. "
            "3. REFUSAL BEHAVIOR: (e.g., 'Stop stalling. I do not care about the weather or your day. Give me your city and your dealbreakers, NOW.') "
            "4. Ask rapid-fire questions: City? Price limit? Any allergies? "
            "5. Once you have that data, make ONE definitive recommendation. Do not give options. The decision is final."
        )
    }
    welcome = "I end arguments. 🛑 You get ONE choice, and you have to eat there. To start the roulette wheel, tell me your city and your absolute dealbreakers (allergies/diets)."

    run_chat_session(
        state_key="roulette_messages",
        system_prompt=system_prompt,
        welcome_message=welcome,
        audio_label="Spin the wheel",
        text_label="Or type your city and dealbreakers...",
        key_prefix="roulette",
        assistant_avatar="🎰",
        bg_color="#E5DBAA"
    )

page_names_to_funcs = {
    "Chef Dee (Recommendations)": render_text_chat,
    "Rev (Vibe Check)": render_reviews_chat,
    "The Macro Hacker (Fitness)": render_macro_chat,
    "Date Night Architect (Ambiance)": render_date_chat,
    "Food Roulette (Indecisive)": render_roulette_chat,
}

st.sidebar.title("Navigation")
selected_demo = st.sidebar.selectbox("Choose your AI Guide", page_names_to_funcs.keys())
page_names_to_funcs[selected_demo]()