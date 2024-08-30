import asyncio
from utils.math_utils import add, subtract

class Calculator:
  """A simple calculator class."""

  def __init__(self):
    self.result = 0
    self._local_var = "This is a local variable"

  def sum(self, a: int, b: int) -> int:
    """Calculates the sum of two numbers."""
    self.result = add(a, b)
    return self.result
  
  def difference(self, a, b):
    """Calculates the difference of two numbers."""
    self.result = subtract(a, b)
    return self.result
  
  def double(self, value: int) -> int:
    """Doubles a given value."""
    return self._private_helper_method(value)

  def _private_helper_method(self, value):
    """A private helper method, used by the 'double' method."""
    return value * 2

  async def async_multiply(self, a: int, b: int) -> int:
    """Calculates the product of two numbers asynchronously."""
    await asyncio.sleep(0.1)  # Simulate async operation
    return a * b