def is_command_list_answer(user_input):
  if user_input == "help":
    return True
  elif user_input == "clear":
    return True
  elif user_input == "deals":
    return True
  elif user_input == "games":
    return True
  elif user_input == "stores":
    return True
  elif user_input == "alerts":
    return True
  return False

def command_list_answer(user_input):
  if is_command_list_answer(user_input):
    answers = {
      "help": "If you need help, type `help`.",
      "clear": "If you want to clear the chat, type `clear`.",
      "deals": "If you want to see the list of deals, type `deals`.",
      "games": "If you want to see the list of games, type `games`.",
      "stores": "If you want to see the list of stores, type `stores`.",
      "alerts": "If you want to see the list of alerts, type `alerts`."
    }
    return answers.get(user_input)
  else:
    return None
