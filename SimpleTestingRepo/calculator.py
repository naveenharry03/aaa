from utils.math_utils import add, subtract

class Calculator:
  """A simple calculator class."""

  def __init__(self):
    self.result = 0

  def sum(self, a, b):
    """Calculates the sum of two numbers."""
    self.result = add(a, b)
    return self.result

  def difference(self, a, b):
    """Calculates the difference of two numbers."""
    self.result = subtract(a, b)
    return self.result