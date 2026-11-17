"""A simple calculator backend.

Start it with `python app.py`, then call an operation with two numbers:

    GET /divide?a=9&b=2   ->  {"operation": "divide", "a": 9.0, "b": 2.0, "result": 4.5}
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Calculator backend")


def _number(request, name):
    """Read a number from the query string.

    Returns (value, error). Exactly one of the two is None.
    """
    raw = request.query_params.get(name)
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


def _handle(request, operation):
    """Shared body for every operation route: read a and b, calculate, reply."""
    a, error = _number(request, "a")
    if error is not None:
        return JSONResponse({"error": error}, status_code=400)

    b, error = _number(request, "b")
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
def add(request: Request):
    return _handle(request, "add")


@app.get("/subtract")
def subtract(request: Request):
    return _handle(request, "subtract")


@app.get("/multiply")
def multiply(request: Request):
    return _handle(request, "multiply")


@app.get("/divide")
def divide(request: Request):
    return _handle(request, "divide")


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
