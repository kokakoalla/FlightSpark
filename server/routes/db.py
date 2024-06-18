import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'my_app.db')
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn
