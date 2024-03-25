import mysql.connector
import os

from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

def database_connection():
  try:
    cnx = mysql.connector.connect(
      host=os.getenv("MYSQL_HOST"),
      port=os.getenv("MYSQL_PORT"),
      user=os.getenv("MYSQL_USER"),
      password=os.getenv("MYSQL_PASSWORD"),
      database=os.getenv("MYSQL_DATABASE")
    )

    if cnx.is_connected():
      print('Connected to MySQL database')
    else:
      print('Connection failed')

    return cnx

  except mysql.connector.Error as err:
    print(f'Error: {err}')
    return None
# NOTE: The created_at for the chat_content is when the given chat was sent
# NOTE: The created_at for the chat_session is when the chat session was created
def create_table():
  cnx = database_connection()
  if cnx is None:
    return

  try:
    cursor = cnx.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_session (
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print('Table chat_session created.')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_content (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_chat TEXT,
            ai_response TEXT,
            model TEXT,
            chat_session_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(chat_session_id) REFERENCES chat_session(id)
        )
    """)
    print('Table chat_content created.')

  except mysql.connector.Error as err:
    print(f'Error: {err}')

  finally:
    if cnx.is_connected():
      cursor.close()
      cnx.close()
      print('Database connection closed[TABLE CREATED].')

def create_new_chat_session():
  cnx = database_connection()
  if cnx is None:
    return

  cursor = cnx.cursor()
  try:
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO chat_session (created_at) VALUES (%s)", (created_at,))
    cnx.commit()
    session_id = cursor.lastrowid
    print(f"Created new chat session with ID: {session_id}")
    return session_id
  except mysql.connector.Error as err:
    print(f'Error: {err}')
    return
  finally:
    cursor.close()
    if cnx.is_connected():
      cnx.close()

def fetch_last_chat_session_id():
  cnx = database_connection()
  if cnx is None:
    return

  cursor = cnx.cursor()
  try:
    cursor.execute("SELECT id FROM chat_session ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    if result is None:
      session_id = create_new_chat_session()
      return session_id
    else:
      print(f"Last chat session ID: {result[0]}")
      return result[0]
  except mysql.connector.Error as err:
    print(f'Error: {err}')
    return
  finally:
    cursor.close()
    if cnx.is_connected():
      cnx.close()

def insert_data_chat_session(chat_content_id):
    cnx = database_connection()
    if cnx is None:
        return

    cursor = cnx.cursor()
    try:
        cursor.execute("INSERT INTO chat_session (created_at) VALUES (%s)", (chat_content_id))
        cnx.commit()
        print(f"Inserted data: chat_content_id={chat_content_id}")
    except mysql.connector.Error as err:
        print(f'Error: {err}')
    finally:
        cursor.close()
        if cnx.is_connected():
            cnx.close()

def check_session_id_exists(chat_session_id):
    cnx = database_connection()
    if cnx is None:
        return False

    cursor = cnx.cursor()
    try:
        cursor.execute("SELECT id FROM chat_session WHERE id = %s", (chat_session_id,))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print(f'Error: {err}')
    finally:
        cursor.close()
        if cnx.is_connected():
            cnx.close()

def insert_data_chat_content(user_chat, ai_response, model, created_at, chat_session_id):
  # NOTE: This is fine, however instead of creating a new chat session every time i check for an existing chat session and add the data to that chat session
  if not check_session_id_exists(chat_session_id):
    chat_session_id = create_new_chat_session()
    if chat_session_id is None:
      print("Failed to create a new chat session.")
      return
  else:
    chat_session_id = fetch_chat_session(chat_session_id)
    if chat_session_id is None:
      print("Failed to fetch the current chat session.")
      return

  cnx = database_connection()
  if cnx is None:
    return

  cursor = cnx.cursor()
  try:
    cursor.execute("INSERT INTO chat_content (user_chat, ai_response, model, created_at, chat_session_id) VALUES (%s, %s, %s, %s, %s)", (user_chat, ai_response, model, created_at, chat_session_id,))
    cnx.commit()
    print(f"Inserted data: user_chat={user_chat}, ai_response={ai_response}, model={model}, created_at={created_at}, chat_session_id={chat_session_id}")
  except mysql.connector.Error as err:
    print(f'Error: {err}')
  finally:
    cursor.close()
    if cnx.is_connected():
      cnx.close()


def fetch_all_chat_history_db():
  cnx = database_connection()
  if cnx is None:
    return []

  try:
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM chat_session")
    rows = cursor.fetchall()
    print("Total number of rows in chat_history is: ", cursor.rowcount)
    cursor.close()
    cnx.close()
    print('Database connection closed.[FETCHED DATA]')
    return rows

  except mysql.connector.Error as err:
    print(f'Error: {err}')
    if cnx.is_connected():
      cnx.close()
    return []

def fetch_selected_id_chat_history_db(chat_session_id):
  cnx = database_connection()
  if cnx is None:
    print("Database connection failed.")
    return [], None

  try:
    cursor = cnx.cursor()
    query = "SELECT * FROM chat_content WHERE chat_session_id = %s"
    cursor.execute(query, (chat_session_id,))
    rows = cursor.fetchall()
    print(f"Chat Session ID: {chat_session_id}")
    print(f"Total number of rows in chat_history is: {cursor.rowcount}")
    chat_session = fetch_chat_session(chat_session_id)
  except mysql.connector.Error as err:
    print(f'Error: {err}')
    rows = []
    chat_session = None
  finally:
    cursor.close()
    cnx.close()
    print('Database connection closed.')

  separated_rows = [list(row) for row in rows]
  return separated_rows, chat_session

def fetch_chat_session(chat_session_id):
    cnx = database_connection()
    if cnx is None:
        print("Database connection failed.")
        return None

    try:
        cursor = cnx.cursor()
        query = "SELECT * FROM chat_session WHERE id = %s"
        cursor.execute(query, (chat_session_id,))
        result = cursor.fetchone()
        if result is None:
            print(f"Chat session with ID {chat_session_id} does not exist.")
            return None
        else:
            print(f"Fetched chat session with ID: {result[0]}")
            return result[0]
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None
    finally:
        cursor.close()
        if cnx.is_connected():
            cnx.close()
