# Samuel St Clair - 24022864

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "pams.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-like access to rows
    return conn