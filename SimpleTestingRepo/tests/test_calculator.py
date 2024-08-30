from calculator import Calculator

def test_sum():
  """Tests the sum method of Calculator class."""
  calc = Calculator()
  assert calc.sum(5, 3) == 8

def test_difference():
  """Tests the difference method of Calculator class."""
  calc = Calculator()
  assert calc.difference(10, 2) == 8

def test_double():
    """Tests the double method of Calculator class."""
    calc = Calculator()
    assert calc.double(5) == 10

def test_get_local_var():
    """Tests the get_local_var method of Calculator class."""
    calc = Calculator()
    assert calc.get_local_var() == "This is a local variable"

async def test_async_multiply():
    """Tests the async_multiply method of Calculator class."""
    calc = Calculator()
    result = await calc.async_multiply(3, 4)
    assert result == 12

# Run the async test using asyncio
asyncio.run(test_async_multiply())
