from database.db_connection import get_connection

def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_user(username, password, role="front_desk", location=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role, location) VALUES (?, ?, ?, ?)",
        (username, password, role, location)
    )
    conn.commit()
    conn.close()

def seed_users():
    """Create one test account per role. Safe to run multiple times."""
    accounts = [
        ("frontdesk1", "1234", "front_desk",       "Bristol"),
        ("finance1",   "1234", "finance_manager",   "Bristol"),
        ("maint1",     "1234", "maintenance_staff", "Bristol"),
        ("admin1",     "1234", "administrator",     "Bristol"),
        ("manager1",   "1234", "manager",           "Bristol"),
    ]
    for username, password, role, location in accounts:
        add_user(username, password, role, location)
    print("Test accounts seeded successfully.")

if __name__ == "__main__":
    seed_users()