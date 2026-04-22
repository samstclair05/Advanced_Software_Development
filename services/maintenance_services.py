#By Ayo
from models.maintenance import get_all_requests, get_request, add_request, update_request, delete_request
from database.db_connection import get_connection

ROLES_CAN_VIEW_MAINTENANCE = {"Administrator", "Manager", "Front Desk Staff", "Maintenance Staff"}
ROLES_CAN_CREATE_MAINTENANCE = {"Administrator", "Front Desk Staff", "Manager", "Maintenance Staff"}
ROLES_CAN_UPDATE_MAINTENANCE = {"Administrator", "Maintenance Staff", "Manager"}

def _check_access(current_user, allowed_roles):
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": f"Access denied."}
    return {"access": True}

def service_get_all_maintenance_requests(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW_MAINTENANCE)
    if not access["access"]: return {"success": False, "error": access["error"]}
    
    return {"success": True, "data": get_all_requests()}

def service_create_maintenance_request(current_user, apartment_id, tenant_id, description, priority, status, assigned_worker, cost, time_hours, created_date):
    access = _check_access(current_user, ROLES_CAN_CREATE_MAINTENANCE)
    if not access["access"]: return {"success": False, "error": access["error"]}
    
    add_request(apartment_id, tenant_id, description, priority, status, assigned_worker, cost, time_hours, created_date)
    return {"success": True, "message": "Maintenance request created."}

def service_update_maintenance_request(current_user, request_id, priority, status, assigned_worker, cost, time_hours):
    access = _check_access(current_user, ROLES_CAN_UPDATE_MAINTENANCE)
    if not access["access"]: return {"success": False, "error": access["error"]}
    
    if not get_request(request_id):
        return {"success": False, "error": "Request not found."}
        
    update_request(request_id, priority, status, assigned_worker, cost, time_hours)
    return {"success": True, "message": "Maintenance request updated."}