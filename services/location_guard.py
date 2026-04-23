def check_location_access(current_user, resource_location):
    """
    Administrators can access all locations.
    All other roles are restricted to their own location.
    """
    role = current_user.get("role")
    user_location = current_user.get("location")

    if role == "administrator":
        return True, None

    if not user_location:
        return False, "Your account has no location assigned. Contact an administrator."

    if resource_location != user_location:
        return False, f"Access denied. This record belongs to '{resource_location}', not your location ('{user_location}')."

    return True, None