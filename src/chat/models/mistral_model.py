from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

llm = Ollama(
    model="mistral", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

def mistral_response(user_input):
    response = llm(user_input)
    return response
