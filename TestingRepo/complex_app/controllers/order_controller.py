from complex_app.services.order_service import OrderService
from typing import Optional
from complex_app.models.user import User
from complex_app.models.product import Product
from typing import List

class OrderController:
    def __init__(self):
        self.order_service = OrderService()

    def create_order(self, user: User, products: List[Product]):
        """Creates a new order."""
        return self.order_service.create_order(user, products)

    def get_order_by_id(self, order_id: int):
        """Retrieves an order by its ID."""
        return self.order_service.get_order_by_id(order_id)

    def get_orders(self):
        """Retrieves all orders."""
        return self.order_service.get_orders()

    def update_order(self, order_id: int, status: Optional[str] = None):
        """Updates an order's status."""
        return self.order_service.update_order(order_id, status)

    def delete_order(self, order_id: int):
        """Deletes an order."""
        return self.order_service.delete_order(order_id)