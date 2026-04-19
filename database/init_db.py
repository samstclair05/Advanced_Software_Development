import os
from db_connection import get_connection

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

    print("Database initialised successfully. Tables created in pams.db")

if __name__ == "__main__":
    init_db()