from database.db_connection import get_connection

ROLES_CAN_VIEW_REPORTS = {"Administrator", "Manager", "Finance Manager"}

def _check_access(current_user, allowed_roles):
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": f"Access denied."}
    return {"access": True}

def service_get_summary_report(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW_REPORTS)
    if not access["access"]: return {"success": False, "error": access["error"]}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM apartments")
    total_apartments = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM apartments WHERE occupancy_status = 'Vacant'")
    vacant_apartments = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM tenants")
    total_tenants = cursor.fetchone()["total"]

    conn.close()

    return {
        "success": True, 
        "data": {
            "total_apartments": total_apartments,
            "vacant_apartments": vacant_apartments,
            "occupied_apartments": total_apartments - vacant_apartments,
            "total_tenants": total_tenants
        }
    }

def service_get_maintenance_cost_report(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW_REPORTS)
    if not access["access"]: return {"success": False, "error": access["error"]}

    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate costs for maintenance
    cursor.execute("SELECT SUM(cost) as total_cost FROM maintenance_requests")
    row = cursor.fetchone()
    total_cost = row["total_cost"] if row["total_cost"] else 0
    
    conn.close()

    return {"success": True, "data": {"total_maintenance_cost": total_cost}}

def service_get_financial_summary(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW_REPORTS)
    if not access["access"]: return {"success": False, "error": access["error"]}

    conn = get_connection()
    cursor = conn.cursor()

    # Calculate collected rent
    cursor.execute("SELECT SUM(amount) as total FROM payments WHERE status != 'Pending'")
    collected_rent = cursor.fetchone()["total"] or 0

    # Calculate pending rent
    cursor.execute("SELECT SUM(amount) as total FROM payments WHERE status = 'Pending'")
    pending_rent = cursor.fetchone()["total"] or 0

    conn.close()

    return {
        "success": True,
        "data": {
            "collected_rent": collected_rent,
            "pending_rent": pending_rent
        }
    }