"""Product catalog and ordering API endpoints."""

TAX_RATE = 0.08  # 8% tax
SHIPPING_RATES = {"standard": 5.99, "express": 14.99, "overnight": 29.99}

def calculate_order_total(items: list, shipping_method: str = "standard") -> dict:
    """Calculate the total cost of an order including tax and shipping."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = subtotal * TAX_RATE
    shipping = SHIPPING_RATES.get(shipping_method, SHIPPING_RATES["standard"])
    
    # Apply free shipping for orders over $100
    if subtotal > 100:
        shipping = 0.0
    
    total = subtotal + tax + shipping
    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "shipping": round(shipping, 2),
        "total": round(total, 2)
    }

def apply_discount(total: float, discount_code: str, valid_codes: dict) -> float:
    """Apply a discount code to an order total."""
    if discount_code not in valid_codes:
        return total
    
    discount = valid_codes[discount_code]
    if discount["type"] == "percentage":
        # BUG: Multiplying by discount instead of (1 - discount/100).
        # A 20% discount should reduce the price, but this INCREASES it.
        return total * (discount["value"] / 100)
    elif discount["type"] == "flat":
        return max(0, total - discount["value"])
    return total

def check_inventory(product_id: str, quantity: int, inventory: dict) -> bool:
    """Check if sufficient inventory exists for a product."""
    available = inventory.get(product_id, 0)
    return available >= quantity

def format_receipt(order: dict) -> str:
    """Format an order as a printable receipt string."""
    lines = ["=" * 40, "ORDER RECEIPT", "=" * 40]
    for item in order.get("items", []):
        lines.append(f"  {item['name']:30s} ${item['price']:.2f} x {item['quantity']}")
    lines.append("-" * 40)
    lines.append(f"  {'Subtotal':30s} ${order.get('subtotal', 0):.2f}")
    lines.append(f"  {'Tax':30s} ${order.get('tax', 0):.2f}")
    lines.append(f"  {'Shipping':30s} ${order.get('shipping', 0):.2f}")
    lines.append("=" * 40)
    lines.append(f"  {'TOTAL':30s} ${order.get('total', 0):.2f}")
    return "\n".join(lines)
