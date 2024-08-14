from typing import Callable, Any , List 
import time , random

def log_execution_time(func: Callable) -> Callable:
    """Decorator to log the execution time of a function."""
    import time
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def retry(attempts: int = 3, delay: float = 0.5):
    """Decorator to retry a function for a specified number of attempts."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@log_execution_time
def process_data(data: List[int]):
    """Processes a list of data (example)."""
    # Some data processing logic (simulated error)
    if random.randint(0, 10) > 8:
        raise ValueError("Simulated error in data processing.")

@retry(attempts=5, delay=1)
def perform_operation(data: List[int]):
    """Performs an operation that may fail (example)."""
    process_data(data)
    print("Operation successful.")

# Example usage
process_data([1, 2, 3, 4, 5])  # May fail and retry with the retry decorator
perform_operation([1, 2, 3, 4, 5])  # Retry on failure