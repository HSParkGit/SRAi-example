import pytest
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.core.security import get_password_hash


def test_create_post(db_session: Session):
    """
    게시글 생성 서비스 함수 테스트
    """
    # 테스트 사용자 생성
    user = models.User(
        email="posttest@example.com",
        username="posttest",
        hashed_password=get_password_hash("password"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # 게시글 생성 데이터
    post_in = schemas.PostCreate(
        title="테스트 게시글",
        content="이것은 테스트 게시글입니다."
    )
    
    # 게시글 생성
    post = services.post.create_post(db=db_session, obj_in=post_in, user_id=user.id)
    
    # 검증
    assert post.title == post_in.title
    assert post.content == post_in.content
    assert post.user_id == user.id
    assert post.view_count == 0


def test_get_post(db_session: Session):
    """
    게시글 조회 서비스 함수 테스트
    """
    # 테스트 사용자 생성
    user = models.User(
        email="getposttest@example.com",
        username="getposttest",
        hashed_password=get_password_hash("password"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # 게시글 생성
    post = models.Post(
        title="조회 테스트 게시글",
        content="이것은 조회 테스트 게시글입니다.",
        user_id=user.id
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    # 게시글 조회
    retrieved_post = services.post.get_post(db=db_session, post_id=post.id)
    
    # 검증
    assert retrieved_post is not None
    assert retrieved_post.id == post.id
    assert retrieved_post.title == post.title
    assert retrieved_post.content == post.content
    assert retrieved_post.user_id == user.id


def test_update_post(db_session: Session):
    """
    게시글 수정 서비스 함수 테스트
    """
    # 테스트 사용자 생성
    user = models.User(
        email="updatetest@example.com",
        username="updatetest",
        hashed_password=get_password_hash("password"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # 게시글 생성
    post = models.Post(
        title="수정 전 게시글",
        content="이것은 수정 전 게시글입니다.",
        user_id=user.id
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    # 게시글 수정 데이터
    post_update = schemas.PostUpdate(
        title="수정 후 게시글",
        content="이것은 수정 후 게시글입니다."
    )
    
    # 게시글 수정
    updated_post = services.post.update_post(db=db_session, db_obj=post, obj_in=post_update)
    
    # 검증
    assert updated_post.id == post.id
    assert updated_post.title == post_update.title
    assert updated_post.content == post_update.content
    assert updated_post.user_id == user.id


def test_increment_view_count(db_session: Session):
    """
    게시글 조회수 증가 서비스 함수 테스트
    """
    # 테스트 사용자 생성
    user = models.User(
        email="viewcounttest@example.com",
        username="viewcounttest",
        hashed_password=get_password_hash("password"),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # 게시글 생성
    post = models.Post(
        title="조회수 테스트 게시글",
        content="이것은 조회수 테스트 게시글입니다.",
        user_id=user.id,
        view_count=0
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    
    # 초기 조회수 확인
    assert post.view_count == 0
    
    # 조회수 증가
    updated_post = services.post.increment_view_count(db=db_session, db_obj=post)
    
    # 검증
    assert updated_post.view_count == 1
    
    # 한 번 더 조회수 증가
    updated_post = services.post.increment_view_count(db=db_session, db_obj=updated_post)
    
    # 검증
    assert updated_post.view_count == 2 