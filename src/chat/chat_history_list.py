import streamlit as st
import datetime

# Sample data
previous_chat = [
    "2022-01-01 10:00:00",
    "2022-01-03 10:00:00",
]

def chat_history_list():
  st.radio("Chat history", previous_chat)


