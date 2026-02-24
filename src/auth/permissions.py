"""Role-based access control for the platform."""

ROLE_HIERARCHY = {
    "admin": 3,
    "manager": 2,
    "editor": 1,
    "viewer": 0
}

def check_permission(user_role: str, required_role: str) -> bool:
    """Check if a user's role has sufficient permissions."""
    user_level = ROLE_HIERARCHY.get(user_role, 0)
    required_level = ROLE_HIERARCHY.get(required_role, 0)
    return user_level >= required_level

def assign_role(user_id: str, new_role: str, assigner_role: str) -> bool:
    """Allow a user to assign a role, only if they outrank the target role."""
    if new_role not in ROLE_HIERARCHY:
        return False
    return check_permission(assigner_role, new_role)

def get_role_name(level: int) -> str:
    """Convert a numeric level back to a role name."""
    for role, lvl in ROLE_HIERARCHY.items():
        if lvl == level:
            return role
    return "unknown"
