"""A simple calculator backend.

Start it with `python app.py`, then call an operation with two numbers:

    GET /divide?a=9&b=2   ->  {"operation": "divide", "a": 9.0, "b": 2.0, "result": 4.5}
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="Calculator backend")


def _number(raw, name):
    """Turn one query value into a number.

    Returns (value, error). Exactly one of the two is None.
    """
    if raw is None:
        return None, f"missing parameter '{name}'"
    try:
        return float(raw), None
    except ValueError:
        return None, f"parameter '{name}' must be a number, got '{raw}'"


def _calculate(operation, a, b):
    """Apply one operation to two numbers."""
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ZeroDivisionError("cannot divide by zero")
        return a / b
    raise KeyError(operation)


def _handle(operation, raw_a, raw_b):
    """Shared body for every operation route: check a and b, calculate, reply."""
    a, error = _number(raw_a, "a")
    if error is not None:
        return JSONResponse({"error": error}, status_code=400)

    b, error = _number(raw_b, "b")
    if error is not None:
        return JSONResponse({"error": error}, status_code=400)

    try:
        result = _calculate(operation, a, b)
    except ZeroDivisionError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)

    return {"operation": operation, "a": a, "b": b, "result": result}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/add")
def add(
    a: Optional[str] = Query(None, description="First number, for example 2"),
    b: Optional[str] = Query(None, description="Second number, for example 3"),
):
    return _handle("add", a, b)


@app.get("/subtract")
def subtract(
    a: Optional[str] = Query(None, description="First number, for example 7"),
    b: Optional[str] = Query(None, description="Second number, for example 4"),
):
    return _handle("subtract", a, b)


@app.get("/multiply")
def multiply(
    a: Optional[str] = Query(None, description="First number, for example 6"),
    b: Optional[str] = Query(None, description="Second number, for example 7"),
):
    return _handle("multiply", a, b)


@app.get("/divide")
def divide(
    a: Optional[str] = Query(None, description="First number, for example 9"),
    b: Optional[str] = Query(None, description="Second number, for example 2"),
):
    return _handle("divide", a, b)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
