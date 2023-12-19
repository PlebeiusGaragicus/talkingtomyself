from langflow import load_flow_from_json

TWEAKS = {
  "OpenAIConversationalAgent-0HJdd": {
    "model_name": "gpt-4-1106-preview"
  },
  "PythonFunctionTool-uJfF3": {}
}
flow = load_flow_from_json("GPT-CLONE!.json", tweaks=TWEAKS)

# say something:
i = input("input")


# Now you can use it like any chain
inputs = {"input":f"{i}"}
flow(inputs)
