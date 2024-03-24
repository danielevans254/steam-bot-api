import os
import streamlit as st
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama

def llava_response(user_input):
  llm = Ollama(
    model="llava",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
  )
  response = llm(user_input)
  return response
