import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models


def test_login(client: TestClient, create_test_user: models.User):
    """
    로그인 API 테스트
    """
    data = {
        "username": "test@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, create_test_user: models.User):
    """
    잘못된 비밀번호로 로그인 시도 테스트
    """
    data = {
        "username": "test@example.com",
        "password": "wrong_password"
    }
    response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 401
    assert "detail" in response.json()


def test_register(client: TestClient):
    """
    회원가입 API 테스트
    """
    data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == data["email"]
    assert response.json()["username"] == data["username"]
    assert "id" in response.json()


def test_register_existing_email(client: TestClient, create_test_user: models.User):
    """
    이미 존재하는 이메일로 회원가입 시도 테스트
    """
    data = {
        "email": "test@example.com",  # 이미 존재하는 이메일
        "username": "newuser",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 400
    assert "detail" in response.json() 