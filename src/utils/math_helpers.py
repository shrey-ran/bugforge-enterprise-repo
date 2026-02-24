"""Mathematical and statistical helper functions."""
import math

def calculate_average(numbers: list) -> float:
    """Calculate the arithmetic mean of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

def calculate_median(numbers: list) -> float:
    """Calculate the median of a list of numbers."""
    if not numbers:
        return 0.0
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]

def calculate_standard_deviation(numbers: list) -> float:
    """Calculate the population standard deviation."""
    if len(numbers) < 2:
        return 0.0
    avg = calculate_average(numbers)
    variance = sum((x - avg) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate the percentage change between two values.
    
    Formula: ((new - old) / old) * 100
    A positive result means increase, negative means decrease.
    """
    if old_value == 0:
        return 0.0
    # BUG: Formula is inverted — (old - new) instead of (new - old).
    # This returns NEGATIVE when value increases and POSITIVE when it decreases.
    return ((old_value - new_value) / old_value) * 100

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between a minimum and maximum."""
    return max(min_val, min(value, max_val))

def round_to_nearest(value: float, step: float) -> float:
    """Round a value to the nearest step increment."""
    return round(value / step) * step

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
