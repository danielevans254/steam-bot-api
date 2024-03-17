import streamlit as st
import streamlit.components.v1 as components

from styles.messages.styles import user_message_style, assistant_message_style
from utils.default_messages import random_welcome_message
from models.king_parser import king_parser

def model_chat():
  st.title("Chat with our Assistant")

  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

  if not st.session_state["chat_history"]:
      st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})

  user_input = st.text_input("Enter your message:")
  if user_input.strip() == "":
    st.warning("Please enter a message.")
  else:
    if st.button("Send"):
      st.session_state["chat_history"].append({"role": "user", "content": user_input})
      # TODO: This should be based on which model is selected openai for now
      st.session_state["chat_history"].append({"role": "assistant", "content": king_parser(user_input)})
      user_input = ""
  return user_input

def chat_history():
  for message in st.session_state["chat_history"]:
    if message["role"] == "user":
      st.write(f'<div style="display: flex; justify-content: flex-start; word-wrap: break-word;"><div style="{user_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
      st.write(f'<div style="display: flex; justify-content: flex-end; word-wrap: break-word;"><div style="{assistant_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)
