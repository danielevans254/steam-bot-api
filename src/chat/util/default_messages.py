import random

ai_assistant_welcome_messages = [
  "Welcome! I am your AI assistant. How can I assist you today?",
  "Hello! I am your AI assistant. How may I help you?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?",
  "Hello! I am your AI assistant. How can I assist you today?",
  "Greetings! I am your AI assistant. What can I do for you?",
  "Hi there! I am your AI assistant. How can I assist you?",
  "Welcome! I am your AI assistant. How may I be of service?",
  "Good to see you! I am your AI assistant. How can I help?",
  "Hey there! I am your AI assistant. What brings you here?",
  "Welcome aboard! I am your AI assistant. How can I assist?",
  "Hi! I am your AI assistant. How may I be of service?",
  "Nice to meet you! I am your AI assistant. How can I help?"
]

def random_welcome_message():
  random_welcome_message = random.choice(ai_assistant_welcome_messages)
  return random_welcome_message