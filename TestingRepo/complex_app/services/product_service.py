from typing import List, Optional
from complex_app.models.product import Product
from complex_app.core.logger import AppLogger

class ProductService:
    def __init__(self):
        self.logger = AppLogger()
        self.products: List[Product] = []

    def create_product(self, name: str, price: float, category: str) -> Product:
        """Creates a new product."""
        new_product = Product(name, price, category)
        self.products.append(new_product)
        self.logger.info(f"Product created: {name}")
        return new_product

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieves a product by its ID."""
        for product in self.products:
            if product.id == product_id:
                return product
        self.logger.warning(f"Product with ID {product_id} not found.")
        return None

    def get_products(self) -> List[Product]:
        """Retrieves all products."""
        return self.products

    def update_product(self, product_id: int, name: Optional[str] = None, price: Optional[float] = None, category: Optional[str] = None) -> bool:
        """Updates a product's information."""
        for product in self.products:
            if product.id == product_id:
                if name is not None:
                    product.name = name
                if price is not None:
                    product.price = price
                if category is not None:
                    product.category = category
                self.logger.info(f"Product {product_id} updated.")
                return True
        self.logger.warning(f"Product with ID {product_id} not found.")
        return False

    def delete_product(self, product_id: int) -> bool:
        """Deletes a product."""
        for i, product in enumerate(self.products):
            if product.id == product_id:
                del self.products[i]
                self.logger.info(f"Product {product_id} deleted.")
                return True
        self.logger.warning(f"Product with ID {product_id} not found.")
        return False