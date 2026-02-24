"""Notification dispatch service for the platform."""

NOTIFICATION_TYPES = {
    "email": {"max_length": 5000, "supports_html": True},
    "sms": {"max_length": 160, "supports_html": False},
    "push": {"max_length": 256, "supports_html": False},
    "slack": {"max_length": 3000, "supports_html": True}
}

_notification_queue = []

def send_notification(user_id: str, message: str, channel: str = "email") -> dict:
    """Queue a notification for delivery."""
    if channel not in NOTIFICATION_TYPES:
        return {"success": False, "error": f"Unknown channel: {channel}"}
    
    config = NOTIFICATION_TYPES[channel]
    if len(message) > config["max_length"]:
        message = message[:config["max_length"]]
    
    notification = {
        "user_id": user_id,
        "message": message,
        "channel": channel,
        "status": "queued"
    }
    _notification_queue.append(notification)
    return {"success": True, "id": len(_notification_queue)}

def get_pending_notifications(user_id: str) -> list:
    """Get all pending notifications for a user."""
    return [n for n in _notification_queue if n["user_id"] == user_id and n["status"] == "queued"]

def mark_as_read(notification_id: int) -> bool:
    """Mark a notification as read."""
    if 0 < notification_id <= len(_notification_queue):
        _notification_queue[notification_id - 1]["status"] = "read"
        return True
    return False

def get_notification_stats(user_id: str) -> dict:
    """Get notification statistics for a user."""
    user_notifs = [n for n in _notification_queue if n["user_id"] == user_id]
    return {
        "total": len(user_notifs),
        "unread": len([n for n in user_notifs if n["status"] == "queued"]),
        "read": len([n for n in user_notifs if n["status"] == "read"])
    }
