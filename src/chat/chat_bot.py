import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
load_dotenv()
import openai

from styles.messages.styles import user_message_style, assistant_message_style
import random
from utils.default_messages import random_welcome_message
openai.openai_api_key = os.getenv("OPENAI_API_KEY")

def chat_bot():
  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

  if not st.session_state["chat_history"]:
      st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})

  user_input = st.text_input("Enter your message:")
  if user_input == "":
    st.warning("Please enter a message.")
  if st.button("Send") and user_input != "":
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    def get_assistant_response(user_input):
      assistant_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": user_input}
        ]
      )

      if assistant_response.choices and len(assistant_response.choices) > 0:
        assistant_response_text = assistant_response.choices[0]['message']['content']
      else:
        assistant_response_text = ""

      return assistant_response_text

    # Append assistant response to chat history
    st.session_state["chat_history"].append({"role": "assistant", "content": get_assistant_response(user_input)})

    user_input = ""

  # Display chat history with improved styling
  for message in st.session_state["chat_history"]:
    if message["role"] == "user":
      st.write(f'<div style="display: flex; justify-content: flex-start;"><div style="{user_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
      st.write(f'<div style="display: flex; justify-content: flex-end;"><div style="{assistant_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)
