import streamlit as st
import streamlit.components.v1 as components
import os

from commands.command_list import show_command_list
from styles.messages.styles import user_message_style, assistant_message_style
from utils.default_messages import random_welcome_message
from models.king_parser import king_parser
from models.llava_model import llava_response
from commands.command_list_answers import command_list_answer, is_command_list_answer,is_command_list_answer_with_argument
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from util.db import create_new_chat_session, database_connection, create_table, insert_data_chat_content, fetch__all_chat_history_db,fetch_last_chat_session_id

def set_page_config():
  st.set_page_config(
    page_title="Chatbot: Steam Games & CheapShark API",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
  )

def show_welcome_message():
  st.write("Welcome to the chatbot! Ask me anything about Steam Games, CheapShark API, and I'll try to help you out.")
  st.write("For list of commands click `show commands`")

# TODO: Fetch the chat history from the database
# TODO: Display the chat session, replace the current chat session with the fetched chat history
# FIXME: When a prompt is currently being processed and the user clicks the radio button to select a different chat history, the chat history currently made is not displayed
def chat_history_list():
    chats = fetch__all_chat_history_db()
    if chats is None:
        chats = []
    chat_ids = [chat[0] for chat in chats]  # Assuming chat[0] is the chat_session_id
    selected_chat_id = st.sidebar.radio("Chat history", options=chat_ids)
    return selected_chat_id

def chosen_chat_history(selected_chat_id):
    chats = fetch__all_chat_history_db()
    if chats is None:
        chats = []
    chat = [chat for chat in chats if chat[0] == selected_chat_id]
    return chat

def model_chat(selected_model):
  st.title("Chat with our Assistant")

  if "chat_id" not in st.session_state:
      st.session_state["chat_id"] = fetch_last_chat_session_id()
  chat_id = st.session_state["chat_id"]

  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

  if not st.session_state["chat_history"]:
    st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})

  if user_input := st.chat_input("Type a message.."):
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    if is_command_list_answer_with_argument(user_input):
      command, argument = user_input.split(":")
      command = command.strip()
      argument = argument.strip()
      command_actions = {
        "deals": lambda arg: print(f"Processing 'deals' command with argument: {arg}"),
        "games": lambda arg: print(f"Processing 'games' command with argument: {arg}"),
        "stores": lambda arg: print(f"Processing 'stores' command with argument: {arg}"),
        "alerts": lambda arg: print(f"Processing 'alerts' command with argument: {arg}")
      }
      if command in command_actions:
        command_actions[command](argument)
        st.session_state["chat_history"].append({"role": "assistant", "content": f"Processing '{command}' command with argument: {argument}"})
    elif is_command_list_answer(user_input):
      st.session_state["chat_history"].append({"role": "assistant", "content": command_list_answer(user_input)})
    elif selected_model == "llava":
      response = llava_response(user_input)
      created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      insert_data_chat_content(user_input, response, selected_model, created_at, chat_id)
      st.session_state["chat_history"].append({"role": "assistant", "content": response})
    else:
      with st.spinner("Processing request..."):
        response = king_parser(user_input, selected_model)
        if response is not None:
          created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          insert_data_chat_content(user_input, response, selected_model, created_at, chat_id)
          st.session_state["chat_history"].append({"role": "assistant", "content": response})
        else:
          st.warning("The response is not yet available. Please wait...")
    user_input = ""

# TODO: Stream the chat history
def display_chat_history():
  chat_history = st.session_state.get("chat_history", [])
  for message in chat_history:
    with st.chat_message(message["role"]):
      st.write(message["content"])

def main():
  set_page_config()
  database_connection()
  create_table()

  with st.sidebar:
    st.subheader("Chatbot 💻")
    if st.button("New chat"):
        st.session_state["chat_history"] = []
        st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})
        st.success("New chat session started.")
        st.session_state["chat_id"] = create_new_chat_session()

    model_options = {
      "ChatGPT 3.5 Turbo": "openai",
      "Ollama 2 Chat": "llama2_chat",
      "Mistral": "mistral",
      "Test": "test",
      "Nous Hermes 2": "nous_hermes2",
      "Llava": "llava"
    }
    add_selectbox = st.selectbox("What model would you like to use?", list(model_options.keys()))
# TODO: Fix the filepath issue, and make it so that i can pass in the image to the llava model, using the uploaded file
    if add_selectbox == "Llava":
      uploaded_file = st.sidebar.file_uploader("Upload File", type=["png", "jpg", "jpeg"])
      if uploaded_file is not None:
        image_dir = "uploaded_images"
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, uploaded_file.name)
        with open(image_path, "wb") as f:
          f.write(uploaded_file.getbuffer())
        print(image_path)
      selected_model = "llava"
    else:
      st.write(f"You have selected {add_selectbox}")
      selected_model = model_options[add_selectbox]

    chat_history_list()
  show_command_list()
  model_chat(selected_model)
  display_chat_history()

if __name__ == "__main__":
  main()