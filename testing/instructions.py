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


   `````````````````````````````````

   1. Understand Directory Structure First
Before providing any response, GitHub Copilot must analyze the existing directory structure to determine where the requested code should be implemented.
The structure includes predefined folders such as:
pages/ - Modular UI pages for Streamlit
static/ - Stores CSS, images, and JavaScript files
data/ - Stores .csv and .xlsx files for processing
core/ - Houses business logic
api/ - Contains Flask API endpoints
server.py - Flask backend for handling API calls
app.py - Streamlit UI entry point
2. Context-Aware Code Suggestions
When answering a query, Copilot must consider all aspects of the existing codebase.
Code should be structured so that API calls between Streamlit and Flask are handled within server.py and routes.py.
If modifications are needed in multiple files, Copilot must explicitly indicate where changes should be applied.
3. Strict Adherence to Code Structure
Any new class, function, or method must strictly follow the format of existing classes and functions.
The placement of functions should align with their purpose (e.g., API logic inside routes.py, data processing inside core/).
Docstrings are mandatory for every function and class to ensure readability and maintainability.
4. API and Backend Integration
Streamlit must communicate with the Flask backend using requests for REST API calls.
API routes should be structured inside routes.py, and all business logic should be inside core/.
Any data fetched via API should be displayed in the UI using st.dataframe() or st.table().
5. Navigation and UI Components
The application must use streamlit_option_menu for navigation.
UI components must align with the organization-approved UI template (color themes, fonts, button styles).
6. Handling Data Files
Any data-related operations (loading, processing, storing) must happen within the data/ folder.
Temporary or processed data should also be stored inside data/.
Flask should expose endpoints to serve data to Streamlit via API calls.
7. Strict Boilerplate Code Generation
Responses must be limited to boilerplate code only, relevant to the specific query.
Copilot must not generate generic Flask or Streamlit templates but instead use the existing structure as a reference.
8. Error Handling and Best Practices
Ensure that all file operations and API calls include proper error handling.
Implement CORS handling in Flask to avoid cross-origin issues.
Use try-except blocks for API calls in server.py.




```````````````````

                         Key Instructions for GitHub Copilot
1. Understand Directory Structure First
Before providing any response, GitHub Copilot must analyze the existing directory structure to determine where the requested code should be implemented.
The structure includes predefined folders such as:
pages/ - Modular UI pages for Streamlit
static/ - Stores CSS, images, and JavaScript files
data/ - Stores .csv and .xlsx files for processing
core/ - Houses business logic
api/ - Contains Flask API endpoints
workers.py - Handles background processing tasks with multithreading
server.py - Flask backend for handling API calls
app.py - Streamlit UI entry point
2. Context-Aware Code Suggestions
When answering a query, Copilot must consider all aspects of the existing codebase.
Code should be structured so that API calls between Streamlit and Flask are handled within server.py and routes.py.
If modifications are needed in multiple files, Copilot must explicitly indicate where changes should be applied.
3. Strict Adherence to Code Structure
Any new class, function, or method must strictly follow the format of existing classes and functions.
The placement of functions should align with their purpose (e.g., API logic inside routes.py, data processing inside core/, multithreading logic inside workers.py).
Docstrings are mandatory for every function and class to ensure readability and maintainability.
4. API, Backend Integration, and Multithreading
Streamlit must communicate with the Flask backend using requests for REST API calls.
API routes should be structured inside routes.py, and all business logic should be inside core/.
workers.py must handle background tasks using Python’s threading or concurrent.futures.
The UI must remain responsive while processing API calls asynchronously.
Long-running processes should be offloaded to background threads or processes.
5. Navigation and UI Components
The application must use streamlit_option_menu for navigation.
UI components must align with the organization-approved UI template (color themes, fonts, button styles).
6. Handling Data Files
Any data-related operations (loading, processing, storing) must happen within the data/ folder.
Temporary or processed data should also be stored inside data/.
Flask should expose endpoints to serve data to Streamlit via API calls.
Streamlit should fetch and process data in a non-blocking manner to avoid UI freezes.
7. Strict Boilerplate Code Generation
Responses must be limited to boilerplate code only, relevant to the specific query.
Copilot must not generate generic Flask or Streamlit templates but instead use the existing structure as a reference.
Any background task must be defined inside workers.py and called properly within the API endpoints.
8. Error Handling and Best Practices
Ensure that all file operations and API calls include proper error handling.
Implement CORS handling in Flask to avoid cross-origin issues.
Use try-except blocks for API calls in server.py.
When using multithreading, ensure that shared resources are accessed safely to avoid race conditions.
Expected Behavior
GitHub Copilot should only return responses based on the directory structure and pre-defined code standards.
If a query requires new files or modifications to multiple existing files, Copilot should provide step-by-step implementation guidance.
Any deviation from the predefined template should be flagged as an error.
By following these instructions, GitHub Copilot ensures a structured, consistent, and maintainable codebase while leveraging Flask's multithreading capabilities for high-performance applications.


