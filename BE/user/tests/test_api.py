"""
Test API calls
"""
from typing import Callable
import pytest
from requests.exceptions import HTTPError
from fastapi.testclient import TestClient
from auth.models import AccessTokenAPIModel

from main import app
from user.models import UserDBModel

client = TestClient(app)


def test_login__success(create_user_function: UserDBModel):
    """
    Test getting the refresh token
    """
    user = create_user_function()
    payload = {
        "email": "test@email.com",
        "password": "simple_pass123",
    }
    response = client.post("/api/auth/login", json=payload)
    response.raise_for_status()
    json_data = response.json()

    assert isinstance(json_data["refresh"], str)
    assert type(json_data["exp"]) is int

def test_login__fail(create_user_function: UserDBModel):
    """
    Test getting the refresh token
    """
    user = create_user_function()
    payload = {
        "email": "test@email.com",
        "password": "wrong_pass",
    }
    response = client.post("/api/auth/login", json=payload)
    json_data = response.json()

    assert response.status_code == 401
    assert json_data["detail"] == "Invalid credentials"

def test_access(create_user_function: UserDBModel):
    """
    Test getting the access token
    """
    user = create_user_function()
    payload = {
        "email": "test@email.com",
        "password": "simple_pass123",
    }
    response = client.post("/api/auth/login", json=payload)
    response.raise_for_status()
    json_data = response.json()

    payload = {
        "email": "test@email.com",
        "password": "simple_pass123",
    }
    response = client.post(f"/api/auth/refresh/{json_data['refresh']}")
    json_data = response.json()
    assert type(json_data["token"]) is str
    assert type(json_data["exp"]) is int


def test_get_user_success(create_user_function):
    """
    Test getting a user with `token_user` dependency
    """
    user = create_user_function(roles=["admin"])
    payload = {
        "email": "test@email.com",
        "password": "simple_pass123",
    }
    response = client.post("/api/auth/login", json=payload)
    response.raise_for_status()
    json_data = response.json()

    response = client.post(f"/api/auth/refresh/{json_data['refresh']}")
    json_data = response.json()
    token = json_data["token"]
    assert type(token) is str
    assert type(json_data["exp"]) is int

    headers = {"X-Auth-Token": token}
    response = client.get(f"/api/user/{user.id}", headers=headers)
    json_data = response.json()
    assert json_data["detail"] == "X-Auth-Token invalid format"

    headers = {"X-Auth-Token": f"Bearer: {token}"}
    response = client.get(f"/api/user/{user.id}", headers=headers)
    response.raise_for_status()
    json_data = response.json()
    assert json_data["email"] == payload["email"]


def test_get_user_fail_invalid_credentials(access_token_func: Callable):
    """
    Test getting a user with `token_user` dependency
    """
    access_operator, user_operator = access_token_func(roles=["operator"])
    access_admin, user_admin = access_token_func(roles=["admin"])

    # Test getting self data
    headers = {"X-Auth-Token": f"Bearer: {access_operator.token}"}
    response = client.get(f"/api/user/{user_operator.id}", headers=headers)
    response.raise_for_status()
    json_data = response.json()
    assert json_data["id"] == user_operator.id
    assert json_data["roles"] == user_operator.roles
    
    # Test getting admin data from operator's POV
    headers = {"X-Auth-Token": f"Bearer: {access_operator.token}"}
    response = client.get(f"/api/user/{user_admin.id}", headers=headers)
    json_data = response.json()
    assert response.status_code == 401
    assert json_data["detail"] == "Invalid credentials"

    # Test getting operator data from admin's POV
    headers = {"X-Auth-Token": f"Bearer: {access_admin.token}"}
    response = client.get(f"/api/user/{user_operator.id}", headers=headers)
    response.raise_for_status()
    json_data = response.json()
    assert json_data["id"] == user_operator.id
    assert json_data["roles"] == user_operator.roles

