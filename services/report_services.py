from database.db_connection import get_connection

ROLES_CAN_VIEW_REPORTS = {"administrator", "manager", "finance_manager"}

VALID_LOCATIONS = {"Bristol", "Cardiff", "London", "Manchester"}


def _check_access(current_user, allowed_roles):
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": "Access denied."}
    return {"access": True}


def _resolve_location(current_user, requested_location=None):
    """
    Determine which location to scope the report to
    Administrator: can pass in a requested_location to choose - defaults to
      their own assigned location if none is given, other roles have no choice
    """
    role = current_user.get("role")
    user_location = current_user.get("location")

    if role == "administrator":
        if requested_location:
            normalised = requested_location.strip().title()
            if normalised not in VALID_LOCATIONS:
                return None, (
                    f"'{requested_location}' is not a valid location. "
                    f"Choose from: {', '.join(sorted(VALID_LOCATIONS))}."
                )
            return normalised, None
        # Fall back to their own assigned location
        if not user_location:
            return None, "Your account has no location assigned. Contact a Manager."
        return user_location, None

    # All other roles are pinned to their assigned location
    if not user_location:
        return None, "Your account has no location assigned. Contact an Administrator."
    return user_location, None

def service_get_summary_report(current_user, requested_location=None):
    """
    Return apartment/tenant counts scoped to a single location.
     """
    
    access = _check_access(current_user, ROLES_CAN_VIEW_REPORTS)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    location, err = _resolve_location(current_user, requested_location)
    if err:
        return {"success": False, "error": err}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) as total FROM apartments WHERE location = ?",
        (location,)
    )
    total_apartments = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as total FROM apartments WHERE location = ? AND occupancy_status = 'Vacant'",
        (location,)
    )
    vacant_apartments = cursor.fetchone()["total"]

    # Tenants whose active lease is in this location
    cursor.execute(
        """SELECT COUNT(DISTINCT t.tenant_id) as total
           FROM tenants t
           JOIN leases l ON t.tenant_id = l.tenant_id
           JOIN apartments a ON l.apartment_id = a.apartment_id
           WHERE a.location = ? AND l.status = 'Active'""",
        (location,)
    )
    total_tenants = cursor.fetchone()["total"]

    conn.close()

    return {
        "success": True,
        "location": location,
        "data": {
            "total_apartments": total_apartments,
            "vacant_apartments": vacant_apartments,
            "occupied_apartments": total_apartments - vacant_apartments,
            "total_tenants": total_tenants,
        }
    }


def service_get_maintenance_cost_report(current_user, requested_location=None):

    access = _check_access(current_user, ROLES_CAN_VIEW_REPORTS)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    location, err = _resolve_location(current_user, requested_location)
    if err:
        return {"success": False, "error": err}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT SUM(mr.cost) as total_cost
           FROM maintenance_requests mr
           JOIN apartments a ON mr.apartment_id = a.apartment_id
           WHERE a.location = ?""",
        (location,)
    )
    row = cursor.fetchone()
    total_cost = row["total_cost"] if row["total_cost"] else 0

    conn.close()

    return {
        "success": True,
        "location": location,
        "data": {"total_maintenance_cost": total_cost}
    }


def service_get_financial_summary(current_user, requested_location=None):
    access = _check_access(current_user, ROLES_CAN_VIEW_REPORTS)
    if not access["access"]:
        return {"success": False, "error": access["error"]}

    # Prompt Administrator to pick a location before generating the report
    if current_user.get("role", "").lower() == "administrator" and not requested_location:
        return {
            "success": False,
            "prompt_location": True,
            "valid_locations": sorted(VALID_LOCATIONS),
            "message": "Please select a location to generate the financial summary for: Bristol, Cardiff, London, Manchester."
        }

    location, err = _resolve_location(current_user, requested_location)
    if err:
        return {"success": False, "error": err}

    conn = get_connection()
    cursor = conn.cursor()

    # Calculate collected rent for location
    cursor.execute(
        """SELECT SUM(p.amount) as total
           FROM payments p
           JOIN apartments a ON p.apartment_id = a.apartment_id
           WHERE p.status != 'Pending' AND a.location = ?""",
        (location,)
    )
    collected_rent = cursor.fetchone()["total"] or 0

    # Calculate pending rent for location
    cursor.execute(
        """SELECT SUM(p.amount) as total
           FROM payments p
           JOIN apartments a ON p.apartment_id = a.apartment_id
           WHERE p.status = 'Pending' AND a.location = ?""",
        (location,)
    )
    pending_rent = cursor.fetchone()["total"] or 0

    conn.close()

    return {
        "success": True,
        "location": location,
        "data": {
            "collected_rent": collected_rent,
            "pending_rent": pending_rent
        }
    }