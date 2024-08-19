from calculator import Calculator

def test_sum():
  """Tests the sum method of Calculator class."""
  calc = Calculator()
  assert calc.sum(5, 3) == 8

def test_difference():
  """Tests the difference method of Calculator class."""
  calc = Calculator()
  assert calc.difference(10, 2) == 8