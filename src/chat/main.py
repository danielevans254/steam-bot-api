import streamlit as st
import streamlit.components.v1 as components
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from streamlit_extras.tags import tagger_component
from commands.command_list import show_command_list
from styles.messages.styles import user_message_style, assistant_message_style
from util.default_messages import random_welcome_message
from models.king_parser import king_parser
from models.llava_model import llava_response
from commands.command_list_answers import command_list_answer, is_command_list_answer, is_command_list_answer_with_argument
from util.db import create_new_chat_session, database_connection, insert_data_chat_content, fetch_all_chat_history_db, fetch_last_chat_session_id, fetch_selected_id_chat_history_db, create_schema
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
# TODO: Add memory and context since we can switch between different chats at a time, and we can have multiple chats at a time
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

def chat_history_list():
  chats = fetch_all_chat_history_db() or []
  if chats == []:
    create_new_chat_session()
    return
  chat_ids = [chat[0] for chat in chats][::-1]
  chat_labels = [chat[1] for chat in chats][::-1]
  selected_chat_label = st.sidebar.radio("Chat history", options=chat_labels, index=0)
  selected_chat_id = chat_ids[chat_labels.index(selected_chat_label)]
  print(selected_chat_id, "selected_chat_id[]")
  return selected_chat_id

def chosen_chat_history(selected_chat_id):
  chats = fetch_all_chat_history_db() or []
  chat = [chat for chat in chats if chat[0] == selected_chat_id]
  print(chat, "chat[]")
  return chat

def model_chat(selected_model, chat_session_id):
  st.title("Chat with our Assistant")

  if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = fetch_last_chat_session_id()

  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

  if not st.session_state["chat_history"]:
    st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})

  user_input = st.chat_input("Type a message..")
  if user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
# TODO: The commands now work and are stored in the database upon execution, however these commands responds with api responses that are very long so we need to use RAG to generate a response for these commands, whilst using a vector database to store the chopped up responses
    if is_command_list_answer_with_argument(user_input):
      command, argument = user_input.split(":")
      command = command.strip()
      argument = argument.strip()
      command_actions = {
        "deals": lambda arg: f"Processing 'deals' command with argument: {arg}",
        "games": lambda arg: f"Processing 'games' command with argument: {arg}",
        "stores": lambda arg: f"Processing 'stores' command with argument: {arg}",
        "alerts": lambda arg: f"Processing 'alerts' command with argument: {arg}"
      }
      if command in command_actions:
        response = command_actions[command](argument)
        response_str = str(response)
        print(response, "  response[][]")
        selected_model = (f"Command: {command} with argument: {argument}")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_data_chat_content(user_input, response_str, selected_model, created_at, chat_session_id)
        st.session_state["chat_history"].append({"role": "assistant", "content": response_str})
    elif is_command_list_answer(user_input):
      response = command_list_answer(user_input)
      response_str = json.dumps(response)
      print(response_str, "  response[][][][]")
      selected_model = (f"Command: {user_input}")
      created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      insert_data_chat_content(user_input, response_str, selected_model, created_at, chat_session_id)
      st.session_state["chat_history"].append({"role": "assistant", "content": response_str})
    else:
      with st.spinner("Processing request..."):
        if selected_model == "llava":
          response = llava_response(user_input)
        else:
          response = king_parser(user_input, selected_model)
        if response is not None:
          created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          insert_data_chat_content(user_input, response, selected_model, created_at, chat_session_id)
          st.session_state["chat_history"].append({"role": "assistant", "content": response})
        else:
          st.warning("The response is not yet available. Please wait...")

def model_description(model_selected):
  model_description = {
    "openai": "This model is powered by OpenAI's ChatGPT 3.5 Turbo. It is a powerful conversational model that can generate human-like text.",
    "llama2_chat": "This model is powered by Llama 2 Chat. It is a conversational model that can generate human-like text.",
    "mistral": "This model is powered by Mistral. It is a conversational model that can generate human-like text.",
    "test": "This is a test model.",
    "nous_hermes2": "This model is powered by Nous Hermes 2. It is a conversational model that can generate human-like text.",
    "llava": "This model is powered by Llava. It is a conversational model that can generate human-like text."
  }
  st.write(model_description[model_selected])

def model_badge(model_selected):
  tagger_component(
    "Model Used:",
    [model_selected],
    color_name=["blue"],
  )

def command_list_badge(command):
  tagger_component(
    "Command Used:",
    [command],
    color_name=["red"],
  )
def argument_list_badge(argument):
  tagger_component(
    "Argument Used:",
    [argument],
    color_name=["lightblue"],
  )

# TODO: Make the badges for the commands and arguments different
def display_chat_history(selected_chat_id):
  chat_history, chat_session = fetch_selected_id_chat_history_db(selected_chat_id)
  for message in chat_history:
    user_input = message[1]
    ai_response = message[2]
    model_used = message[3]
    with st.chat_message("user"):
      st.write(user_input)
    with st.chat_message("assistant"):
      st.write(ai_response)
      model_badge(model_used)

# FIXME: Fix llava image path issue
def main():
  set_page_config()
  database_connection()
  create_schema()

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
    if add_selectbox == "Llava":
      uploaded_file = st.sidebar.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
      if uploaded_file is not None:
        image_dir = "uploaded_images"
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, uploaded_file.name)
        print(image_path)
        with open(image_path, "wb") as f:
          f.write(uploaded_file.getbuffer())
        print(image_path)
      selected_model = "llava"
    else:
      selected_model = model_options[add_selectbox]

    selected_chat_id = chat_history_list()

  show_command_list()
  model_chat(selected_model, selected_chat_id)
  display_chat_history(selected_chat_id)

if __name__ == "__main__":
  main()