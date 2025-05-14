from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app import models, schemas

def get_comments_by_post(
    db: Session, post_id: int, skip: int = 0, limit: int = 100
) -> List[models.Comment]:
    return (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .order_by(desc(models.Comment.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def create_comment(
    db: Session, obj_in: schemas.CommentCreate, user_id: int
) -> models.Comment:
    db_obj = models.Comment(
        content=obj_in.content,
        post_id=obj_in.post_id,
        user_id=user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_comment(
    db: Session, db_obj: models.Comment, obj_in: schemas.CommentUpdate
) -> models.Comment:
    update_data = obj_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_comment(db: Session, db_obj: models.Comment) -> models.Comment:
    db.delete(db_obj)
    db.commit()
    return db_obj 