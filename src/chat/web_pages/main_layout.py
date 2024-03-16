import streamlit as st

def page_setup():
  st.set_page_config(
      page_title="Chatbot: Steam Games & CheapShark API",
      page_icon="🎮",
      layout="wide",
      initial_sidebar_state="expanded"
  )
  st.write("Welcome to the chatbot! Ask me anything about Steam Games, CheapShark API, and I'll try to help you out.")