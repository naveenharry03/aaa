from fastapi import FastAPI
from calculator import Calculator
import uvicorn
import asyncio

# GLOBAL VARIABLE
GLOBAL_CONFIG = {
    "api_version": "1.0.0",
    "default_currency": "USD"
}

app = FastAPI()

@app.get("/sum/{a}/{b}")
def calculate_sum(a: int, b: int):
    """Calculates the sum of two numbers."""
    calc = Calculator()
    return {"result": calc.sum(a, b), "api_version": GLOBAL_CONFIG["api_version"]}

@app.get("/difference/{a}/{b}")
def calculate_difference(a: int, b: int):
    """Calculates the difference of two numbers."""
    calc = Calculator()
    return {"result": calc.difference(a, b)}

@app.get("/multiply/{a}/{b}")
async def calculate_multiply(a: int, b: int):
    """Calculates the product of two numbers asynchronously."""
    calc = Calculator()
    return {"result": await calc.async_multiply(a, b)}

@app.get("/double/{value}")
def calculate_double(value: int):
    """Doubles the given value."""
    calc = Calculator()
    return {"result": calc.double(value)}

@app.get("/")
async def root():  
    return {"message": "Welcome to the calculator API!", "api_version": GLOBAL_CONFIG["api_version"]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info") 