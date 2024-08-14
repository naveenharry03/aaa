from typing import Optional
import uuid

class User:
    def __init__(self, username: str, email: str):
        self.id: str = str(uuid.uuid4())  # Generate a unique ID
        self.username: str = username
        self.email: str = email

    def __repr__(self):
        return f"User(id='{self.id}', username='{self.username}', email='{self.email}')"

# Example usage
user1 = User("Alice", "alice@example.com")
print(user1)  # Output: User(id='...', username='Alice', email='alice@example.com')