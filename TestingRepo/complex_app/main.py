from complex_app.controllers.user_controller import UserController
from complex_app.controllers.product_controller import ProductController
from complex_app.controllers.order_controller import OrderController
from complex_app.models.user import User
from complex_app.models.product import Product

def main():
    user_controller = UserController()
    product_controller = ProductController()
    order_controller = OrderController()

    # Create users
    user1 = user_controller.create_user("Alice", "alice@example.com")
    user2 = user_controller.create_user("Bob", "bob@example.com")

    # Create products
    product1 = product_controller.create_product("Laptop", 1200.00, "Electronics")
    product2 = product_controller.create_product("Mouse", 20.00, "Computer Peripherals")

    # Create orders
    order1 = order_controller.create_order(user1, [product1, product2])

    # Retrieve users
    users = user_controller.get_users()
    print("All Users:")
    for user in users:
        print(user)

    # Retrieve products
    products = product_controller.get_products()
    print("All Products:")
    for product in products:
        print(product)

    # Retrieve orders
    orders = order_controller.get_orders()
    print("All Orders:")
    for order in orders:
        print(order)

if __name__ == "__main__":
    main()