#By Lonique

from datetime import date, timedelta
from models.tenant import get_all_tenants, get_tenant, add_tenant, update_tenant, delete_tenant
from database.db_connection import get_connection

#Roles (for memory)
# Front Desk Staff:  register/view tenants, assign to apartments
# Administrator:     full access for their location
# Manager:           view only (overseeing everything)
# Finance Manager:   no tenant management access
# Maintenance Staff: no tenant management access

ROLES_CAN_VIEW   = {"front_desk", "administrator", "manager"}
ROLES_CAN_EDIT   = {"front_desk", "administrator"}
ROLES_CAN_DELETE = {"administrator"}
ROLES_CAN_ASSIGN = {"front_desk", "administrator"}


def _check_access(current_user, allowed_roles):
    """
    Check if the current user's role is in the allowed.
    Return access granting message
    """
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": f"Access denied. Your role '{role}' cannot perform this action."}
    return {"access": True}


#Operations

def service_get_all_tenants(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    
    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    return {"success": True, "data": get_all_tenants()}


def service_get_tenant(current_user, tenant_id):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    
    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    tenant = get_tenant(tenant_id)
    
    if not tenant:
        return {"success": False, "error": f"Tenant ID {tenant_id} not found."}
    return {"success": True, "data": tenant}


def service_add_tenant(current_user, name, phone, email, occupation,
                       ni_number, lease_period, reference, apartment_requirement):
    access = _check_access(current_user, ROLES_CAN_EDIT)
    if not access["access"]:
        return {"success": False, "error": access["error"]}


    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    
    cleaned_ni = ni_number.strip().upper()

    if cleaned_ni:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT tenant_id FROM tenants WHERE ni_number = ?", (cleaned_ni,))
        if cursor.fetchone():
            conn.close()
            return {"success": False, "error": f"A tenant with NI number '{ni_number}' already exists."}
        conn.close()

    ni_number = cleaned_ni

    add_tenant(name, phone, email, occupation, ni_number, lease_period, reference, apartment_requirement)
    return {"success": True}


def service_update_tenant(current_user, tenant_id, name, phone, email, occupation,
                          ni_number, lease_period, reference, apartment_requirement):
    access = _check_access(current_user, ROLES_CAN_EDIT)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    
    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    if not get_tenant(tenant_id):
        return {"success": False, "error": f"Tenant ID {tenant_id} not found."}

    ni_number = ni_number.strip().upper()

    update_tenant(tenant_id, name, phone, email, occupation, ni_number,
                  lease_period, reference, apartment_requirement)
    return {"success": True}


def service_delete_tenant(current_user, tenant_id):
    access = _check_access(current_user, ROLES_CAN_DELETE)
    if not access["access"]:
        return {"success": False, "error": access["error"]}
    
    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    if not get_tenant(tenant_id):
        return {"success": False, "error": f"Tenant ID {tenant_id} not found."}

    # Block deletion if tenant has an active lease
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lease_id FROM leases WHERE tenant_id = ? AND status = 'Active'", (tenant_id,))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "error": "Cannot delete tenant: they have an active lease. Terminate it first."}
    conn.close()

    #use CRUD subroutines
    delete_tenant(tenant_id)
    return {"success": True}


# assigning lease
def service_assign_tenant_to_apartment(current_user, tenant_id, apartment_id,
                                       start_date, end_date, monthly_rent):
    """
    Assign a tenant to a empty apartment. 
    Create a lease and tghrn mark apartment Occupied.
    Only Front Desk Staff and Administrators allowed to do this.
    """
    access = _check_access(current_user, ROLES_CAN_ASSIGN)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    if not get_tenant(tenant_id):
        return {"success": False, "error": f"Tenant ID {tenant_id} not found."}

    conn = get_connection()
    cursor = conn.cursor()

    # Check if apartment exist and if available
    cursor.execute("SELECT * FROM apartments WHERE apartment_id = ?", (apartment_id,))
    apartment = cursor.fetchone()
    if not apartment:
        conn.close()
        return {"success": False, "error": f"Apartment ID {apartment_id} not found."}
    
    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    
    if dict(apartment)["occupancy_status"] != "Vacant":
        conn.close()
        return {"success": False, "error": f"Apartment {apartment_id} is not vacant."}

    # Check tenant doesn't already have an active lease
    cursor.execute("SELECT lease_id FROM leases WHERE tenant_id = ? AND status = 'Active'", (tenant_id,))
    if cursor.fetchone():
        conn.close()
        return {"success": False, "error": "This tenant already has an active lease."}

    if not monthly_rent or monthly_rent <= 0:
        conn.close()
        return {"success": False, "error": "Monthly rent must be greater than zero."}

    cursor.execute(
        """INSERT INTO leases (tenant_id, apartment_id, start_date, end_date, monthly_rent, status)
           VALUES (?, ?, ?, ?, ?, 'Active')""",
        (tenant_id, apartment_id, start_date, end_date, monthly_rent)
    )
    cursor.execute(
        "UPDATE apartments SET occupancy_status = 'Occupied' WHERE apartment_id = ?",
        (apartment_id,)
    )
    conn.commit()
    lease_id = cursor.lastrowid
    conn.close()
    return {"success": True, "lease_id": lease_id}


def service_terminate_lease(current_user, lease_id, early=False):
    """
    Terminate a lease. If early is True, apply 1 month notice and 5% rent penalty.
    Only Administrators can terminate leases.
    """
    access = _check_access(current_user, ROLES_CAN_DELETE)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leases WHERE lease_id = ?", (lease_id,))
    lease = cursor.fetchone()
    if not lease:
        conn.close()
        return {"success": False, "error": f"Lease ID {lease_id} not found."}

    lease = dict(lease)
    if lease["status"] != "Active":
        conn.close()
        return {"success": False, "error": f"Lease {lease_id} is not active (status: {lease['status']})."}

    penalty = None
    if early:
        penalty = round(lease["monthly_rent"] * 0.05, 2)
        effective_end = (date.today() + timedelta(days=30)).isoformat()
        cursor.execute(
            "UPDATE leases SET status = 'Early Terminated', end_date = ? WHERE lease_id = ?",
            (effective_end, lease_id)
        )
    else:
        cursor.execute("UPDATE leases SET status = 'Terminated' WHERE lease_id = ?", (lease_id,))

    cursor.execute(
        "UPDATE apartments SET occupancy_status = 'Vacant' WHERE apartment_id = ?",
        (lease["apartment_id"],)
    )
    conn.commit()
    conn.close()
    return {"success": True, "penalty": penalty}


def service_get_tenant_lease_history(current_user, tenant_id):
    access = _check_access(current_user, ROLES_CAN_VIEW)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    allowed, err = check_location_access(current_user, location)
    if not allowed:
        return {"success": False, "error": err}
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT l.*, a.location, a.apartment_type
           FROM leases l
           JOIN apartments a ON l.apartment_id = a.apartment_id
           WHERE l.tenant_id = ?
           ORDER BY l.start_date DESC""",
        (tenant_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return {"success": True, "data": [dict(row) for row in rows]}
