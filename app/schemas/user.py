from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

# 공통 속성
class UserBase(BaseModel):
    email: EmailStr
    username: str

# 생성 요청 시 사용
class UserCreate(UserBase):
    password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

# 업데이트 요청 시 사용
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

# DB에서 조회한 데이터를 반환할 때 사용
class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 로그인 요청 시 사용
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 토큰 응답
class Token(BaseModel):
    access_token: str
    token_type: str

# 토큰 페이로드
class TokenPayload(BaseModel):
    sub: Optional[int] = None 