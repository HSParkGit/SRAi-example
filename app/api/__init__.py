from fastapi import APIRouter

from app.api.endpoints import auth, users, posts, comments, ai

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["인증"])
api_router.include_router(users.router, prefix="/users", tags=["사용자"])
api_router.include_router(posts.router, prefix="/posts", tags=["게시글"])
api_router.include_router(comments.router, prefix="/comments", tags=["댓글"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
