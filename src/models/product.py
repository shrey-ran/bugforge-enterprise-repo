"""Data models and schema definitions."""

class Product:
    def __init__(self, id: str, name: str, price: float, category: str, stock: int = 0):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock
    
    def is_in_stock(self) -> bool:
        return self.stock > 0
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "stock": self.stock
        }

class ShoppingCart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items = []
    
    def add_item(self, product: Product, quantity: int = 1) -> bool:
        if quantity <= 0 or quantity > product.stock:
            return False
        
        # Check if item already in cart
        for item in self.items:
            if item["product_id"] == product.id:
                item["quantity"] += quantity
                return True
        
        self.items.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": quantity
        })
        return True
    
    def remove_item(self, product_id: str) -> bool:
        for i, item in enumerate(self.items):
            if item["product_id"] == product_id:
                self.items.pop(i)
                return True
        return False
    
    def get_total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def get_item_count(self) -> int:
        # BUG: Returns len(self.items) which is number of unique products,
        # not total quantity. A cart with 3x Apple and 2x Banana returns 2 instead of 5.
        return len(self.items)
    
    def clear(self):
        self.items = []

class UserProfile:
    def __init__(self, user_id: str, username: str, email: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.preferences = {}
        self.order_history = []
    
    def add_order(self, order_id: str, total: float):
        self.order_history.append({"order_id": order_id, "total": total})
    
    def get_total_spent(self) -> float:
        return sum(order["total"] for order in self.order_history)
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "total_orders": len(self.order_history),
            "total_spent": self.get_total_spent()
        }
