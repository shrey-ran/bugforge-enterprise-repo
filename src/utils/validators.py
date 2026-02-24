"""Data validation and formatting utilities."""
import re
from datetime import datetime

def validate_phone(phone: str) -> bool:
    """Validate a phone number format."""
    pattern = r'^\+?1?\d{10,14}$'
    return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a monetary amount with proper currency symbol."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹", "JPY": "¥"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def calculate_age(birth_date: str) -> int:
    """Calculate age from a birth date string (YYYY-MM-DD)."""
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.now()
    age = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1
    return age

def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def parse_csv_line(line: str) -> list:
    """Parse a simple CSV line into fields."""
    fields = []
    current = ""
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(current.strip())
            current = ""
        else:
            current += char
    fields.append(current.strip())
    return fields

def mask_sensitive_data(text: str, visible_chars: int = 4) -> str:
    """Mask sensitive data like credit card numbers or SSNs."""
    if len(text) <= visible_chars:
        return text
    return "*" * (len(text) - visible_chars) + text[-visible_chars:]
