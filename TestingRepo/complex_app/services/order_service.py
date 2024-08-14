from typing import List, Optional
from complex_app.models.order import Order
from complex_app.models.product import Product
from complex_app.models.user import User
from complex_app.core.logger import AppLogger

class OrderService:
    def __init__(self):
        self.logger = AppLogger()
        self.orders: List[Order] = []

    def create_order(self, user: User, products: List[Product]) -> Order:
        """Creates a new order."""
        new_order = Order(user, products)
        self.orders.append(new_order)
        self.logger.info(f"Order created for user: {user.username}")
        return new_order

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Retrieves an order by its ID."""
        for order in self.orders:
            if order.id == order_id:
                return order
        self.logger.warning(f"Order with ID {order_id} not found.")
        return None

    def get_orders(self) -> List[Order]:
        """Retrieves all orders."""
        return self.orders

    def update_order(self, order_id: int, status: Optional[str] = None) -> bool:
        """Updates an order's status."""
        for order in self.orders:
            if order.id == order_id:
                if status is not None:
                    order.status = status
                self.logger.info(f"Order {order_id} updated.")
                return True
        self.logger.warning(f"Order with ID {order_id} not found.")
        return False

    def delete_order(self, order_id: int) -> bool:
        """Deletes an order."""
        for i, order in enumerate(self.orders):
            if order.id == order_id:
                del self.orders[i]
                self.logger.info(f"Order {order_id} deleted.")
                return True
        self.logger.warning(f"Order with ID {order_id} not found.")
        return False