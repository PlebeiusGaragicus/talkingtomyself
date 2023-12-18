import os
import dotenv

dotenv.load_dotenv()

from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    # https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})