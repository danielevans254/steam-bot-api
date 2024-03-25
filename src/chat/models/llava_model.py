from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
# TODO: This should include the file path of the uploaded file
def llava_response(user_input):
  llm = Ollama(
    model="llava",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
  )
  response = llm(user_input)
  return response
