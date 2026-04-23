# Samuel St Clair - 24022864

from database.db_connection import get_connection

def get_all_payments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_payment(payment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE payment_id = ?", (payment_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_payment(tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number):
    conn = get_connection()
    cursor = conn.cursor()

    #insert first without invoice number
    cursor.execute("""
        INSERT INTO payments (tenant_id, apartment_id, amount, due_date, payment_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tenant_id, apartment_id, amount, due_date, payment_date, status))

    payment_id = cursor.lastrowid

    #generate invoice
    invoice_number = f"INV-{payment_id}"

    cursor.execute("""
        UPDATE payments SET invoice_number = ? WHERE payment_id = ?
    """, (invoice_number, payment_id))

    conn.commit()
    conn.close()

def update_payment(payment_id, tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE payments SET tenant_id=?, apartment_id=?, amount=?, due_date=?,
           payment_date=?, status=?, invoice_number=? WHERE payment_id=?""",
        (tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number, payment_id)
    )
    conn.commit()
    conn.close()

def delete_payment(payment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM payments WHERE payment_id = ?", (payment_id,))
    conn.commit()
    conn.close()