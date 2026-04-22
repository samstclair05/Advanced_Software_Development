def check_location_access(current_user, resource_location):
    """
    Aministrators have no location restriction.
    All other roles are scoped to their assigned location.
    """
    role = current_user.get("role")
    user_location = current_user.get("location")

    if role == "Administrator":
        return True, None  #Administrators see everything

    if not user_location:
        return False, "Your account has no location assigned. Contact an administrator."

    if resource_location != user_location:
        return False, f"Access denied. This record belongs to '{resource_location}', not your location ('{user_location}')."

    return True, None