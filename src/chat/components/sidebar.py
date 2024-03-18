import streamlit as st
from styles.messages.styles import user_message_style, assistant_message_style
from chat_history_list import chat_history_list
# FIXME: The kingparser already works as expected yet the selected option from this doesn't change the model, you can change it manually inside the king_parser file, this might have some caching issues, but it's not clear why it's not changing

def new_chat():
  if st.button("New chat"):
    st.session_state["chat_history"] = []
    st.session_state["chat_history"].append({"role": "assistant", "content": "Welcome new chat!"})
    return st.session_state["chat_history"]

def model_select():
  add_selectbox = st.selectbox(
    "What model would you like to use?",
    ("ChatGPT 3.5 Turbo", "Ollama 2 Chat", "Mistral", "Test", "Nous Hermes 2")
  )
  return add_selectbox

exported_model_value_select = model_select()

def parse_selected_model():
    if exported_model_value_select == "Test":
      st.write("You have selected Test")
      return "test"
    if exported_model_value_select == "ChatGPT 3.5 Turbo":
      st.write("You have selected ChatGPT 3.5 Turbo")
      return "openai"
    if exported_model_value_select == "Ollama 2 Chat":
      st.write("You have selected Ollama 2 Chat")
      return "llama2_chat"
    if exported_model_value_select == "Mistral":
      st.write("You have selected Mistral")
      return "mistral"

exported_add_selectbox_value = parse_selected_model()

def side_bar():
  with st.sidebar:
    st.subheader("Chatbot ☕️")
    new_chat()
    model_select()
    chat_history_list()
