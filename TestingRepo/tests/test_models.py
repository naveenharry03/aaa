from complex_app.models.user import User
from complex_app.models.product import Product
from complex_app.models.order import Order
import unittest

class TestModels(unittest.TestCase):
    def test_user_model(self):
        user1 = User("Alice", "alice@example.com")
        self.assertEqual(user1.username, "Alice")
        self.assertEqual(user1.email, "alice@example.com")

    def test_product_model(self):
        product1 = Product("Laptop", 1200.00, "Electronics")
        self.assertEqual(product1.name, "Laptop")
        self.assertEqual(product1.price, 1200.00)
        self.assertEqual(product1.category, "Electronics")

    def test_order_model(self):
        user1 = User("Alice", "alice@example.com")
        product1 = Product("Laptop", 1200.00, "Electronics")
        order1 = Order(user1, [product1])
        self.assertEqual(order1.user.username, "Alice")
        self.assertEqual(order1.products[0].name, "Laptop")

if __name__ == '__main__':
    unittest.main()