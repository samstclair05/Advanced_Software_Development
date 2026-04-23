#By Ayo, Htet
from datetime import date
from models.payment import add_payment, update_payment, delete_payment, get_all_payments
from database.db_connection import get_connection

ALLOWED_PAYMENT_ROLES = ["administrator", "finance_manager"]
ALLOWED_PAYMENT_VIEW_ROLES = ["administrator", "finance_manager", "manager"]


def _auto_status(status, due_date):
    if status == "Paid":
        return "Paid"

    try:
        if due_date and date.fromisoformat(str(due_date)) < date.today():
            return "Overdue"
    except ValueError:
        pass

    return "Pending"


def service_get_payment_details_for_tenant(current_user, tenant_id):
    if current_user["role"] not in ALLOWED_PAYMENT_ROLES:
        return {
            "success": False,
            "error": f"Access denied. Your role '{current_user['role']}' cannot perform this action."
        }

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT l.apartment_id, l.monthly_rent
            FROM leases l
            WHERE l.tenant_id = ? AND l.status = 'Active'
            """,
            (tenant_id,)
        )
        lease = cursor.fetchone()
        conn.close()

        if not lease:
            return {
                "success": False,
                "error": f"No active lease found for Tenant ID {tenant_id}."
            }

        lease = dict(lease)

        return {
            "success": True,
            "data": {
                "apartment_id": lease["apartment_id"],
                "amount": lease["monthly_rent"]
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def service_record_payment(current_user, tenant_id, apartment_id, amount, due_date, payment_date, status, invoice_number):
    if current_user["role"] not in ALLOWED_PAYMENT_ROLES:
        return {
            "success": False,
            "error": f"Access denied. Your role '{current_user['role']}' cannot perform this action."
        }

    try:
        if status not in ["Pending", "Paid"]:
            return {
                "success": False,
                "error": "Invalid payment status."
            }

        final_status = _auto_status(status, due_date)

        add_payment(
            tenant_id,
            apartment_id,
            amount,
            due_date,
            payment_date,
            final_status,
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

    if status not in ["Pending", "Paid"]:
        return {
            "success": False,
            "error": "Invalid payment status."
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

        final_status = _auto_status(status, payment_to_update["due_date"])

        update_payment(
            payment_id,
            payment_to_update["tenant_id"],
            payment_to_update["apartment_id"],
            payment_to_update["amount"],
            payment_to_update["due_date"],
            payment_to_update["payment_date"],
            final_status,
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
        payments = get_all_payments()

        normalized = []
        for payment in payments:
            final_status = _auto_status(payment["status"], payment["due_date"])
            normalized.append({
                "payment_id": payment["payment_id"],
                "tenant_id": payment["tenant_id"],
                "apartment_id": payment["apartment_id"],
                "amount": payment["amount"],
                "due_date": payment["due_date"],
                "status": final_status,
                "invoice_number": payment["invoice_number"]
            })

        return {
            "success": True,
            "data": normalized
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }