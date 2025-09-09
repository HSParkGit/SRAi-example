import logging
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import api_router
from app.core.config import settings
from app.db.base import get_db
from app.db.init_db import init_db

# 더 자세한 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="게시판 API",
    description="로그인, 회원가입, 게시판 기능을 제공하는 API",
    version="0.1.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시에는 특정 오리진만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "게시판 API 서버에 오신 것을 환영합니다."}

@app.on_event("startup")
def on_startup():
    logger.info("애플리케이션 시작...")
    # 데이터베이스 초기화
    db = next(get_db())
    init_db(db)
    logger.info("데이터베이스가 초기화되었습니다.") 