from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.api import deps
from app.db.base import get_db

router = APIRouter()

@router.get("/", response_model=schemas.PostPagination)
def read_posts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    order_by: str = Query("created_at", description="정렬 기준"),
    order_desc: bool = Query(True, description="내림차순 정렬"),
) -> Any:
    """
    게시글 목록 조회 (페이지네이션)
    """
    return services.post.get_pagination(
        db=db, page=page, size=size, order_by=order_by, order_desc=order_desc
    )

@router.post("/", response_model=schemas.Post)
def create_post(
    *,
    db: Session = Depends(get_db),
    post_in: schemas.PostCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    새 게시글 작성
    """
    post = services.post.create_post(db=db, obj_in=post_in, user_id=current_user.id)
    return post

@router.get("/{post_id}", response_model=schemas.PostDetail)
def read_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    skip_increment: bool = Query(False, description="조회수 증가 건너뛰기"),
) -> Any:
    """
    게시글 상세 조회
    """
    post = services.post.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )
    
    # skip_increment 파라미터가 True가 아닌 경우에만 조회수 증가
    if not skip_increment:
        post = services.post.increment_view_count(db=db, db_obj=post)
    
    return post

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    post_in: schemas.PostUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    게시글 업데이트
    """
    post = services.post.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )
    if post.user_id != current_user.id and not services.user.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    post = services.post.update_post(db=db, db_obj=post, obj_in=post_in)
    return post

@router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    게시글 삭제
    """
    post = services.post.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )
    if post.user_id != current_user.id and not services.user.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    post = services.post.delete_post(db=db, db_obj=post)
    return post

@router.get("/{post_id}/comments", response_model=List[schemas.CommentDetail])
def read_post_comments(
    *,
    db: Session = Depends(get_db),
    post_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    게시글의 댓글 목록 조회
    """
    post = services.post.get_post(db=db, post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )
    return services.comment.get_comments_by_post(
        db=db, post_id=post_id, skip=skip, limit=limit
    ) 