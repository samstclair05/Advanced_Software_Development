from models.apartment import get_all_apartments, get_apartment, add_apartment, update_apartment, delete_apartment
from database.db_connection import get_connection

# Roles 
# Administrator:      full access for their location (add, edit, delete apartments)
# Manager:            view all apartments across all locations
# Front Desk Staff:   view only (to handle tenant inquiries)
# Finance Manager:    no apartment management access
# Maintenance Staff:  no apartment management access

ROLES_CAN_VIEW   = {"Front Desk Staff", "Administrator", "Manager"}
ROLES_CAN_EDIT   = {"Administrator"}
ROLES_CAN_DELETE = {"Administrator"}


def _check_access(current_user, allowed_roles):
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": f"Access denied. Your role '{role}' cannot perform this action."}
    return {"access": True}


#Operations

def service_get_all_apartments(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    return {"success": True, "data": get_all_apartments()}


def service_get_apartment(current_user, apartment_id):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    apartment = get_apartment(apartment_id)
    if not apartment:
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}
    return {"success": True, "data": apartment}


def service_get_apartments_by_location(current_user, location):
    """Managers see all locations. Admins are filtered to their own location."""
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apartments WHERE location = ? ORDER BY apartment_id", (location,))
    rows = cursor.fetchall()
    conn.close()
    return {"success": True, "data": [dict(row) for row in rows]}


def service_get_vacant_apartments(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apartments WHERE occupancy_status = 'Vacant' ORDER BY location")
    rows = cursor.fetchall()
    conn.close()
    return {"success": True, "data": [dict(row) for row in rows]}


def service_add_apartment(current_user, location, apartment_type, num_rooms,
                          floor_number, monthly_rent, occupancy_status="Vacant", notes=""):
    access = _check_access(current_user, ROLES_CAN_EDIT)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    #use CRUD subroutines
    add_apartment(location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes)
    return {"success": True}


def service_update_apartment(current_user, apartment_id, location, apartment_type,
                             num_rooms, floor_number, monthly_rent, occupancy_status, notes=""):
    access = _check_access(current_user, ROLES_CAN_EDIT)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    if not get_apartment(apartment_id):
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    #Cant manually put is occupied if no lease, expetion handling
    if occupancy_status == "Occupied":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT lease_id FROM leases WHERE apartment_id = ? AND status = 'Active'", (apartment_id,))
        if not cursor.fetchone():
            conn.close()
            return {"success": False, "error": "Cannot set status to 'Occupied' without an active lease. Use the assign tenant function."}
        conn.close()

    #use CRUD subroutines
    update_apartment(apartment_id, location, apartment_type, num_rooms,
                     floor_number, monthly_rent, occupancy_status, notes)
    return {"success": True}


def service_delete_apartment(current_user, apartment_id):
    access = _check_access(current_user, ROLES_CAN_DELETE)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    if not get_apartment(apartment_id):
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    #Cant delete if lease = active
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lease_id FROM leases WHERE apartment_id = ? AND status = 'Active'", (apartment_id,))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "error": "Cannot delete apartment: it has an active lease. Terminate it first."}
    conn.close()

    #call subroutine
    delete_apartment(apartment_id)
    return {"success": True}


#Check who lives there currently

def service_get_current_tenant(current_user, apartment_id):
    """Return the current tenant and lease info for an apartment."""
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT t.*, l.lease_id, l.start_date, l.end_date,
                  l.monthly_rent AS lease_rent, l.status AS lease_status
           FROM leases l
           JOIN tenants t ON l.tenant_id = t.tenant_id
           WHERE l.apartment_id = ? AND l.status = 'Active'""",
        (apartment_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return {"success": True, "data": dict(row) if row else None}
