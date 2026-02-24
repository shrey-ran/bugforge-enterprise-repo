"""Date and time utility functions."""
from datetime import datetime, timedelta

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_business_days(start_date: str, end_date: str) -> int:
    """Count the number of business days (Mon-Fri) between two dates."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    if start > end:
        start, end = end, start
    
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # Mon=0, Fri=4
            count += 1
        current += timedelta(days=1)
    return count

def format_relative_time(timestamp: float) -> str:
    """Convert a Unix timestamp to a human-readable relative time string."""
    now = datetime.now()
    dt = datetime.fromtimestamp(timestamp)
    diff = now - dt
    
    seconds = diff.total_seconds()
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        mins = int(seconds // 60)
        return f"{mins} minute{'s' if mins > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"

def get_quarter(date_str: str) -> str:
    """Get the fiscal quarter for a given date."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    month = dt.month
    if month <= 3:
        return f"Q1 {dt.year}"
    elif month <= 6:
        return f"Q2 {dt.year}"
    elif month <= 9:
        return f"Q3 {dt.year}"
    else:
        return f"Q4 {dt.year}"

def add_working_days(start_date: str, days_to_add: int) -> str:
    """Add a number of working days to a date, skipping weekends."""
    current = datetime.strptime(start_date, "%Y-%m-%d")
    added = 0
    while added < days_to_add:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current.strftime("%Y-%m-%d")
