from dotenv import load_dotenv
load_dotenv()
import openai
import os
openai.openai_api_key = os.getenv("OPENAI_API_KEY")

def openAI_response(user_input):
  assistant_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": user_input}
    ]
  )

  if assistant_response.choices and len(assistant_response.choices) > 0:
    assistant_response_text = assistant_response.choices[0]['message']['content']
  else:
    assistant_response_text = ""

  return assistant_response_text




