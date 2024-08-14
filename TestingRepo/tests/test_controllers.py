from complex_app.controllers.user_controller import UserController
from complex_app.controllers.product_controller import ProductController
from complex_app.controllers.order_controller import OrderController
from complex_app.models.user import User
from complex_app.models.product import Product
import unittest

class TestControllers(unittest.TestCase):
    def test_user_controller(self):
        user_controller = UserController()
        user1 = user_controller.create_user("Alice", "alice@example.com")
        self.assertEqual(user1.username, "Alice")
        self.assertEqual(user_controller.get_user_by_id(user1.id).username, "Alice")

        user_controller.update_user(user1.id, username="Updated Alice")
        self.assertEqual(user_controller.get_user_by_id(user1.id).username, "Updated Alice")

        user_controller.delete_user(user1.id)
        self.assertIsNone(user_controller.get_user_by_id(user1.id))

    def test_product_controller(self):
        product_controller = ProductController()
        product1 = product_controller.create_product("Laptop", 1200.00, "Electronics")
        self.assertEqual(product1.name, "Laptop")
        self.assertEqual(product_controller.get_product_by_id(product1.id).name, "Laptop")

        product_controller.update_product(product1.id, name="Updated Laptop")
        self.assertEqual(product_controller.get_product_by_id(product1.id).name, "Updated Laptop")

        product_controller.delete_product(product1.id)
        self.assertIsNone(product_controller.get_product_by_id(product1.id))

    def test_order_controller(self):
        order_controller = OrderController()
        user1 = User("Alice", "alice@example.com")
        product1 = Product("Laptop", 1200.00, "Electronics")
        order1 = order_controller.create_order(user1, [product1])
        self.assertEqual(order1.user.username, "Alice")
        self.assertEqual(order_controller.get_order_by_id(order1.id).user.username, "Alice")

        order_controller.update_order(order1.id, status="Shipped")
        self.assertEqual(order_controller.get_order_by_id(order1.id).status, "Shipped")

        order_controller.delete_order(order1.id)
        self.assertIsNone(order_controller.get_order_by_id(order1.id))

if __name__ == '__main__':
    unittest.main()