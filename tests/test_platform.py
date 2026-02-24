"""Test suite for the enterprise platform."""
import pytest
from src.utils.math_helpers import calculate_percentage_change, calculate_average
from src.services.search import calculate_trending_score
from src.auth.session import validate_token, generate_session_token
from src.api.orders import apply_discount
from src.models.product import ShoppingCart, Product

class TestMathHelpers:
    def test_percentage_change_increase(self):
        """Stock went from $100 to $150 = 50% increase."""
        result = calculate_percentage_change(100, 150)
        assert result == 50.0, f"Expected 50.0, got {result}"
    
    def test_percentage_change_decrease(self):
        """Stock went from $200 to $150 = -25% decrease."""
        result = calculate_percentage_change(200, 150)
        assert result == -25.0, f"Expected -25.0, got {result}"

class TestTrendingScore:
    def test_trending_normalization(self):
        """Products listed for longer should have LOWER trending scores, not higher."""
        score_1day = calculate_trending_score(views=100, purchases=10, days_listed=1)
        score_30days = calculate_trending_score(views=100, purchases=10, days_listed=30)
        assert score_1day > score_30days, f"1-day score ({score_1day}) should be > 30-day score ({score_30days})"

class TestSessionExpiry:
    def test_token_expires(self):
        """Old tokens should be invalid."""
        import time
        token = generate_session_token("user_1")
        # Manually backdate the session
        from src.auth.session import _active_sessions, TOKEN_EXPIRY
        _active_sessions[token]["created_at"] = time.time() - TOKEN_EXPIRY - 100
        assert validate_token(token) == False, "Expired token should be invalid"

class TestDiscount:
    def test_percentage_discount(self):
        """A 20% discount on $100 should give $80, not $20."""
        codes = {"SAVE20": {"type": "percentage", "value": 20}}
        result = apply_discount(100.0, "SAVE20", codes)
        assert result == 80.0, f"Expected 80.0, got {result}"

class TestShoppingCart:
    def test_item_count_with_quantities(self):
        """Cart with 3x Apple + 2x Banana should report 5 total items."""
        cart = ShoppingCart("user_1")
        apple = Product("1", "Apple", 1.0, "fruit", stock=10)
        banana = Product("2", "Banana", 0.5, "fruit", stock=10)
        cart.add_item(apple, 3)
        cart.add_item(banana, 2)
        assert cart.get_item_count() == 5, f"Expected 5, got {cart.get_item_count()}"
