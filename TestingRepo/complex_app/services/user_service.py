from typing import List, Optional
from complex_app.models.user import User
from complex_app.core.logger import AppLogger

class UserService:
    def __init__(self):
        self.logger = AppLogger()
        self.users: List[User] = []

    def create_user(self, username: str, email: str) -> User:
        """Creates a new user."""
        new_user = User(username, email)
        self.users.append(new_user)
        self.logger.info(f"User created: {username}")
        return new_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieves a user by their ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        self.logger.warning(f"User with ID {user_id} not found.")
        return None

    def get_users(self) -> List[User]:
        """Retrieves all users."""
        return self.users

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None) -> bool:
        """Updates a user's information."""
        for user in self.users:
            if user.id == user_id:
                if username is not None:
                    user.username = username
                if email is not None:
                    user.email = email
                self.logger.info(f"User {user_id} updated.")
                return True
        self.logger.warning(f"User with ID {user_id} not found.")
        return False

    def delete_user(self, user_id: int) -> bool:
        """Deletes a user."""
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                self.logger.info(f"User {user_id} deleted.")
                return True
        self.logger.warning(f"User with ID {user_id} not found.")
        return False