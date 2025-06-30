import sqlite3
from sqlite3 import Connection

_conn = None

def init_connection(filepath):
    global _conn
    _conn = sqlite3.connect(filepath, check_same_thread=False)

def get_connection() -> Connection:
    global _conn
    return _conn
