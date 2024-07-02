import sqlite3
import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()


def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(db_url)
    return conn

