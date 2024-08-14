import random
import datetime
from typing import Any, Callable, Tuple

# Global Variable 
GLOBAL_CONSTANT = 10

def generate_random_string(length: int = 10) -> str:
    """Generates a random string of specified length."""
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(characters) for i in range(length))

def format_date(date_obj: datetime.datetime) -> str:
    """Formats a date object into a specific string format."""
    return date_obj.strftime("%Y-%m-%d")

def is_valid_email(email: str) -> bool:
    """Checks if an email string is valid (basic validation)."""
    return "@" in email and "." in email

def apply_discount(price: float, discount: float) -> float:
    """Applies a discount to a price."""
    return price - (price * discount / 100)

def _get_random_value(min: int, max: int) -> int:
    """Helper function for generating random values."""
    return random.randint(min, max)

# Decorators
def log_function_call(func: Callable) -> Callable:
    """Decorator to log function calls."""
    def wrapper(*args, **kwargs) -> Any:
        print(f"Calling function: {func.__name__} with arguments: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

@log_function_call
def multiply_numbers(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

# Example usage
random_string = generate_random_string(15)
print(random_string)  # Output: random string of length 15

formatted_date = format_date(datetime.datetime.now())
print(formatted_date)  # Output: current date in YYYY-MM-DD format

is_valid = is_valid_email("john.doe@example.com")
print(is_valid)  # Output: True

discounted_price = apply_discount(100.00, 10.00)
print(discounted_price)  # Output: 90.00

multiply_numbers(5, 3)  # Output: logs the function call and result