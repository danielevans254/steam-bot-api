import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt
import re

LIST_OF_DEALS_URL = 'https://www.cheapshark.com/api/1.0/deals'
LIST_OF_GAMES_URL = 'https://www.cheapshark.com/api/1.0/games'
LIST_OF_STORES_URL = 'https://www.cheapshark.com/api/1.0/stores'
ALERT_URL= 'https://www.cheapshark.com/api/1.0/alerts'

st.title('Steam Games, CheapShark API')
tab1, tab2, tab3, tab4 = st.tabs(["Deals", "Games", "Stores", "Alerts"])

def validate_email(email):
  pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
  return re.match(pattern, email)

with tab1:
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
        game_df = pd.DataFrame(game_data)
        df = pd.concat([df, game_df], ignore_index=True)
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
  def deals_chart(df):
      columns_to_keep = ['title', 'salePrice', 'normalPrice', 'savings']
      df = df[columns_to_keep]

      for column in ['salePrice', 'normalPrice', 'savings']:
          df[column] = df[column].astype(float)

      df_normal = df.nlargest(30, 'normalPrice')
      chart_normal_price = alt.Chart(df_normal).mark_bar().encode(
          x=alt.X('normalPrice:Q', title='Normal Price', sort='descending'),
          y=alt.Y('title', title='Product Title', sort='-x'),
          tooltip=[alt.Tooltip('normalPrice', format='$,.2f')]
      ).properties(
          title='Normal Price Chart',
      )
      st.altair_chart(chart_normal_price, use_container_width=True)

      df_sale = df.nlargest(30, 'salePrice')
      chart_sale_price = alt.Chart(df_sale).mark_bar().encode(
          x=alt.X('salePrice:Q', title='Sale Price', sort='descending'),
          y=alt.Y('title', title='Product Title', sort='-x'),
          tooltip=[alt.Tooltip('salePrice', format='$,.2f')]
      ).properties(
          title='Sale Price Chart',
      )
      st.altair_chart(chart_sale_price, use_container_width=True)

      df_savings = df.nlargest(30, 'savings')
      chart_savings = alt.Chart(df_savings).mark_bar().encode(
          x=alt.X('savings:Q', title='Savings', sort='descending'),
          y=alt.Y('title', title='Product Title', sort='-x'),
          tooltip=[alt.Tooltip('savings', format='$,.2f')]
      ).properties(
          title='Savings Chart',
      )
      st.altair_chart(chart_savings, use_container_width=True)

      return df

  load_list_of_deals()


with tab2:
  def games_list(external, steamAppID):
      st.write('Search for a game:')
      col1, col2 = st.columns(2)
      filter_by = col1.selectbox("Filter by:", ['title', 'steamAppID'])

      if filter_by == 'title':
          external = col2.text_input("Enter a game title:", value=steamAppID, key='steamAppID')
      else:
          steamAppID = col2.text_input("Enter a Steam App ID:", value=external, key='title')

      if st.button('Search Game'):
          try:
              response = requests.get(LIST_OF_GAMES_URL, params={filter_by: external})
              response.raise_for_status()
              games = response.json()
              if not games:
                if filter_by == 'title':
                  st.markdown(f'No games found by **Title**: "{external}".')
                else:
                  st.markdown(f'No games found by **Steam App ID**: "{steamAppID}".')
              else:
                  st.write('List of Games:')
                  st.dataframe(games)
          except requests.RequestException as e:
              st.error(f'Failed to fetch game data: {e}')

  games_list("", "")

with tab3:
  def stores_list():
    try:
      response = requests.get(LIST_OF_STORES_URL)
      response.raise_for_status()
      stores = response.json()

      col1, col2 = st.columns(2)
      search_field = col1.selectbox("Search by:", ['storeID', 'storeName'])
      search_value = col2.text_input("Enter search value:")

      if st.button('Search Store'):
        filtered_stores = [store for store in stores if store.get(search_field) == search_value]
        if filtered_stores:
          st.write('Filtered Stores:')
          st.dataframe(filtered_stores)
        else:
          st.write('No stores found for the given search criteria.')

      if not stores:
        st.write('No stores found.')

      col1, col2 = st.columns(2)
      show_all_stores = col1.button('Show Stores')

      if show_all_stores:
        hide_all_stores = col2.button('Hide Stores')
        st.write('List of all Stores:')
        st.dataframe(stores)
        if hide_all_stores:
          st.write('')

    except requests.RequestException as e:
      st.error(f'Failed to fetch store data: {e}')

  stores_list()

with tab4:
  def edit_alerts():
    col1, col2 = st.columns(2)
    action = col1.selectbox('Select Action', ['set', 'delete'])
    email = col2.text_input('Enter User Email', value='', args={'placeholder': 'example@example.com', 'alpha': 0.5})

    if not validate_email(email):
      st.warning('Invalid email format. Please enter a valid email address.')

    col1, col2 = st.columns([3,2])
    gameId = col1.text_input('Enter Game ID')
    price = col2.text_input('Enter Price')

    if not gameId:
          st.warning('Game ID is required.')
    if not price:
          st.warning('Price is required.')

    price = float(price) if price else None

    if st.button('Send Alert'):
      try:
        if action == 'create':
          response = requests.get(ALERT_URL, params={'action': action, 'email': email, 'gameId': gameId, 'price': price})
          response.raise_for_status()
          st.success(f"Email sent to {email} for action: {action}")
        elif action == 'delete':
          response = requests.get(ALERT_URL, params={'action': action, 'email': email, 'gameId': gameId})
          response.raise_for_status()
          st.success(f"Email sent to {email} for action: {action}")
        else:
          st.error("Invalid action. Only 'set' and 'delete' actions are supported.")
      except requests.RequestException as e:
        st.error(f'Failed to fetch alert data: {e}')

  def manage_alerts():
      col1, col2 = st.columns(2)
      action = col1.selectbox('Select Action', ['manage'])
      email = col2.text_input('Enter Users Email', value='', args={'placeholder': 'example@example.com', 'alpha': 0.5})

      if not validate_email(email):
        st.warning('Invalid email format. Please enter a valid email address.')

      if st.button('Check Alert'):
        try:
          if action == 'manage':
            response = requests.get(ALERT_URL, params={'action': action, 'email': email})
            response.raise_for_status()
            st.success(f"Email sent to {email} for action: {action}")
          else:
            st.error("Invalid action. Only 'manage' action is supported.")
        except requests.RequestException as e:
          st.error(f'Failed to fetch alert data: {e}')

  edit_alerts()
  manage_alerts()

