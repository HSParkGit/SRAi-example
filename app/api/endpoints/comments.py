from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.api import deps
from app.db.base import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Comment)
def create_comment(
    *,
    db: Session = Depends(get_db),
    comment_in: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    댓글 작성
    """
    # 게시글 존재 확인
    post = services.post.get_post(db=db, post_id=comment_in.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )
    comment = services.comment.create_comment(
        db=db, obj_in=comment_in, user_id=current_user.id
    )
    return comment

@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    comment_in: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    댓글 수정
    """
    comment = services.comment.get_comment(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다.",
        )
    if comment.user_id != current_user.id and not services.user.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    comment = services.comment.update_comment(
        db=db, db_obj=comment, obj_in=comment_in
    )
    return comment

@router.delete("/{comment_id}", response_model=schemas.Comment)
def delete_comment(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    댓글 삭제
    """
    comment = services.comment.get_comment(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다.",
        )
    if comment.user_id != current_user.id and not services.user.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )
    comment = services.comment.delete_comment(db=db, db_obj=comment)
    return comment 