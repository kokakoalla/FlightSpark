import psycopg2
import os

db_url = os.getenv('DATABASE_URL')
try:
    conn = psycopg2.connect(db_url)
    print("Connection to PostgreSQL established successfully.")
except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")
finally:
    if conn:
        conn.close()
        print("PostgreSQL connection is closed.")
