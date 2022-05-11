import os
import sqlite3

def get_database_connection():
    """connects to database and returns connection to records.db
    Returns:
        database connection
    """
    dirname = os.path.dirname(__file__)
    connection = sqlite3.connect(os.path.join(dirname, "..", "records.db"))
    return connection

def drop_table(connection):
    """drops table if it exists already
    """
    cursor = connection.cursor()
    cursor.execute("""drop table if exists records""")
    connection.commit()

def create_table(connection):
    """creates table for scores
    """
    cursor = connection.cursor()
    cursor.execute("""create table records (score integer);""")
    connection.commit()

def initialize_database():
    """initialized the database
    """
    connection = get_database_connection()
    drop_table(connection)
    create_table(connection)

if __name__ == '__main__':
    initialize_database()
