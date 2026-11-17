"""A simple calculator backend.

Start it with `python app.py`, then call an operation with two numbers:

    GET /divide?a=9&b=2   ->  {"operation": "divide", "a": 9.0, "b": 2.0, "result": 4.5}
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


def _number(name):
    """Read a number from the query string.

    Returns (value, error). Exactly one of the two is None.
    """
    raw = request.args.get(name)
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


def _handle(operation):
    """Shared body for every operation route: read a and b, calculate, reply."""
    a, error = _number("a")
    if error is not None:
        return jsonify({"error": error}), 400

    b, error = _number("b")
    if error is not None:
        return jsonify({"error": error}), 400

    try:
        result = _calculate(operation, a, b)
    except ZeroDivisionError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"operation": operation, "a": a, "b": b, "result": result})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/add")
def add():
    return _handle("add")


@app.get("/subtract")
def subtract():
    return _handle("subtract")


@app.get("/multiply")
def multiply():
    return _handle("multiply")


@app.get("/divide")
def divide():
    return _handle("divide")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
