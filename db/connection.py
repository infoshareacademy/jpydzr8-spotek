# db/connection.py
import os
from contextlib import contextmanager
from dotenv import load_dotenv
import mysql.connector

# wczytaj zmienne z .env (w katalogu głównym projektu)
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "Admin_1234"),
    "database": os.getenv("DB_NAME", "baza_spotek"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

@contextmanager
def get_conn():
    conn = mysql.connector.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_cursor(commit: bool = False):
    with get_conn() as conn:
        cur = conn.cursor()
        try:
            yield cur
            if commit:
                conn.commit()
        finally:
            cur.close()
