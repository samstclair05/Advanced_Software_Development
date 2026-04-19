from database.db_connection import get_connection

def get_all_tenants():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tenants")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_tenant(tenant_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tenants WHERE tenant_id = ?", (tenant_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_tenant(name, phone, email, occupation, ni_number, lease_period, reference, apartment_requirement):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tenants (name, phone, email, occupation, ni_number, lease_period, reference, apartment_requirement)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, phone, email, occupation, ni_number, lease_period, reference, apartment_requirement)
    )
    conn.commit()
    conn.close()

def update_tenant(tenant_id, name, phone, email, occupation, ni_number, lease_period, reference, apartment_requirement):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE tenants SET name=?, phone=?, email=?, occupation=?, ni_number=?,
           lease_period=?, reference=?, apartment_requirement=? WHERE tenant_id=?""",
        (name, phone, email, occupation, ni_number, lease_period, reference, apartment_requirement, tenant_id)
    )
    conn.commit()
    conn.close()

def delete_tenant(tenant_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tenants WHERE tenant_id = ?", (tenant_id,))
    conn.commit()
    conn.close()