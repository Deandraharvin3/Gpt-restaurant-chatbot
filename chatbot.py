from openai import OpenAI
import streamlit as st

client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

def chat_with_gpt(messages):
    response = client.responses.create(
    model="gpt-5",
    tools=[{
        "type": "web_search",
        "user_location": {
            "type": "approximate",
            "country": "US",
            "city": "Baltimore",
            "region": "Maryland",
        },
        # "filters":{
        #     "allowed_domains": [
        #         "www.google.com",
        #         "www.opentable.com",
        #         "www.eater.com",
        #         "www.baltimoremagazine.com",
        #         "www.yelp.com",
        #     ]
        # }
    }],
    input=messages,
    )
    return response.output_text

def voice_chat_with_gpt(audio_value):
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file = audio_value
    )
    return response