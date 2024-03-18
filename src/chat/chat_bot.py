import streamlit as st
import streamlit.components.v1 as components

from styles.messages.styles import user_message_style, assistant_message_style
from utils.default_messages import random_welcome_message
from models.king_parser import king_parser
from commands.command_list_answers import command_list_answer, is_command_list_answer
def model_chat():
  st.title("Chat with our Assistant")

  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

  if not st.session_state["chat_history"]:
      st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})

  user_input = st.text_input("Enter your message:")
  if user_input.strip() == "":
    st.warning("Please enter a message.")
  elif len(user_input) > 500:
    st.error("Your message is too long. Please keep it under 500 characters.")
  elif is_command_list_answer(user_input):
    if st.button("Send the message"):
      st.session_state["chat_history"].append({"role": "user", "content": user_input})
      st.session_state["chat_history"].append({"role": "assistant", "content": command_list_answer(user_input)})
    user_input = ""
  else:
    if st.button("Send the message"):
      with st.spinner("Processing request..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.session_state["chat_history"].append({"role": "assistant", "content": king_parser(user_input)})
    user_input = ""
  return user_input

def chat_history():
  for message in st.session_state["chat_history"]:
    if message["role"] == "user":
      st.write(f'<div style="display: flex; justify-content: flex-start; word-wrap: break-word;"><div style="{user_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
      st.write(f'<div style="display: flex; justify-content: flex-end; word-wrap: break-word;"><div style="{assistant_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)

def clear_chat_history():
  if st.button("Clear chat history"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared.")