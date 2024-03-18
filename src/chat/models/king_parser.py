from models.openai_model import openAI_response
from models.test_model import test_response
from models.ollama_2_model import ollama_response
from models.mistral_model import mistral_response
from components.sidebar import exported_add_selectbox_value

# TODO: This should be taken from the sidebar component for the select box, but for now, we'll hardcode it.
exported_add_selectbox_value = "llama2_chat"
def king_parser(user_input):
  print(exported_add_selectbox_value, "exported_select_model")
  if exported_add_selectbox_value == "openai":
    print("openai")
    return openAI_response(user_input)
  elif exported_add_selectbox_value == "test":
    print("test")
    return test_response(user_input)
  elif exported_add_selectbox_value == "llama2_chat":
    print("llama2_chat")
    return ollama_response(user_input)
  elif exported_add_selectbox_value == "mistral":
    print("mistral")
    return mistral_response(user_input)
  else:
    return f"The {exported_add_selectbox_value} model is not supported yet.😞"
