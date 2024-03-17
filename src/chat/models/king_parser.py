from models.openai_model import openAI_response
from models.test_model import test_response
from components.sidebar import exported_select_model

# TODO: This should be taken from the sidebar component for the select box, but for now, we'll hardcode it.
exported_select_model = "mistral"
def king_parser(user_input):
  print(exported_select_model, "exported_select_model")
  if exported_select_model == "openai":
    print("openai")
    return openAI_response(user_input)
  elif exported_select_model == "test":
    print("test")
    return test_response(user_input)
  elif exported_select_model == "ollama":
    print("ollama")
    return "ollama"
  elif exported_select_model == "mistral":
    print("mistral")
    return "mistral"
  else:
    return f"The {exported_select_model} model is not supported yet.😞"
