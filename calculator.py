# give me the complate fastapi code for calcualtor

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Literal

app = FastAPI(
    title="Calculator API",
    description="Simple and Advanced Calculator using FastAPI",
    version="1.0"
)

# ====================== MODELS ======================
class CalculatorRequest(BaseModel):
    num1: float
    num2: float
    operation: Literal["add", "sub", "multiply", "divide"]


class AdvancedCalculatorRequest(BaseModel):
    num1: float
    num2: float


# ====================== DEPENDENCIES ======================
def validate_numbers(num1: float, num2: float):
    """Reusable dependency for number validation"""
    if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
        raise HTTPException(status_code=400, detail="Both numbers must be valid")
    return True


# ====================== ROUTES ======================

@app.get("/")
async def root():
    return {
        "message": "Calculator API is running! 🚀",
        "docs": "/docs"
    }


@app.post("/calculator")
def calculate(data: CalculatorRequest):
    """Basic calculator with operation selection"""
    
    if data.operation == "add":
        result = data.num1 + data.num2
    elif data.operation == "sub":
        result = data.num1 - data.num2
    elif data.operation == "multiply":
        result = data.num1 * data.num2
    elif data.operation == "divide":
        if data.num2 == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        result = data.num1 / data.num2
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")

    return {
        "num1": data.num1,
        "num2": data.num2,
        "operation": data.operation,
        "Here is the result": result
    }


# Individual operation endpoints (easier to use)
@app.get("/add")
async def add(num1: float, num2: float, _: bool = Depends(validate_numbers)):
    return {"result": num1 + num2}


@app.get("/sub")
async def sub(num1: float, num2: float):
    return {"result": num1 - num2}


@app.get("/multiply")
async def multiply(num1: float, num2: float):
    return {"result": num1 * num2}


@app.get("/divide")
async def divide(num1: float, num2: float):
    if num2 == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": num1 / num2}


@app.get("/power")
async def power(base: float, exponent: float):
    return {"result": base ** exponent}


@app.get("/sqrt")
async def square_root(number: float):
    if number < 0:
        raise HTTPException(status_code=400, detail="Cannot take square root of negative number")
    return {"result": number ** 0.5}


# Run with: uvicorn firstFastAPI:app --reload