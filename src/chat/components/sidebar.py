import streamlit as st

def select_model():
  with st.sidebar:
    st.title("Chatbot ☕️")
    add_selectbox = st.selectbox(
      "What model would you like to use?",
      ("ChatGPT 3.5 Turbo", "Ollama 2 Chat", "Mistral", "Test")
    )
    st.button("New Chat")

    # TODO: Make this reusable and add the ability to change the model
    if add_selectbox == "Test":
      st.write("You have selected Test")
    if add_selectbox == "ChatGPT 3.5 Turbo":
      st.write("You have selected ChatGPT 3.5 Turbo")
    if add_selectbox == "Ollama 2 Chat":
      st.write("You have selected Ollama 2 Chat")
    if add_selectbox == "Mistral":
      st.write("You have selected Mistral")

    st.radio(
      "Choose a shipping method",
      ("Standard (5-15 days)", "Express (2-5 days)")
    )
