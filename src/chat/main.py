import random
import string
import streamlit as st
import streamlit.components.v1 as components
import mysql.connector
import os
import asyncio

from commands.command_list import show_command_list
from styles.messages.styles import user_message_style, assistant_message_style
from utils.default_messages import random_welcome_message
from models.king_parser import king_parser
from commands.command_list_answers import command_list_answer, is_command_list_answer
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime


def database_connection():
    cnx = None
    try:
        cnx = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port = os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        if cnx.is_connected():
            print('Connected to MySQL database')
        else:
            print('Connection failed')

    except mysql.connector.Error as err:
        print(f'Error: {err}')
    finally:
        pass

    return cnx

def create_table():
    cnx = None
    cursor = None
    try:
        cnx = database_connection()

        cursor = cnx.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS chat_history (id INT AUTO_INCREMENT PRIMARY KEY, content TEXT, response TEXT, model TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    except mysql.connector.Error as err:
        print(f'Error: {err}')

    finally:
        if cursor is not None:
            cursor.close()
        if cnx is not None and cnx.is_connected():
            cnx.close()
            print('Database connection closed[TABLE CREATED].')

def generate_random_string(length):
  letters = string.ascii_letters + string.digits
  return ''.join(random.choice(letters) for _ in range(length))

def insert_data(content, response, model,created_at,chat_id):
  cnx = None
  cursor = None
  try:
    cnx = database_connection()
    chat_id = generate_random_string(30)

    cursor = cnx.cursor()
    cursor.execute("INSERT INTO chat_history (content, response, model, created_at,chat_id) VALUES (%s, %s, %s, %s,%s)", (content, response, model,created_at,chat_id))
    cnx.commit()

    print(f"Inserted data: content={content}, response={response}, model={model}, created_at={created_at}, chat_id={chat_id}")

  except mysql.connector.Error as err:
    print(f'Error: {err}')

  finally:
    if cursor is not None:
      cursor.close()
    if cnx is not None and cnx.is_connected():
      cnx.close()
      print('Database connection closed.[INSERTED DATA]')


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
def chat_history_list():
  previous_chat = [
    "2022-01-01 10:00:00",
    "2022-01-03 10:00:00",
  ]
  st.sidebar.radio("Chat history", previous_chat)

def clear_chat_session_history():
  if st.button("Clear chat history"):
    st.session_state["chat_history"] = []
    st.success("Chat history cleared.")

def model_chat(selected_model):
  st.title("Chat with our Assistant")

  if "chat_id" not in st.session_state:
    st.session_state["chat_id"] = generate_random_string(30)
  chat_id = st.session_state["chat_id"]

  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

  if not st.session_state["chat_history"]:
    st.session_state["chat_history"].append({"role": "assistant", "content": random_welcome_message()})

  if user_input := st.chat_input("Type a message.."):
    if is_command_list_answer(user_input):
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.session_state["chat_history"].append({"role": "assistant", "content": command_list_answer(user_input)})
        user_input = ""
    else:
      with st.spinner("Processing request..."):
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        response = king_parser(user_input, selected_model)
        if response is not None:
          st.session_state["chat_history"].append({"role": "assistant", "content": response})
          created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          insert_data(user_input, response, selected_model, created_at,chat_id)
        else:
          st.warning("The response is not yet available. Please wait...")
      user_input = ""

# TODO: Stream the chat history
def display_chat_history():
  for message in st.session_state["chat_history"]:
      with st.chat_message(message["role"]):
        st.write(message["content"])

def main():
  set_page_config()

  with st.sidebar:
    st.subheader("Chatbot ☕️")
    if st.button("New chat"):
      st.session_state["chat_history"] = []
      st.session_state["chat_history"].append({"role": "assistant", "content": "Welcome new chat!"})

    add_selectbox = st.selectbox(
      "What model would you like to use?",
      ("ChatGPT 3.5 Turbo", "Ollama 2 Chat", "Mistral", "Test", "Nous Hermes 2")
    )
    chat_history_list()

  if add_selectbox == "Nous Hermes 2":
    st.write("You have selected Nous Hermes 2")
    selected_model = "nous_hermes2"
  if add_selectbox == "Test":
    st.write("You have selected Test")
    selected_model = "test"
  if add_selectbox == "ChatGPT 3.5 Turbo":
    st.write("You have selected ChatGPT 3.5 Turbo")
    selected_model = "openai"
  if add_selectbox == "Ollama 2 Chat":
    st.write("You have selected Ollama 2 Chat")
    selected_model = "llama2_chat"
  if add_selectbox == "Mistral":
    st.write("You have selected Mistral")
    selected_model = "mistral"
  show_command_list()
  model_chat(selected_model)
  clear_chat_session_history()
  display_chat_history()

if __name__ == "__main__":
  main()