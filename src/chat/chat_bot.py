import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
load_dotenv()
import string
import random
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Chatbot: Steam Games & CheapShark API",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and introductory text
st.title("Chatbot ☕️")
st.write("Welcome to the chatbot! Ask me anything about Steam Games, CheapShark API, and I'll try to help you out.")

# User instructions
def command_lists():
  st.write("To get started, type in the command you want to execute.")
  st.write("For example, type `list of deals` to get the list of deals.")
  st.write("If you need help, type `help`.")
  st.write("If you want to exit, type `exit`.")
  st.write("If you want to clear the chat, type `clear`.")
  st.write("If you want to see the list of commands, type `commands`.")
  st.write("If you want to see the list of deals, type `deals`.")
  st.write("If you want to see the list of games, type `games`.")
  st.write("If you want to see the list of stores, type `stores`.")
  st.write("If you want to see the list of alerts, type `alerts`.")
  if st.button("Close"):
    st.stop()

# Button to show commands in a modal
if st.button("Show Commands"):
  command_lists()

# Define message styles
user_message_style = """
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 70%;
  font-family: Arial, sans-serif;
  font-size: 16px;
  color: #333;
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 10px;
  padding-bottom: 10px;
  font-weight: bold;
"""

assistant_message_style = """
  background-color: #d3eaf5;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  max-width: 70%;
  align-self: flex-end;
  font-family: Arial, sans-serif;
  font-size: 16px;
  color: #333;
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 10px;
  padding-bottom: 10px;
  font-weight: bold;
"""
# FIXME: When the user successfully sends a message clear the text input field
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input
user_input = st.text_input("Enter your message:")

if user_input:
    # Append user input to chat history
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

    # Clear user input
    user_input = ""

    # Clear user input
    user_input = ""

# Display chat history with improved styling
for message in st.session_state["chat_history"]:
    if message["role"] == "user":
        st.write(f'<div style="display: flex; justify-content: flex-start;"><div style="{user_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.write(f'<div style="display: flex; justify-content: flex-end;"><div style="{assistant_message_style}">{message["content"]}</div></div>', unsafe_allow_html=True)

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "What model would like to use?",
    ("ChatGPT 3.5 Turbo", "Ollama 2 Chat", "Mistral", "Test")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

