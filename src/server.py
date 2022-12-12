from flask import Flask
from flask import request
import mysql.connector
import uuid
import os

app = Flask(__name__)

DB_IP = os.environ.get("DB_IP", "192.168.0.105")
DB_USER = "root"
DB_PASSWORD = ""


@app.route("/insert_event", methods = ['POST', 'GET'])
def insert_event():
  if request.is_json:
    req_json = request.get_json()
  else:
    req_json = request.args
  name = req_json.get("name")
  detail = req_json.get("detail")

  if name is None:
    return "name is None"
  
  if detail is None:
    return "detail is None"

  try:
    db_connection = mysql.connector.connect(
      host=DB_IP,
      user=DB_USER,
      password=DB_PASSWORD
    )

    cursor = db_connection.cursor(prepared=True)
    cursor.execute("USE trading_record;")

    cursor.execute('SELECT dolt_pull("origin", "main")')
    print(list(cursor.fetchall()))

    event_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO trading_event (event_id, event_name, event_detail) VALUES (%s, %s, %s)", (event_id, name, detail))
    db_connection.commit()

    cursor.execute('SELECT dolt_add("trading_event")')
    print(list(cursor.fetchall()))

    cursor.execute('SELECT dolt_commit("-m", ".")')
    print(list(cursor.fetchall()))

    cursor.execute('SELECT dolt_push("origin", "main")')
    print(list(cursor.fetchall()))

    cursor.execute("SELECT * FROM trading_event")
    results = cursor.fetchall()
    print(list(results))

  except mysql.connector.Error as error:
    print("parameterized query failed {}".format(error))
    return "Failed to insert event {}".format(error)
  finally:
    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("MySQL connection is closed")

  return "{}: {}".format(name, detail)