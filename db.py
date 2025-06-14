import sqlite3
import bcrypt
import pathlib
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

sql_file_path = resource_path("models/create_tables.sql")
db_path = resource_path("data.db")

def initialize_database():
    if not os.path.exists(sql_file_path):
        raise FileNotFoundError(f"SQL schema file not found at {sql_file_path}")

    conn = sqlite3.connect(db_path)
    with open(sql_file_path, "r") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()

def insert_operator(cursor, username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO operators (username, password) VALUES (?, ?)", (username, hashed))
    except sqlite3.IntegrityError:
        pass  # already exists

def verify_login(username, password):
    conn = sqlite3.connect("infotech.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM operators WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False
