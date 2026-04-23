# Samuel St Clair - 24022864

from database.db_connection import get_connection

def get_all_requests():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM maintenance_requests")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_request(request_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM maintenance_requests WHERE request_id = ?", (request_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_request(apartment_id, tenant_id, description, priority, status, assigned_worker, cost, time_hours, created_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO maintenance_requests
           (apartment_id, tenant_id, description, priority, status, assigned_worker, cost, time_hours, created_date)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (apartment_id, tenant_id, description, priority, status, assigned_worker, cost, time_hours, created_date)
    )
    conn.commit()
    conn.close()

def update_request(request_id, priority, status, assigned_worker, cost, time_hours):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE maintenance_requests SET priority=?, status=?, assigned_worker=?,
           cost=?, time_hours=? WHERE request_id=?""",
        (priority, status, assigned_worker, cost, time_hours, request_id)
    )
    conn.commit()
    conn.close()

def delete_request(request_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM maintenance_requests WHERE request_id = ?", (request_id,))
    conn.commit()
    conn.close()