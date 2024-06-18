import sqlite3
import os

def create_tables():
    db_path = os.path.join(os.path.dirname(__file__), 'my_app.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create search_history table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_city TEXT,
        to_city TEXT,
        price REAL,
        date_time INTEGER,
        url TEXT,
        from_id TEXT,
        to_id TEXT,
        local_arrival TEXT,
        local_departure TEXT,
        stopovers INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()



if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully.")