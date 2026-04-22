# Samuel St Clair

from database.db_connection import get_connection

def get_all_apartments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apartments")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_apartment(apartment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apartments WHERE apartment_id = ?", (apartment_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_apartment(location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO apartments (location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes)
    )
    conn.commit()
    conn.close()

def update_apartment(apartment_id, location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE apartments SET location=?, apartment_type=?, num_rooms=?, floor_number=?,
           monthly_rent=?, occupancy_status=?, notes=? WHERE apartment_id=?""",
        (location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes, apartment_id)
    )
    conn.commit()
    conn.close()

def delete_apartment(apartment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM apartments WHERE apartment_id = ?", (apartment_id,))
    conn.commit()
    conn.close()