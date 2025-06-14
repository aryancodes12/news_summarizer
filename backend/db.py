import sqlite3
from os import makedirs
from os.path import exists

DB_PATH = "data/news.db"

def init_db():
    if not exists("data"):
        makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            summary TEXT,
            url TEXT,
            thumbnail TEXT,
            timestamp TEXT,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)