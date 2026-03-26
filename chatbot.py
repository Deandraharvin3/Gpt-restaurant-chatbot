import os
from openai import OpenAI
import streamlit as st

client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

def chat_with_gpt(messages):
    # if user_input.isdigit() and 1 <= int(user_input) <= len(prompts):
    #     messages.append({"role": "user", "content": prompts[int(user_input) - 1]})
    # else:
    #     messages.append({"role": "user", "content": user_input})
    response = client.responses.create(
    model="gpt-5-nano",
    tools=[{
        "type": "web_search",
        "user_location": {
            "type": "approximate",
            "country": "US",
            "city": "Baltimore",
            "region": "Maryland",
        },
        "filters":{
            "allowed_domains": [
                "www.google.com",
                "www.opentable.com",
                "www.eater.com",
                "www.baltimoremagazine.com",
                "www.yelp.com",
            ]
        }
    }],
    input=messages,
    )
    return response.output_text
# if __name__ == "__main__":
#     chat_with_gpt()