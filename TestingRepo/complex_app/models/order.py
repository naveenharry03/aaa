from typing import List
import uuid
from complex_app.models.product import Product
from complex_app.models.user import User

class Order:
    def __init__(self, user: User, products: List[Product]):
        self.id: str = str(uuid.uuid4())  # Generate a unique ID
        self.user: User = user
        self.products: List[Product] = products
        self.status: str = "Pending"  # Default order status

    def __repr__(self):
        return f"Order(id='{self.id}', user='{self.user.username}', products='{self.products}', status='{self.status}')"

# Example usage
user1 = User("Alice", "alice@example.com")
product1 = Product("Laptop", 1200.00, "Electronics")
product2 = Product("Mouse", 20.00, "Computer Peripherals")

order1 = Order(user1, [product1, product2])
print(order1)  # Output: Order(id='...', user='Alice', products='[Product(id='...', name='Laptop', price=1200.0, category='Electronics'), Product(id='...', name='Mouse', price=20.0, category='Computer Peripherals')]', status='Pending')