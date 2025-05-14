from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.schemas.user import User

# 공통 속성
class CommentBase(BaseModel):
    content: str

# 생성 요청 시 사용
class CommentCreate(CommentBase):
    post_id: int

# 업데이트 요청 시 사용
class CommentUpdate(BaseModel):
    content: Optional[str] = None

# DB에서 조회한 데이터를 반환할 때 사용
class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 상세 정보를 포함한 댓글 (작성자 정보 포함)
class CommentDetail(Comment):
    author: User

    class Config:
        orm_mode = True 