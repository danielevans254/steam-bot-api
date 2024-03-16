import streamlit as st

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
  return

def show_command_list():
  if st.button("Show Commands"):
    command_lists()