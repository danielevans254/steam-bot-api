import streamlit as st
import streamlit.components.v1 as components

from commands.command_list import show_command_list
from components.sidebar import side_bar
from chat_bot import model_chat, chat_history, clear_chat_history

st.set_page_config(
page_title="Chatbot: Steam Games & CheapShark API",
page_icon="🎮",
layout="wide",
initial_sidebar_state="expanded"
)
st.write("Welcome to the chatbot! Ask me anything about Steam Games, CheapShark API, and I'll try to help you out.")
st.write("For list of commands click `show commands`")

def main():
  side_bar()
  show_command_list()
  model_chat()
  clear_chat_history()
  chat_history()

main()