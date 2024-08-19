from fastapi import FastAPI
from calculator import Calculator
import uvicorn

app = FastAPI()

@app.get("/sum/{a}/{b}")
def calculate_sum(a: int, b: int):
    """Calculates the sum of two numbers."""
    calc = Calculator()
    return {"result": calc.sum(a, b)}

@app.get("/difference/{a}/{b}")
def calculate_difference(a: int, b: int):
    """Calculates the difference of two numbers."""
    calc = Calculator()
    return {"result": calc.difference(a, b)}

@app.get("/")
async def root():
    return {"message": "Welcome to the calculator API!"} 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info") 