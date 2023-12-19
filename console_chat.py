import os
import dotenv

dotenv.load_dotenv()

import requests
from typing import Optional


BASE_API_URL = os.getenv("BASE_API_URL")
FLOW_ID = os.getenv("FLOW_ID")

TWEAKS = {
  "OpenAIConversationalAgent-0HJdd": {},
  "PythonFunctionTool-uJfF3": {}
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
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
    # if api_key:
        # headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Setup any tweaks you want to apply to the flow
inputs = input("input:")
inputs = {"input":f"{inputs}"}

print(run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS))

# say something:
# i = input("input")


# Now you can use it like any chain
# inputs = {"input":f"{i}"}
# flow(inputs)
