from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

def connect():
    db = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        passwd=os.getenv('DB_PASS'),
        database=os.getenv('DB_DATABASE')
    )

    if db.is_connected():
        return db
    else:
        print("Connection Failed!")
        return False