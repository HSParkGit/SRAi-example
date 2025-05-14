from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.schemas.user import User

# 공통 속성
class PostBase(BaseModel):
    title: str
    content: str

# 생성 요청 시 사용
class PostCreate(PostBase):
    pass

# 업데이트 요청 시 사용
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# DB에서 조회한 데이터를 반환할 때 사용 (기본)
class Post(PostBase):
    id: int
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 상세 정보를 포함한 게시글 (작성자 정보 포함)
class PostDetail(Post):
    author: User

    class Config:
        orm_mode = True

# 페이지네이션을 위한 응답
class PostPagination(BaseModel):
    total: int
    items: List[Post]
    page: int
    size: int
    pages: int 