"""Authentication login handler for the enterprise platform."""
import hashlib
import time

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes

_failed_attempts = {}

def hash_password(password: str, salt: str = "enterprise_salt") -> str:
    """Hash a password with SHA-256 and salt."""
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

def check_credentials(username: str, password: str, user_db: dict) -> bool:
    """Verify user credentials against the database."""
    if username not in user_db:
        return False
    stored_hash = user_db[username]["password_hash"]
    return hash_password(password) == stored_hash

def is_account_locked(username: str) -> bool:
    """Check if account is locked due to too many failed attempts."""
    if username not in _failed_attempts:
        return False
    attempts, lock_time = _failed_attempts[username]
    if attempts >= MAX_LOGIN_ATTEMPTS:
        if time.time() - lock_time < LOCKOUT_DURATION:
            return True
        else:
            _failed_attempts.pop(username)
            return False
    return False

def record_failed_attempt(username: str):
    """Record a failed login attempt."""
    if username in _failed_attempts:
        attempts, _ = _failed_attempts[username]
        _failed_attempts[username] = (attempts + 1, time.time())
    else:
        _failed_attempts[username] = (1, time.time())
