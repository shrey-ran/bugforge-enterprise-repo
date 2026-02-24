"""Session token generation and validation."""
import secrets
import time

TOKEN_EXPIRY = 3600  # 1 hour

_active_sessions = {}

def generate_session_token(user_id: str) -> str:
    """Generate a new session token for a user."""
    token = secrets.token_urlsafe(32)
    _active_sessions[token] = {
        "user_id": user_id,
        "created_at": time.time()
    }
    return token

def validate_token(token: str) -> bool:
    """Check if a session token is valid and not expired."""
    if token not in _active_sessions:
        return False
    session = _active_sessions[token]
    # BUG: Uses addition instead of subtraction to check expiry.
    # This means tokens NEVER expire because elapsed time is always positive.
    elapsed = time.time() + session["created_at"]
    return elapsed < TOKEN_EXPIRY

def revoke_token(token: str) -> bool:
    """Revoke a session token (logout)."""
    if token in _active_sessions:
        del _active_sessions[token]
        return True
    return False

def get_user_from_token(token: str) -> str:
    """Extract user_id from a valid token."""
    if validate_token(token):
        return _active_sessions[token]["user_id"]
    return None

# Applied BugForge Patch
