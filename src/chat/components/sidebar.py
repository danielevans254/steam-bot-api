import streamlit as st

# FIXME: The kingparser already works as expected yet the selected option from this doesn't change the model, you can change it manually inside the king_parser file, this might have some caching issues, but it's not clear why it's not changing
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
      return "test"
    if add_selectbox == "ChatGPT 3.5 Turbo":
      st.write("You have selected ChatGPT 3.5 Turbo")
      return "openai"
    if add_selectbox == "Ollama 2 Chat":
      st.write("You have selected Ollama 2 Chat")
      return "ollama"
    if add_selectbox == "Mistral":
      st.write("You have selected Mistral")
      return "mistral"

    st.radio(
      "Choose a shipping method",
      ("Standard (5-15 days)", "Express (2-5 days)")
    )

exported_select_model = select_model()