from complex_app.services.user_service import UserService
from typing import Optional

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def create_user(self, username: str, email: str):
        """Creates a new user."""
        return self.user_service.create_user(username, email)

    def get_user_by_id(self, user_id: int):
        """Retrieves a user by their ID."""
        return self.user_service.get_user_by_id(user_id)

    def get_users(self):
        """Retrieves all users."""
        return self.user_service.get_users()

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None):
        """Updates a user's information."""
        return self.user_service.update_user(user_id, username, email)

    def delete_user(self, user_id: int):
        """Deletes a user."""
        return self.user_service.delete_user(user_id)