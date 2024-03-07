import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt

LIST_OF_DEALS_URL = 'https://www.cheapshark.com/api/1.0/deals'

st.title('Steam Games, CheapShark API')

@st.cache_data
def fetch_list_of_deals(page_number):
    try:
        response = requests.get(LIST_OF_DEALS_URL, params={'pageSize': 60, 'pageNumber': page_number})
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
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
    st.write('Games currently on sale:')
    st.dataframe(df)

    deals_chart(df)
  except requests.RequestException as e:
    st.error(f'Failed to fetch game data: {e}')

# TODO: Create the stacked chart to display correctly
# TODO: Create a button to filter the data based on what the user want to see, for now the default i've set is 'savings',
def deals_chart(df, page_size=60, page_number=1):
  columns_to_keep = ['title', 'salePrice', 'normalPrice', 'savings']
  df = df[columns_to_keep]

  # Sort the dataframe by salePrice in descending order
  df = df.sort_values('savings', ascending=True)

  # FIXME: Not Working Apply pagination
  start_index = (page_number - 1) * page_size
  end_index = start_index + page_size
  df = df[start_index:end_index]

  chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('title', title='Product Title'),
    y=alt.Y('value:Q', title='Price'),
    color=alt.Color('variable:N', title='Price Type', sort=['savings', 'normalPrice', 'salePrice']),
    tooltip=[alt.Tooltip('salePrice'), alt.Tooltip('normalPrice'), alt.Tooltip('savings')]
  ).properties(
    title='Deals Chart',
  ).transform_fold(
    ['salePrice', 'normalPrice', 'savings'],
    as_=['variable', 'value']
  )
  st.altair_chart(chart, use_container_width=True)
  return df

load_list_of_deals()

