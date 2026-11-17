"""Tests for the calculator backend in app.py."""

import pytest

from app import app


@pytest.fixture
def client():
    return app.test_client()


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        ("add", 2, 3, 5.0),
        ("subtract", 7, 4, 3.0),
        ("multiply", 6, 7, 42.0),
        ("divide", 9, 2, 4.5),
    ],
)
def test_operations(client, operation, a, b, expected):
    response = client.get(f"/{operation}?a={a}&b={b}")

    assert response.status_code == 200
    body = response.get_json()
    assert body["operation"] == operation
    assert body["a"] == float(a)
    assert body["b"] == float(b)
    assert body["result"] == expected


def test_negative_numbers(client):
    response = client.get("/multiply?a=-3&b=4")

    assert response.status_code == 200
    assert response.get_json()["result"] == -12.0


def test_decimals(client):
    response = client.get("/add?a=0.5&b=0.25")

    assert response.status_code == 200
    assert response.get_json()["result"] == 0.75


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_divide_by_zero(client):
    response = client.get("/divide?a=5&b=0")

    assert response.status_code == 400
    assert response.get_json() == {"error": "cannot divide by zero"}


def test_unknown_operation(client):
    response = client.get("/power?a=2&b=3")

    assert response.status_code == 404


def test_missing_parameter(client):
    response = client.get("/add?a=2")

    assert response.status_code == 400
    assert response.get_json() == {"error": "missing parameter 'b'"}


def test_not_a_number(client):
    response = client.get("/add?a=two&b=3")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "parameter 'a' must be a number, got 'two'"
    }
