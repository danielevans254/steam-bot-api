from dotenv import load_dotenv
load_dotenv()
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama2:chat", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

def llama2_chat_response(user_input):
    response = llm(user_input)
    return response
