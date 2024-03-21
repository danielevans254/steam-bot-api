from models.openai_model import openAI_response
from models.test_model import test_response
from models.ollama_2_model import llama2_chat_response
from models.mistral_model import mistral_response
from models.nous_hermes2 import nous_hermes2_response

# TODO: This should be taken from the sidebar component for the select box, but for now, we'll hardcode it.

def king_parser(user_input, selected_model):
  print(selected_model, "exported_select_model")
  if selected_model == "openai":
    print("openai")
    return openAI_response(user_input)
  elif selected_model == "test":
    print("test")
    return test_response(user_input)
  elif selected_model == "llama2_chat":
    print("llama2_chat")
    return llama2_chat_response(user_input)
  elif selected_model == "mistral":
    print("mistral")
    return mistral_response(user_input)
  elif selected_model == "nous_hermes2":
    return nous_hermes2_response(user_input)
  else:
    return f"The {selected_model} model is not supported yet.😞"
