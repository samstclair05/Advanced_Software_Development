from models.payment import get_all_payments, get_payment, add_payment, update_payment, delete_payment
from database.db_connection import get_connection

ROLES_CAN_VIEW_PAYMENTS = {"Administrator", "Manager", "Finance Manager", "Front Desk Staff"}
ROLES_CAN_MANAGE_PAYMENTS = {"Administrator", "Finance Manager"}

def _check_access(current_user, allowed_roles):
    if not current_user:
        return {"access": False, "error": "No user is logged in."}
    role = current_user.get("role")
    if role not in allowed_roles:
        return {"access": False, "error": f"Access denied. Your role '{role}' cannot perform this action."}
    return {"access": True}

def service_get_payment_history(current_user):
    access = _check_access(current_user, ROLES_CAN_VIEW_PAYMENTS)
    if not access["access"]: return {"success": False, "error": access["error"]}
    
    return {"success": True, "data": get_all_payments()}

def service_record_payment(current_user, tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number):
    access = _check_access(current_user, ROLES_CAN_MANAGE_PAYMENTS)
    if not access["access"]: return {"success": False, "error": access["error"]}
    
    add_payment(tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number)
    return {"success": True, "message": "Payment recorded successfully."}

def service_update_payment_status(current_user, payment_id, status):
    access = _check_access(current_user, ROLES_CAN_MANAGE_PAYMENTS)
    if not access["access"]: return {"success": False, "error": access["error"]}
    
    payment = get_payment(payment_id)
    if not payment:
        return {"success": False, "error": "Payment not found."}
        
    update_payment(payment_id, payment['tenant_id'], payment['apartment_id'], payment['amount'], 
                   payment['due_date'], payment['payment_date'], status, payment['invoice_number'])
    return {"success": True, "message": "Payment status updated."}