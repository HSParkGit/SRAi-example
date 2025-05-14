import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models
from app.services import post as post_service


def test_read_posts(client: TestClient, db_session: Session):
    """
    게시글 목록 조회 API 테스트
    """
    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()
    assert "page" in response.json()


def test_create_post(client: TestClient, db_session: Session, normal_user_token_headers: dict):
    """
    게시글 작성 API 테스트
    """
    data = {
        "title": "테스트 게시글",
        "content": "이것은 테스트 게시글입니다."
    }
    response = client.post(
        "/api/v1/posts/", 
        json=data,
        headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["content"] == data["content"]
    assert "id" in response.json()


def test_create_post_unauthorized(client: TestClient, db_session: Session):
    """
    인증되지 않은 사용자의 게시글 작성 시도 테스트
    """
    data = {
        "title": "테스트 게시글",
        "content": "이것은 테스트 게시글입니다."
    }
    response = client.post("/api/v1/posts/", json=data)
    assert response.status_code == 401


def test_read_post(client: TestClient, db_session: Session, normal_user_token_headers: dict):
    """
    게시글 상세 조회 API 테스트
    """
    # 테스트용 게시글 생성
    data = {
        "title": "테스트 게시글",
        "content": "이것은 테스트 게시글입니다."
    }
    create_response = client.post(
        "/api/v1/posts/", 
        json=data,
        headers=normal_user_token_headers
    )
    post_id = create_response.json()["id"]
    
    # 게시글 조회
    response = client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]
    assert response.json()["content"] == data["content"]
    assert response.json()["id"] == post_id


def test_update_post(client: TestClient, db_session: Session, normal_user_token_headers: dict):
    """
    게시글 수정 API 테스트
    """
    # 테스트용 게시글 생성
    data = {
        "title": "테스트 게시글",
        "content": "이것은 테스트 게시글입니다."
    }
    create_response = client.post(
        "/api/v1/posts/", 
        json=data,
        headers=normal_user_token_headers
    )
    post_id = create_response.json()["id"]
    
    # 게시글 수정
    update_data = {
        "title": "수정된 게시글",
        "content": "이것은 수정된 게시글입니다."
    }
    response = client.put(
        f"/api/v1/posts/{post_id}", 
        json=update_data,
        headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]
    assert response.json()["content"] == update_data["content"]
    assert response.json()["id"] == post_id


def test_delete_post(client: TestClient, db_session: Session, normal_user_token_headers: dict):
    """
    게시글 삭제 API 테스트
    """
    # 테스트용 게시글 생성
    data = {
        "title": "테스트 게시글",
        "content": "이것은 테스트 게시글입니다."
    }
    create_response = client.post(
        "/api/v1/posts/", 
        json=data,
        headers=normal_user_token_headers
    )
    post_id = create_response.json()["id"]
    
    # 게시글 삭제
    response = client.delete(
        f"/api/v1/posts/{post_id}",
        headers=normal_user_token_headers
    )
    assert response.status_code == 200
    
    # 삭제 후 조회 불가 확인
    get_response = client.get(f"/api/v1/posts/{post_id}")
    assert get_response.status_code == 404 