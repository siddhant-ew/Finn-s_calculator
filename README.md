# Finn's Project

This is Finn's project.

## Calculator backend

A small calculator API written in Python with [Flask](https://flask.palletsprojects.com/).
Every operation takes two numbers as query parameters, `a` and `b`, and answers with JSON.

| Operation | Call | Answer |
| --- | --- | --- |
| add | `/add?a=2&b=3` | `{"operation": "add", "a": 2.0, "b": 3.0, "result": 5.0}` |
| subtract | `/subtract?a=7&b=4` | `{"operation": "subtract", "a": 7.0, "b": 4.0, "result": 3.0}` |
| multiply | `/multiply?a=6&b=7` | `{"operation": "multiply", "a": 6.0, "b": 7.0, "result": 42.0}` |
| divide | `/divide?a=9&b=2` | `{"operation": "divide", "a": 9.0, "b": 2.0, "result": 4.5}` |
| health | `/health` | `{"status": "ok"}` |

## Install

```
pip install -r requirements.txt
```

## Run

```
python app.py
```

The server listens on <http://127.0.0.1:5000>. Try:

```
curl "http://127.0.0.1:5000/divide?a=9&b=2"
```

To use a different port, change the `port=` value at the bottom of `app.py`.

## Test

```
pytest -q
```

`test_app.py` covers each operation, negative numbers, decimals, the health check,
dividing by zero, an unknown operation, a missing parameter and a non-numeric one.

## Errors

Every error comes back as JSON with an `error` message.

| Situation | Status | Body |
| --- | --- | --- |
| `a` or `b` missing | 400 | `{"error": "missing parameter 'b'"}` |
| `a` or `b` not a number | 400 | `{"error": "parameter 'a' must be a number, got 'two'"}` |
| dividing by zero | 400 | `{"error": "cannot divide by zero"}` |
| no such operation | 404 | Flask's default 404 page |

## Adding another operation

1. Add the maths to `_calculate` in `app.py`.
2. Add a route that calls `_handle("your-operation")`, following the ones already there.
3. Add a case to the table in `test_app.py`.
4. Add a row to the table at the top of this README.
