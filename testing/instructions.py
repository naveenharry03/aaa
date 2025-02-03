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




# System Instructions for Basic Streamlit UI

## Objective
This document provides strict guidelines for GitHub Copilot to generate Streamlit-based boilerplate code **only** based on the pre-defined UI structure. The responses should be context-aware, ensuring that all generated code fits within the existing structure.

## Key Instructions for GitHub Copilot
1. **Understand Directory Structure First**  
   - Before providing any response, GitHub Copilot must analyze the existing directory structure to determine where the requested code should be implemented.
   - The structure includes predefined folders such as `pages/`, `static/`, `data/`, and `core/`, each serving a specific purpose.
   
2. **Context-Aware Code Suggestions**  
   - When answering a query, Copilot must consider all aspects of the codebase, ensuring that the suggested code aligns with existing patterns.
   - If modifications are needed in multiple files, Copilot must explicitly indicate where changes should be applied.

3. **Strict Adherence to Code Structure**  
   - Any new **class**, **function**, or **method** must strictly follow the format of existing classes and functions.
   - The placement of functions should align with their purpose (e.g., utility functions inside `utils/`, core logic inside `core/`).
   - **Docstrings are mandatory** for every function and class to ensure readability and maintainability.

4. **Navigation and UI Components**  
   - The application must use `streamlit_option_menu` for navigation.
   - All UI components must align with the pre-defined organization-approved UI template (color themes, fonts, button styles).

5. **Handling Data Files**  
   - Any data-related operations (loading, processing, storing) must happen within the `data/` folder.
   - Temporary or processed data should also be stored inside `data/` and not scattered in other directories.
   - All `.csv`, `.xlsx`, and other data-related files must be read from and written to the `data/` directory.

6. **Strict Boilerplate Code Generation**  
   - Responses must be limited to **boilerplate code only**, relevant to the specific query.
   - Copilot must **not** generate generic Streamlit templates but instead use the existing structure as a reference.

7. **Error Handling and Best Practices**  
   - Ensure that all file operations include error handling.
   - Avoid unnecessary global variables; prefer function encapsulation.

## Expected Behavior  
- GitHub Copilot should **only** return responses based on the directory structure and pre-defined code standards.  
- If a query requires new files or modifications to multiple existing files, Copilot should provide step-by-step implementation guidance.  
- Any deviation from the predefined template should be flagged as an error.  

By following these instructions, GitHub Copilot ensures a structured, consistent, and maintainable codebase.

