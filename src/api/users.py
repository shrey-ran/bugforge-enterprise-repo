"""REST API endpoint handlers for user management."""
from typing import Optional

def create_user_response(user_data: dict) -> dict:
    """Format a user object for API response."""
    return {
        "id": user_data.get("id"),
        "username": user_data.get("username"),
        "email": user_data.get("email"),
        "role": user_data.get("role", "viewer"),
        "is_active": user_data.get("is_active", True)
    }

def paginate_results(items: list, page: int, per_page: int = 20) -> dict:
    """Paginate a list of results."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "data": items[start:end],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

def validate_email(email: str) -> bool:
    """Basic email validation."""
    if not email or "@" not in email:
        return False
    parts = email.split("@")
    return len(parts) == 2 and len(parts[0]) > 0 and "." in parts[1]

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters from user input."""
    dangerous_chars = ["<", ">", "&", '"', "'", ";", "--"]
    result = text
    for char in dangerous_chars:
        result = result.replace(char, "")
    return result.strip()
