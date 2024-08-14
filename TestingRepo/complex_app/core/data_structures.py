from typing import List, Dict, Optional
import threading

# Global Variable 
GLOBAL_DATA = "This is a global variable."

class Node:
    def __init__(self, data):
        self.data = data
        self.next: Optional[Node] = None

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def __str__(self):
        current = self.head
        nodes = []
        while current is not None:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)

    def _get_node_at_index(self, index: int) -> Optional[Node]:
        """Helper function to get the node at a specific index."""
        current = self.head
        count = 0
        while current is not None and count < index:
            current = current.next
            count += 1
        return current

    def insert_at_index(self, data: int, index: int):
        """Inserts a node at a specific index."""
        if index == 0:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
            return

        previous_node = self._get_node_at_index(index - 1)
        if previous_node is None:
            return  # Index out of bounds

        new_node = Node(data)
        new_node.next = previous_node.next
        previous_node.next = new_node

# Decorators
def log_execution_time(func):
    """Decorator to log the execution time of a function."""
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

@log_execution_time
def process_data(data: List[int]):
    """Processes a list of data (example)."""
    for item in data:
        # Some data processing logic
        pass

# Example usage
my_list = LinkedList()
my_list.append(1)
my_list.append(2)
my_list.append(3)
print(my_list)  # Output: 1 -> 2 -> 3

my_list.insert_at_index(4, 1)
print(my_list)  # Output: 1 -> 4 -> 2 -> 3

process_data([1, 2, 3, 4, 5])