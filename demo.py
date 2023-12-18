import os
import requests
from typing import Optional
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_API_URL = os.getenv("BASE_API_URL")
FLOW_ID = os.getenv("FLOW_ID")

if None in [API_KEY, BASE_API_URL, FLOW_ID]:
    st.error("Missing environment variables. Please check your .env file.")

# Setting page title and header
st.set_page_config(page_title="DEMO", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>a harmless chatbot appears! 😬</h1>", unsafe_allow_html=True)


# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "OpenAIConversationalAgent-4IhdD": {},
  "Calculator-lS5UW": {},
  "OpenAI-wT08R": {}
}

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param flow_id: The ID of the flow to run
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {"inputs": inputs}
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    # if api_key := st.secrets["API_KEY"]:
        # headers = {"x-api-key": api_key}
    if API_KEY:
        headers = {"x-api-key": API_KEY}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Setup any tweaks you want to apply to the flow
inputs = {"input":""}

with st.container():
    # Create a text input field where the user can enter a message
    message = st.text_input("Message", value="")
    # Create a button to send the message to the flow
    if st.button("Send"):
        # Send the message to the flow and get the response
        response = run_flow(inputs={"input": message}, flow_id=FLOW_ID, tweaks=TWEAKS)
        # Display the response to the user
        # st.write(response["output"])
        st.write(response['result']['output'])
