import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'Successfully connected to {db_file}')
        return conn
    except sqlite3.Error as e:
        print(f'Error occurred: {e}')
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f'Error occurred: {e}')

def main():
    database = "my_app.db"

    sql_create_search_history_table = """CREATE TABLE IF NOT EXISTS search_history (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        from_city TEXT NOT NULL,
                                        to_city TEXT NOT NULL,
                                        price REAL NOT NULL,
                                        date_time INTEGER NOT NULL,
                                        url TEXT NOT NULL, 
                                        from_id TEXT NOT NULL,
                                        to_id TEXT NOT NULL,
                                        local_arrival TEXT NOT NULL,
                                        local_departure TEXT NOT NULL,
                                        stopovers INTEGER NOT NULL
                                    );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_search_history_table)
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()