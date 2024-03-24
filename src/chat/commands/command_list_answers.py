import requests
import streamlit as st
import unittest

LIST_OF_DEALS_URL = 'https://www.cheapshark.com/api/1.0/deals'
LIST_OF_GAMES_URL = 'https://www.cheapshark.com/api/1.0/games'
LIST_OF_STORES_URL = 'https://www.cheapshark.com/api/1.0/stores'
ALERT_URL= 'https://www.cheapshark.com/api/1.0/alerts'

def is_command_list_answer(user_input):
    command_list = ["help", "clear", "deals", "games", "stores", "alerts"]
    return any(user_input.startswith(command) for command in command_list)

def is_command_list_answer_with_argument(user_input):
    command_list = ["help", "clear", "deals", "games", "stores", "alerts"]
    return any(user_input.startswith(command + ":") for command in command_list)

@st.cache_data
def fetch_deals_list():
    try:
        response = requests.get(LIST_OF_DEALS_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

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
  try:
    response = requests.get(LIST_OF_STORES_URL)
    response.raise_for_status()
    stores = response.json()
    return stores

  except requests.RequestException as e:
    return None

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

def parse_deals_list(deals):
  important_columns = ["title", "salePrice", "isOnSale", "steamRatingText", "steamRatingPercent", "steamRatingCount"]
  parsed_deals = []
  for deal in deals:
    parsed_deal = {column: deal[column] for column in important_columns if column in deal}
    parsed_deals.append(parsed_deal)
  return parsed_deals

def command_list_answer(user_input):
  if is_command_list_answer(user_input):
    answers = {
      "help": "If you need help, type `help`.",
      "clear": "If you want to clear the chat, type `clear`.",
      "deals": parse_deals_list(fetch_deals_list()),
      "games": fetch_games_list(),
      "stores": fetch_stores_list(),
      "alerts": fetch_alerts_list(),
    }
    return answers.get(user_input)
  else:
    return None

def command_list_answer_with_argument(user_input):
  if is_command_list_answer_with_argument(user_input):
    answers = {
      "help": "If you need help, type `help`.",
      "clear": "If you want to clear the chat, type `clear`.",
      "deals": parse_deals_list(fetch_deals_list()),
      "games": fetch_games_list(),
      "stores": fetch_stores_list(),
      "alerts": fetch_alerts_list(),
    }
    return answers.get(user_input)
  else:
    return None