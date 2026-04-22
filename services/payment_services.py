#By Ayo, Htet
from models.payment import add_payment, update_payment, delete_payment, get_all_payments

# roles allowed to create, update, or delete payments
ALLOWED_PAYMENT_ROLES = ["administrator", "finance_manager"]

# roles allowed to view payment history
ALLOWED_PAYMENT_VIEW_ROLES = ["administrator", "finance_manager", "manager"]


def service_record_payment(current_user, tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number):
    if current_user["role"] not in ALLOWED_PAYMENT_ROLES:
        return {
            "success": False,
            "error": f"Access denied. Your role '{current_user['role']}' cannot perform this action."
        }

    try:
        add_payment(
            tenant_id,
            apartment_id,
            amount,
            due_date,
            payment_date,
            status,
            invoice_number
        )
        return {
            "success": True,
            "message": "Payment recorded successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def service_update_payment_status(current_user, payment_id, status):
    if current_user["role"] not in ALLOWED_PAYMENT_ROLES:
        return {
            "success": False,
            "error": f"Access denied. Your role '{current_user['role']}' cannot perform this action."
        }

    try:
        payments = get_all_payments()
        payment_to_update = None

        for payment in payments:
            if str(payment["payment_id"]) == str(payment_id):
                payment_to_update = payment
                break

        if not payment_to_update:
            return {
                "success": False,
                "error": "Payment not found."
            }

        update_payment(
            payment_id,
            payment_to_update["tenant_id"],
            payment_to_update["apartment_id"],
            payment_to_update["amount"],
            payment_to_update["due_date"],
            payment_to_update["payment_date"],
            status,
            payment_to_update["invoice_number"]
        )

        return {
            "success": True,
            "message": "Payment status updated successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def service_delete_payment(current_user, payment_id):
    if current_user["role"] not in ALLOWED_PAYMENT_ROLES:
        return {
            "success": False,
            "error": f"Access denied. Your role '{current_user['role']}' cannot perform this action."
        }

    try:
        delete_payment(payment_id)
        return {
            "success": True,
            "message": "Payment deleted successfully."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def service_get_payment_history(current_user):
    if current_user["role"] not in ALLOWED_PAYMENT_VIEW_ROLES:
        return {
            "success": False,
            "error": f"Access denied. Your role '{current_user['role']}' cannot view payment history."
        }

    try:
        return {
            "success": True,
            "data": get_all_payments()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }