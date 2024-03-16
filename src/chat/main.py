import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
load_dotenv()

from commands.command_list import show_command_list
from components.sidebar import select_model
from chat_bot import chat_bot
from web_pages.main_layout import page_setup

def main():
  page_setup()
  show_command_list()
  select_model()
  chat_bot()

if __name__ == "__main__":
  main()


