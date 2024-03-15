import streamlit as st
import pandas as pd
import numpy as np
import requests
import altair as alt

LIST_OF_DEALS_URL = 'https://www.cheapshark.com/api/1.0/deals'
LIST_OF_GAMES_URL = 'https://www.cheapshark.com/api/1.0/games'
LIST_OF_STORES_URL = 'https://www.cheapshark.com/api/1.0/stores'
ALERT_URL= 'https://www.cheapshark.com/api/1.0/alerts'

st.title('Steam Games, CheapShark API')
tab1, tab2, tab3, tab4 = st.tabs(["Deals", "Games", "Stores", "Alerts"])

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

    # Convert string columns to float
    for column in ['salePrice', 'normalPrice', 'savings']:
      df[column] = df[column].astype(float)

    # Chart for normalPrice
    df_normal = df.sort_values('normalPrice', ascending=True).head(30)
    print(df_normal, "Normal Price Ascending")

    chart_normal_price = alt.Chart(df_normal).mark_bar().encode(
      x=alt.X('title', title='Product Title'),
      y=alt.Y('normalPrice:Q', title='Normal Price'),
      tooltip=[alt.Tooltip('normalPrice')]
    ).properties(
      title='Normal Price Chart',
    ).configure_axis(
      labelFontSize=16,
      titleFontSize=16
    ).configure_title(
      fontSize=16
    )
    st.altair_chart(chart_normal_price, use_container_width=True)

    # Chart for salePrice
    df_sale = df.sort_values('salePrice', ascending=True).head(30)
    print(df_sale, "Sale Price Ascending")

    chart_sale_price = alt.Chart(df_sale).mark_bar().encode(
      x=alt.X('title', title='Product Title'),
      y=alt.Y('salePrice:Q', title='Sale Price'),
      tooltip=[alt.Tooltip('salePrice')]
    ).properties(
      title='Sale Price Chart',
    ).configure_axis(
      labelFontSize=16,
      titleFontSize=16
    ).configure_title(
      fontSize=16
    )

    st.altair_chart(chart_sale_price, use_container_width=True)

    # Chart for savings
    df_savings = df.sort_values('savings', ascending=True).head(30)[['savings', 'title']]
    print(df_savings, "Savings Price Ascending")

    chart_savings = alt.Chart(df_savings).mark_bar().encode(
      x=alt.X('title', title='Product Title'),
      y=alt.Y('savings:Q', title='Savings'),
      tooltip=[alt.Tooltip('savings')]
    ).properties(
      title='Savings Chart',
    ).configure_axis(
      labelFontSize=16,
      titleFontSize=16
    ).configure_title(
      fontSize=16
    )
    st.altair_chart(chart_savings, use_container_width=True)

    return df

  load_list_of_deals()

with tab2:
  def games_list(title, steamAppID):
    try:
      st.write('Search for a game:')
      filter_by = st.selectbox("Filter by:", ['title', 'steamAppID'])

      if filter_by == 'title':
        title = st.text_input("Enter a game title:", value=steamAppID, key='steamAppID')
      else:
        steamAppID = st.text_input("Enter a Steam App ID:", value=title, key='title')

      response = requests.get(LIST_OF_GAMES_URL, params={filter_by: title})
      response.raise_for_status()
      games = response.json()
      if not games:
        st.write(f'No games found "{title}"')
        st.write('Search for a game.')
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
      if not stores:
        st.write('No stores found.')
      else:
        st.write('List of Stores:')
        st.dataframe(stores)
    except requests.RequestException as e:
      st.error(f'Failed to fetch store data: {e}')

  stores_list()

with tab4:
  def edit_alerts():
    action = st.selectbox('Select Action', ['set', 'delete'])
    email = st.text_input('Enter User Email')
    gameId = st.text_input('Enter Game ID')
    price = st.text_input('Enter Price')
    price = float(price) if price else None

    if st.button('Send Alert'):
      try:
        if action == 'create':
          response = requests.get(ALERT_URL, params={'action': action, 'email': email, 'gameId': gameId, 'price': price})
          response.raise_for_status()
          st.write(f"Email sent to {email} for action: {action}")
        elif action == 'delete':
          response = requests.get(ALERT_URL, params={'action': action, 'email': email, 'gameId': gameId})
          response.raise_for_status()
          st.write(f"Email sent to {email} for action: {action}")
        else:
          st.write("Invalid action. Only 'set' and 'delete' actions are supported.")
      except requests.RequestException as e:
        st.error(f'Failed to fetch alert data: {e}')

  def manage_alerts():
    action = st.selectbox('Select Action', ['manage'])
    email = st.text_input('Enter Email')

    if st.button('Check Alert'):
      try:
        if action == 'manage':
          response = requests.get(ALERT_URL, params={'action': action, 'email': email})
          response.raise_for_status()
          st.write(f"Email sent to {email} for action: {action}")
        else:
          st.write("Invalid action. Only 'manage' action is supported.")
      except requests.RequestException as e:
        st.error(f'Failed to fetch alert data: {e}')

  edit_alerts()
  manage_alerts()

