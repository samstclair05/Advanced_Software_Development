#Lonique Mayoua 24027974
#Htet Oo Wai - 24037079

from models.apartment import get_all_apartments, get_apartment, add_apartment, update_apartment, delete_apartment
from database.db_connection import get_connection
from services.location_guard import check_location_access

# Roles
# administrator: full access for their location
# manager: can view all locations
# front_desk: view only
# finance_manager: no apartment management access
# maintenance_staff: no apartment management access

ROLES_CAN_VIEW   = {"front_desk", "administrator", "manager"}
ROLES_CAN_EDIT   = {"administrator"}
ROLES_CAN_DELETE = {"administrator"}


def _check_access(current_user, allowed_roles):
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": f"Access denied. Your role '{role}' cannot perform this action."}
    return {"access": True}


# Operations

def service_get_all_apartments(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    apartments = get_all_apartments()

    if current_user.get("role") == "administrator":
        return {"success": True, "data": apartments}

    user_loc = current_user.get("location")
    apartments = [a for a in apartments if a["location"] == user_loc]

    return {"success": True, "data": apartments}


def service_get_apartment(current_user, apartment_id):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    apartment = get_apartment(apartment_id)
    if not apartment:
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    allowed, err = check_location_access(current_user, apartment["location"])
    if not allowed:
        return {"success": False, "error": err}

    return {"success": True, "data": apartment}


def service_get_apartments_by_location(current_user, location):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}

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

    apartments = get_all_apartments()

    if current_user.get("role") != "manager":
        user_loc = current_user.get("location")
        apartments = [a for a in apartments if a["location"] == user_loc]

    apartments = [a for a in apartments if a["occupancy_status"] == "Vacant"]

    return {"success": True, "data": apartments}


def service_add_apartment(current_user, location, apartment_type, num_rooms,
                          floor_number, monthly_rent, occupancy_status="Vacant", notes=""):
    access = _check_access(current_user, ROLES_CAN_EDIT)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}

    add_apartment(location, apartment_type, num_rooms, floor_number, monthly_rent, occupancy_status, notes)
    return {"success": True}


def service_update_apartment(current_user, apartment_id, location, apartment_type,
                             num_rooms, floor_number, monthly_rent, occupancy_status, notes=""):
    access = _check_access(current_user, ROLES_CAN_EDIT)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    apartment = get_apartment(apartment_id)
    if not apartment:
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    allowed, err = check_location_access(current_user, apartment["location"])
    if not allowed:
        return {"success": False, "error": err}

    # prevent manual occupied without lease
    if occupancy_status == "Occupied":
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT lease_id FROM leases WHERE apartment_id = ? AND status = 'Active'",
            (apartment_id,)
        )
        if not cursor.fetchone():
            conn.close()
            return {"success": False, "error": "Cannot set status to 'Occupied' without an active lease. Use the assign tenant function."}
        conn.close()

    update_apartment(apartment_id, location, apartment_type, num_rooms,
                     floor_number, monthly_rent, occupancy_status, notes)
    return {"success": True}


def service_delete_apartment(current_user, apartment_id):
    access = _check_access(current_user, ROLES_CAN_DELETE)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    apartment = get_apartment(apartment_id)
    if not apartment:
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    allowed, err = check_location_access(current_user, apartment["location"])
    if not allowed:
        return {"success": False, "error": err}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT lease_id FROM leases WHERE apartment_id = ? AND status = 'Active'",
        (apartment_id,)
    )
    if cursor.fetchone():
        conn.close()
        return {
            "success": False,
            "error": "This apartment cannot be deleted because it has an active lease. Terminate the lease first, or mark the apartment as Inactive."
        }
    conn.close()

    delete_apartment(apartment_id)
    return {"success": True}


def service_get_current_tenant(current_user, apartment_id):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    apartment = get_apartment(apartment_id)
    if not apartment:
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    allowed, err = check_location_access(current_user, apartment["location"])
    if not allowed:
        return {"success": False, "error": err}

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


def service_terminate_current_lease_for_apartment(current_user, apartment_id):
    access = _check_access(current_user, ROLES_CAN_DELETE)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    apartment = get_apartment(apartment_id)
    if not apartment:
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}

    allowed, err = check_location_access(current_user, apartment["location"])
    if not allowed:
        return {"success": False, "error": err}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT lease_id FROM leases WHERE apartment_id = ? AND status = 'Active'",
        (apartment_id,)
    )
    lease = cursor.fetchone()

    if not lease:
        conn.close()
        return {"success": False, "error": "No active lease found for this apartment."}

    lease_id = lease["lease_id"]

    cursor.execute(
        "UPDATE leases SET status = 'Terminated' WHERE lease_id = ?",
        (lease_id,)
    )
    cursor.execute(
        "UPDATE apartments SET occupancy_status = 'Vacant' WHERE apartment_id = ?",
        (apartment_id,)
    )

    conn.commit()
    conn.close()

    return {"success": True, "message": "Lease terminated successfully. Apartment is now Vacant."}