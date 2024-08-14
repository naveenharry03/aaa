from complex_app.services.product_service import ProductService
from typing import Optional

class ProductController:
    def __init__(self):
        self.product_service = ProductService()

    def create_product(self, name: str, price: float, category: str):
        """Creates a new product."""
        return self.product_service.create_product(name, price, category)

    def get_product_by_id(self, product_id: int):
        """Retrieves a product by its ID."""
        return self.product_service.get_product_by_id(product_id)

    def get_products(self):
        """Retrieves all products."""
        return self.product_service.get_products()

    def update_product(self, product_id: int, name: Optional[str] = None, price: Optional[float] = None, category: Optional[str] = None):
        """Updates a product's information."""
        return self.product_service.update_product(product_id, name, price, category)

    def delete_product(self, product_id: int):
        """Deletes a product."""
        return self.product_service.delete_product(product_id)