```````````````````````

                         # Business Requirements Document  
## Project: Streamlit File Validation and Upload Tool  
## Version: 1.0  
## Date: [YYYY-MM-DD]  
## Author: [Your Name / Team]  
## Stakeholders: [Architects, Tech Leads, Business Analysts]  
---------------------------------------------------------------

## 1. Overview  
The Streamlit File Validation and Upload Tool enables users to upload a `CSV` or `XLSX` file via a Streamlit UI. The tool validates and cleans data before storing it in a Snowflake table. It includes multiple pages for user interaction and automatic processing.

---------------------------------------------------------------

## 2. Functional Requirements  

### 2.1 Streamlit UI Pages  
- **Home Page:** Displays an introduction to the tool.  
- **Upload Page:** Allows users to upload files and select the data source.  
- **Algorithm Page:** Executes data validation and cleaning operations.  

### 2.2 Upload Page Requirements  
- Users should be able to upload a file (`CSV` or `XLSX`).  
- A **radio button** should allow users to choose the data source:  
  - **Option 1:** Upload from local system.  
  - **Option 2:** Read from Snowflake (`schema.table_name`).  
- Once uploaded, the file should be displayed in a **pandas DataFrame** format.  
- The upload page should have a **"Process Data"** button to trigger the validation algorithm.

### 2.3 Algorithm Page (Data Validation & Cleaning)  
- The uploaded dataset should undergo the following transformations:  
  1. **Missing Value Handling:**  
     - If **numerical with outliers** → Fill with `median`.  
     - If **numerical without outliers** → Fill with `mean`.  
     - If **categorical** → Fill with `mode`.  
  2. **Data Type Validation:** Ensure all columns have correct data types.  
  3. **Range Validation:** Check if numerical columns are within predefined ranges.  
  4. **Date Validation:** Ensure date fields follow the correct format (`YYYY-MM-DD`).  
  5. **Duplicate Removal:** Drop duplicate rows from the dataset.  
  6. **Schema Mapping:** Ensure the cleaned dataset conforms to Snowflake schema before insertion.  
  7. **Store cleaned data in Snowflake (`schema.table_name`).**  

---------------------------------------------------------------

## 3. Non-Functional Requirements  
- The UI should be **responsive** and support **drag-and-drop** file uploads.  
- Data processing should handle files up to **50MB** efficiently.  
- The tool should be optimized for **fast execution (< 10 sec for 1M rows).**  
- **Logging and Debugging** mechanisms must be implemented.  

---------------------------------------------------------------

## 4. Error Handling & Logging  
- Use **try-except** blocks for all functions and log errors in JSON format.  
- **Validation Logs:**  
  - If a column has missing values, log `"missing_values": ["column_name"]`.  
  - If a numerical column exceeds allowed range, log `"out_of_range": ["column_name"]`.  
  - If an invalid data type is found, log `"invalid_dtype": {"column_name": "expected_type"}`.  
- **System Logs:**  
  - Log file read/write errors.  
  - Log failed Snowflake inserts with error details.  

---------------------------------------------------------------

## 5. Expected Output  
- Cleaned dataset stored in Snowflake table `schema.table_name`.  
- Validation errors stored in `logs/validation_log.json`.  
- Debug logs stored in `logs/debug_log.json`.  

---------------------------------------------------------------

## 6. Future Enhancements  
- Add support for **Google Drive / S3 uploads**.  
- Enable **custom validation rules** via UI.  
- Implement **real-time data streaming** from Snowflake.

---------------------------------------------------------------

