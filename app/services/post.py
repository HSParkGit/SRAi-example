from typing import Dict, List, Optional, Any

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app import models, schemas

def get_posts(
    db: Session, 
    skip: int = 0, 
    limit: int = 10,
    order_by: str = "created_at",
    order_desc: bool = True
) -> List[models.Post]:
    query = db.query(models.Post)
    
    # 정렬
    if order_by == "created_at":
        order_col = models.Post.created_at
    elif order_by == "view_count":
        order_col = models.Post.view_count
    else:
        order_col = models.Post.created_at
    
    if order_desc:
        query = query.order_by(desc(order_col))
    else:
        query = query.order_by(order_col)
    
    return query.offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int) -> Optional[models.Post]:
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_post_with_author(db: Session, post_id: int) -> Optional[models.Post]:
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def create_post(db: Session, obj_in: schemas.PostCreate, user_id: int) -> models.Post:
    db_obj = models.Post(
        title=obj_in.title,
        content=obj_in.content,
        user_id=user_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_post(
    db: Session, db_obj: models.Post, obj_in: schemas.PostUpdate
) -> models.Post:
    update_data = obj_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_post(db: Session, db_obj: models.Post) -> models.Post:
    db.delete(db_obj)
    db.commit()
    return db_obj

def increment_view_count(db: Session, db_obj: models.Post) -> models.Post:
    db_obj.view_count += 1
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_total_count(db: Session) -> int:
    return db.query(func.count(models.Post.id)).scalar()

def get_pagination(
    db: Session,
    page: int = 1,
    size: int = 10,
    order_by: str = "created_at",
    order_desc: bool = True
) -> Dict[str, Any]:
    total = get_total_count(db)
    pages = (total // size) + (1 if total % size > 0 else 0)
    skip = (page - 1) * size
    
    posts = get_posts(
        db=db, 
        skip=skip, 
        limit=size,
        order_by=order_by,
        order_desc=order_desc
    )
    
    return {
        "total": total,
        "items": posts,
        "page": page,
        "size": size,
        "pages": pages
    } 