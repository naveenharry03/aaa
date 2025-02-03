# Python Code Style Guidelines

## Directory Structure

```
root/
├── src/
│   ├── core/              # Core application logic
│   ├── models/            # Data models and schemas
│   ├── services/          # Business logic and services
│   ├── utils/             # Utility functions
│   ├── config/            # Configuration files
│   └── api/               # API endpoints (if applicable)
├── tests/                 # Test files
├── docs/                  # Documentation
└── scripts/              # Utility scripts
```

## Code Organization Guidelines

1. **Module Organization**
   - One class per file (when possible)
   - Related functions in thematic modules
   - Keep modules focused and cohesive

2. **File Naming**
   - Use lowercase with underscores
   - Models: `user_model.py`
   - Utils: `string_utils.py`
   - Tests: `test_user_model.py`

3. **Code Templates**

### Class Template
```python
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class ClassName:
    """
    Class description.

    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """
    attr1: str
    attr2: Optional[int] = None

    def method_name(self, param1: str) -> bool:
        """
        Method description.

        Args:
            param1: Parameter description

        Returns:
            Description of return value
        """
        pass
```

### Function Template
```python
from typing import Dict, Any

def function_name(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Function description.

    Args:
        param1: First parameter description
        param2: Second parameter description (optional)

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
    """
    pass
```

## Coding Standards

1. **Python Version**
   - Use Python 3.8+ features
   - Use type hints
   - Use f-strings for string formatting

2. **Style Guide**
   - Follow PEP 8
   - Maximum line length: 88 characters (Black formatter)
   - Use meaningful variable names
   - Use docstrings for documentation

3. **Best Practices**
   - Use list/dict comprehensions when appropriate
   - Prefer explicit over implicit
   - Use context managers (with statements)
   - Handle exceptions properly

4. **Type Hints**
   - Use type hints for all function parameters
   - Use Optional[] for nullable types
   - Use Union[] for multiple types
   - Use TypeVar for generics

5. **Testing**
   - Write unit tests using pytest
   - Use fixtures for test setup
   - Mock external dependencies
   - Aim for high test coverage

## Documentation

1. **Docstrings**
   - Use Google style docstrings
   - Document parameters and return types
   - Document exceptions
   - Include usage examples for complex functions

2. **Comments**
   - Explain complex algorithms
   - Document business rules
   - Add TODO comments for future work

## Project Setup

1. **Dependencies**
   - Use requirements.txt or pyproject.toml
   - Pin dependency versions
   - Separate dev dependencies

2. **Environment**
   - Use virtual environments
   - Use .env files for configuration
   - Document environment setup

## Code Quality Tools

1. **Linting and Formatting**
   - Use Black for formatting
   - Use isort for import sorting
   - Use flake8 for linting
   - Use mypy for type checking

2. **Pre-commit Hooks**
   - Run formatters
   - Run linters
   - Run type checkers
   - Run tests

## Error Handling

1. **Exceptions**
   - Create custom exceptions when needed
   - Use specific exception types
   - Handle exceptions at appropriate levels
   - Log errors properly

## Performance Guidelines

1. **Optimization**
   - Use generators for large datasets
   - Profile code when needed
   - Use appropriate data structures
   - Consider memory usage

2. **Async Programming**
   - Use asyncio when appropriate
   - Handle coroutines properly
   - Use async context managers
   - Consider thread safety


      
``````````````````````````

      Directory Awareness:

Copilot must recognize the predefined directory structure before generating any code.

It must analyze the existing folder and file purposes before suggesting changes.

When modifying or adding code, it should ensure the update aligns with the correct module.

Code Integration & Context Retention:

All generated responses must align with the entire codebase context.

Instead of providing isolated code snippets, Copilot should suggest exact file locations for implementation.

For any function/class modifications, it must analyze the existing structure and provide updates in the correct location.

Boilerplate Code Standards:

Copilot must follow the pre-defined template style for all functions and classes.

Every class must include an appropriate constructor (__init__) and adhere to existing design patterns.

All functions should include detailed docstrings explaining parameters, return values, and functionality.

New Class & Function Creation Rules:

If a new class is required, it must adhere to the existing class structure.

Function signatures, arguments, and return types should match the overall project conventions.

Any helper functions should be placed inside common/utils.py unless they are core features.

Changes & Enhancements:

When modifying existing files, Copilot must not overwrite unrelated code.

It should add new logic in an incremental manner, ensuring that it seamlessly integrates with current functionality.

If a significant update is required, it should generate a structured explanation along with the new code.

Strict Response Format:

Copilot must return responses only in boilerplate code format.

No additional explanations or unrelated suggestions should be included.

Responses must be fully executable and include inline comments where necessary.
