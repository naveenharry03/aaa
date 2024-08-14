# Complex Application - Code Analyzer Test Repository

This repository is designed for testing a code analyzer by providing a complex Python application with various code structures and concepts.

## File Structure and Concepts

Here's a breakdown of the files and the concepts they illustrate:

**complex_app:**

- **core:**
  - **data_structures.py:**
    - **Classes:** `Node`, `LinkedList`, `Graph`
    - **Functions:** `append`, `__str__`, `_get_node_at_index`, `insert_at_index` (helper)
    - **Sub-functions (Helper Functions):**  `_get_node_at_index`
    - **Decorators:** `log_execution_time` 
    - **Global Variables:** `GLOBAL_DATA`
    - **Type Annotations:**  `List`, `Dict`, `Optional`, `Node`
    - **Data Structures:** `List`, `Dict` 
  - **utils.py:**
    - **Functions:** `generate_random_string`, `format_date`, `is_valid_email`, `apply_discount`, `_get_random_value` (helper)
    - **Sub-functions (Helper Functions):** `_get_random_value`
    - **Decorators:** `log_function_call` 
    - **Global Variables:** `GLOBAL_CONSTANT`
    - **Type Annotations:** `List`, `int`, `str`, `float`, `Callable`, `Tuple`, `Any`
    - **Imports:** `random`, `datetime` 
  - **logger.py:**
    - **Class:** `AppLogger` 
    - **Functions:**  `info`, `debug`, `warning`, `error`, `critical`
    - **Type Annotations:** `Union`, `Any`
    - **Imports:** `logging`
  - **decorators.py:**
    - **Functions:** `log_execution_time`, `retry` (decorator factory)
    - **Type Annotations:** `Callable`, `Any`

- **services:**
  - **user_service.py:**
    - **Class:** `UserService`
    - **Functions:** `create_user`, `get_user_by_id`, `get_users`, `update_user`, `delete_user`
    - **Type Annotations:** `List`, `Optional`, `User`
    - **Imports:** `User`, `AppLogger` 
  - **product_service.py:**
    - **Class:** `ProductService`
    - **Functions:** `create_product`, `get_product_by_id`, `get_products`, `update_product`, `delete_product`
    - **Type Annotations:** `List`, `Optional`, `Product`
    - **Imports:** `Product`, `AppLogger` 
  - **order_service.py:**
    - **Class:** `OrderService`
    - **Functions:** `create_order`, `get_order_by_id`, `get_orders`, `update_order`, `delete_order`
    - **Type Annotations:** `List`, `Optional`, `Order`, `Product`, `User`
    - **Imports:** `Order`, `Product`, `User`, `AppLogger`

- **models:**
  - **user.py:**
    - **Class:** `User`
    - **Functions:** `__init__`, `__repr__`
    - **Type Annotations:** `Optional`, `str`
    - **Imports:** `uuid` 
  - **product.py:**
    - **Class:** `Product`
    - **Functions:** `__init__`, `__repr__`
    - **Type Annotations:** `Optional`, `str`, `float`
    - **Imports:** `uuid` 
  - **order.py:**
    - **Class:** `Order`
    - **Functions:** `__init__`, `__repr__`
    - **Type Annotations:** `List`, `Product`, `User`
    - **Imports:** `uuid`, `Product`, `User`

- **controllers:**
  - **user_controller.py:**
    - **Class:** `UserController`
    - **Functions:** `create_user`, `get_user_by_id`, `get_users`, `update_user`, `delete_user`
    - **Type Annotations:** `Optional`
    - **Imports:** `UserService`
  - **product_controller.py:**
    - **Class:** `ProductController`
    - **Functions:** `create_product`, `get_product_by_id`, `get_products`, `update_product`, `delete_product`
    - **Type Annotations:** `Optional`, `float`
    - **Imports:** `ProductService`
  - **order_controller.py:**
    - **Class:** `OrderController`
    - **Functions:** `create_order`, `get_order_by_id`, `get_orders`, `update_order`, `delete_order`
    - **Type Annotations:** `Optional`, `List`, `Product`, `User`
    - **Imports:** `OrderService`

- **main.py:**
  - **Functions:** `main`
  - **Type Annotations:** None (in this example)
  - **Imports:** `UserController`, `ProductController`, `OrderController`, `User`, `Product`

**tests:**

- **test_core.py:**
  - **Class:** `TestCore` (unittest)
  - **Functions:** `test_linked_list`, `test_graph`, `test_generate_random_string`, `test_format_date`, `test_is_valid_email`
  - **Type Annotations:** None (in this example)
  - **Imports:** `LinkedList`, `Node`, `Graph`, `generate_random_string`, `format_date`, `is_valid_email`, `unittest` 
- **test_services.py:**
  - **Class:** `TestServices` (unittest)
  - **Functions:** `test_user_service`, `test_product_service`, `test_order_service`
  - **Type Annotations:** None (in this example)
  - **Imports:** `UserService`, `ProductService`, `OrderService`, `User`, `Product`, `unittest`
- **test_models.py:**
  - **Class:** `TestModels` (unittest)
  - **Functions:** `test_user_model`, `test_product_model`, `test_order_model`
  - **Type Annotations:** None (in this example)
  - **Imports:** `User`, `Product`, `Order`, `unittest`
- **test_controllers.py:**
  - **Class:** `TestControllers` (unittest)
  - **Functions:** `test_user_controller`, `test_product_controller`, `test_order_controller`
  - **Type Annotations:** None (in this example)
  - **Imports:** `UserController`, `ProductController`, `OrderController`, `User`, `Product`, `unittest`
- **test_main.py:**
  - **Class:** `TestMain` (unittest)
  - **Functions:** `test_main_function`
  - **Type Annotations:** None (in this example)
  - **Imports:** `main`, `unittest`, `logging`

**requirements.txt:**

- **List of Dependencies:**  `typing`, `uuid`, `datetime`, `unittest`, `logging`

## Running Tests

You can run the tests using the following command:

```bash
python -m unittest discover -s tests
