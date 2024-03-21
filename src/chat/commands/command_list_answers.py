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

def fetch_deals_list():
  return [
    {
      "dealID": "12345",
      "title": "Game Title",
      "salePrice": "10.00",
      "normalPrice": "20.00",
      "savings": "50%",
      "storeID": "1",
      "gameID": "1",
      "isOnSale": "1"
    },
    {
      "dealID": "67890",
      "title": "Another Game Title",
      "salePrice": "15.00",
      "normalPrice": "30.00",
      "savings": "50%",
      "storeID": "2",
      "gameID": "2",
      "isOnSale": "1"
    }
  ]

def fetch_games_list():
  return [
    {
      "gameID": "1",
      "title": "Game Title",
      "steamAppID": "12345",
      "external": "1"
    },
    {
      "gameID": "2",
      "title": "Another Game Title",
      "steamAppID": "67890",
      "external": "0"
    }
  ]

def fetch_stores_list():
  return [
    {
      "storeID": "1",
      "storeName": "Steam",
      "isActive": "1"
    },
    {
      "storeID": "2",
      "storeName": "Epic Games",
      "isActive": "1"
    }
  ]

def fetch_alerts_list():
  return [
    {
      "alertID": "1",
      "gameID": "1",
      "price": "10.00",
      "email": "example-email@gmail.com"
    },
    {
      "alertID": "2",
      "gameID": "2",
      "price": "15.00",
      "email": "test_email@yahoo.com"
    }
  ]

def command_list_answer(user_input):
  if is_command_list_answer(user_input):
    answers = {
      "help": "If you need help, type `help`.",
      "clear": "If you want to clear the chat, type `clear`.",
      "deals": fetch_deals_list(),
      "games": fetch_games_list(),
      "stores": fetch_stores_list(),
      "alerts": fetch_alerts_list(),
    }
    return answers.get(user_input)
  else:
    return None
