from complex_app.services.user_service import UserService
from complex_app.services.product_service import ProductService
from complex_app.services.order_service import OrderService
from complex_app.models.user import User
from complex_app.models.product import Product
import unittest

class TestServices(unittest.TestCase):
    def test_user_service(self):
        user_service = UserService()
        user1 = user_service.create_user("Alice", "alice@example.com")
        self.assertEqual(user1.username, "Alice")
        self.assertEqual(user_service.get_user_by_id(user1.id).username, "Alice")

        user_service.update_user(user1.id, username="Updated Alice")
        self.assertEqual(user_service.get_user_by_id(user1.id).username, "Updated Alice")

        user_service.delete_user(user1.id)
        self.assertIsNone(user_service.get_user_by_id(user1.id))

    def test_product_service(self):
        product_service = ProductService()
        product1 = product_service.create_product("Laptop", 1200.00, "Electronics")
        self.assertEqual(product1.name, "Laptop")
        self.assertEqual(product_service.get_product_by_id(product1.id).name, "Laptop")

        product_service.update_product(product1.id, name="Updated Laptop")
        self.assertEqual(product_service.get_product_by_id(product1.id).name, "Updated Laptop")

        product_service.delete_product(product1.id)
        self.assertIsNone(product_service.get_product_by_id(product1.id))

    def test_order_service(self):
        order_service = OrderService()
        user1 = User("Alice", "alice@example.com")
        product1 = Product("Laptop", 1200.00, "Electronics")
        order1 = order_service.create_order(user1, [product1])
        self.assertEqual(order1.user.username, "Alice")
        self.assertEqual(order_service.get_order_by_id(order1.id).user.username, "Alice")

        order_service.update_order(order1.id, status="Shipped")
        self.assertEqual(order_service.get_order_by_id(order1.id).status, "Shipped")

        order_service.delete_order(order1.id)
        self.assertIsNone(order_service.get_order_by_id(order1.id))

if __name__ == '__main__':
    unittest.main()