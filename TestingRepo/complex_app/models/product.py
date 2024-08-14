from typing import Optional
import uuid

class Product:
    def __init__(self, name: str, price: float, category: str):
        self.id: str = str(uuid.uuid4())  # Generate a unique ID
        self.name: str = name
        self.price: float = price
        self.category: str = category

    def __repr__(self):
        return f"Product(id='{self.id}', name='{self.name}', price={self.price}, category='{self.category}')"

# Example usage
product1 = Product("Laptop", 1200.00, "Electronics")
print(product1)  # Output: Product(id='...', name='Laptop', price=1200.0, category='Electronics')