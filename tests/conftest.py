import os
import pytest
from typing import Generator, Dict

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.base import Base, get_db
from app.core.config import settings
from app.api.deps import get_current_active_user
from app import models
from app.core.security import create_access_token

# 테스트용 PostgreSQL 데이터베이스
TEST_DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi_ai_test"

# 테스트용 데이터베이스 엔진 설정
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    테스트용 데이터베이스 세션 픽스처
    """
    # 테스트 데이터베이스 생성
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    # 테스트 후 데이터베이스 내용 삭제
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    테스트 클라이언트 픽스처
    """
    # 의존성 오버라이드
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 의존성 오버라이드 제거
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def create_test_user(db_session: Session) -> models.User:
    """
    테스트용 사용자 생성 픽스처
    """
    # 기존 사용자 확인
    user = db_session.query(models.User).filter(models.User.email == "test@example.com").first()
    if not user:
        # 테스트 사용자 생성
        from app.core.security import get_password_hash
        user = models.User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def normal_user_token_headers(create_test_user: models.User) -> Dict[str, str]:
    """
    테스트용 사용자 토큰 헤더 픽스처
    """
    access_token = create_access_token(
        data={"sub": create_test_user.email}
    )
    return {"Authorization": f"Bearer {access_token}"} 