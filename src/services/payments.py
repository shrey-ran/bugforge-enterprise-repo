"""Payment processing service with Stripe-like integration."""

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY"]
MIN_AMOUNT = 0.50
MAX_AMOUNT = 999999.99

def process_payment(amount: float, currency: str, card_token: str) -> dict:
    """Process a payment transaction."""
    if currency not in SUPPORTED_CURRENCIES:
        return {"success": False, "error": f"Unsupported currency: {currency}"}
    if amount < MIN_AMOUNT or amount > MAX_AMOUNT:
        return {"success": False, "error": "Amount out of allowed range"}
    
    # Simulate payment processing
    return {
        "success": True,
        "transaction_id": f"txn_{hash(card_token) % 1000000:06d}",
        "amount": amount,
        "currency": currency
    }

def calculate_refund(original_amount: float, days_since_purchase: int) -> dict:
    """Calculate refund amount based on return policy.
    
    Policy:
    - Within 7 days: 100% refund
    - 8-30 days: 80% refund
    - 31-60 days: 50% refund
    - After 60 days: no refund
    """
    if days_since_purchase <= 7:
        refund_percentage = 100
    elif days_since_purchase <= 30:
        refund_percentage = 80
    elif days_since_purchase <= 60:
        refund_percentage = 50
    else:
        refund_percentage = 0
    
    refund_amount = original_amount * (refund_percentage / 100)
    return {
        "original_amount": original_amount,
        "refund_percentage": refund_percentage,
        "refund_amount": round(refund_amount, 2)
    }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert between currencies using hardcoded rates."""
    rates_to_usd = {
        "USD": 1.0,
        "EUR": 1.08,
        "GBP": 1.27,
        "INR": 0.012,
        "JPY": 0.0067
    }
    if from_currency not in rates_to_usd or to_currency not in rates_to_usd:
        raise ValueError(f"Unsupported currency pair: {from_currency}/{to_currency}")
    
    usd_amount = amount * rates_to_usd[from_currency]
    return round(usd_amount / rates_to_usd[to_currency], 2)

def validate_card_number(card_number: str) -> bool:
    """Validate a credit card number using the Luhn algorithm."""
    digits = [int(d) for d in card_number if d.isdigit()]
    if len(digits) < 13 or len(digits) > 19:
        return False
    
    checksum = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0
