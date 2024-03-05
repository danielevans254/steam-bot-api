import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

LIST_OF_DEALS_URL = 'https://www.cheapshark.com/api/1.0/deals'

st.title('Steam Games')

# TODO: Add different filters, for steamRatingText, isOnSale, (based on user input)
# TODO: Add the query params, to be able to filter the data, based on user input
# TODO: Based on the documentation the default is only 60 games, so we need to fetch all the games, although the api might rate limit me. after fetching and being rate limited then it shows the data 3000 might be the max based on testing it out
# NOTE: This should be fetching 3060 games, but it only fetches 3000, there might be a limit for the table? not sure through, might be on streamlit's end
@st.cache_data
def fetch_list_of_deals(page_number):
    try:
        df = pd.DataFrame()
        response = requests.get(LIST_OF_DEALS_URL, params={'pageSize': 60, 'pageNumber': page_number})
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        st.error(f'Returned {page_number} pages.')
        return None

def load_list_of_deals():
  try:
    df = pd.DataFrame()
    page_number = 1
    while True:
      game_data = fetch_list_of_deals(page_number)
      if not game_data:
        break
      df = pd.concat([df, pd.DataFrame(game_data)], ignore_index=True)
      page_number += 1

    # Only keeping the columns that are important
    columns_to_keep = ['title', 'storeID', 'gameID', 'salePrice', 'normalPrice', 'savings','metacriticScore', 'steamRatingText', 'steamRatingPercent', 'steamRatingCount','steamAppID', 'dealRating']
    df = df[columns_to_keep]
    st.write('Games on sale:')
    st.dataframe(df)

    deals_chart(df)
  except requests.RequestException as e:
    st.error(f'Failed to fetch game data: {e}')

def deals_chart(df):
    print(df)
    # Calculate price difference
    # Create a simplified DataFrame for plotting
    columns_to_keep = ['title', 'salePrice', 'normalPrice', 'savings']
    df = df[columns_to_keep]
    chart_data = pd.DataFrame(df, columns=['salePrice', 'normalPrice', 'savings'])
    # Plot the bar chart
    st.bar_chart(chart_data)
    return df

load_list_of_deals()

