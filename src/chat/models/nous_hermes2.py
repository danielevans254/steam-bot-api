from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

llm = Ollama(
    model="nous-hermes2", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

def nous_hermes2_response(user_input):
    response = llm(user_input)
    return response
