"""
AI 관련 API 엔드포인트
컬럼 후보 추출, 임베딩 갱신
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
import json
import logging
import traceback

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.services.ai import ai_service

router = APIRouter()
logger = logging.getLogger(__name__)


class ColumnCandidatesRequest(BaseModel):
    """컬럼 후보 추출 요청"""
    input: str
    top_k: int = 5
    
    class Config:
        from_attributes = True


class ColumnCandidatesResponse(BaseModel):
    """컬럼 후보 추출 응답"""
    candidates: list[str]
    details: list[dict] = []
    input: str
    message: str = ""


class UpdateEmbeddingsResponse(BaseModel):
    """임베딩 갱신 응답"""
    message: str
    count: int
    total_columns: int = 0


@router.post("/column-candidates", response_model=ColumnCandidatesResponse)
async def get_column_candidates(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    사용자 입력에 대한 컬럼 후보 추출
    
    Args:
        request: FastAPI Request 객체
        db: 데이터베이스 세션
    
    Returns:
        컬럼 후보 리스트와 상세 정보
    """
    try:
        logger.info("컬럼 후보 추출 요청 시작")
        
        # JSON 바디 파싱
        body = await request.json()
        logger.info(f"받은 JSON: {body}")
        
        input_text = body.get("input", "")
        top_k = body.get("top_k", 5)
        
        logger.info(f"input: {input_text}")
        logger.info(f"top_k: {top_k}")
        
        if not input_text.strip():
            raise HTTPException(status_code=400, detail="입력값이 비어있습니다.")
        
        if top_k < 1 or top_k > 20:
            raise HTTPException(status_code=400, detail="top_k는 1-20 사이의 값이어야 합니다.")
        
        logger.info("AI 서비스 호출 시작")
        result = ai_service.get_column_candidates(input_text, top_k)
        logger.info(f"AI 서비스 결과: {result}")
        
        if "error" in result:
            logger.error(f"AI 서비스 오류: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        
        logger.info("응답 생성 완료")
        return ColumnCandidatesResponse(
            candidates=result["candidates"],
            details=result.get("details", []),
            input=result["input"],
            message=result.get("message", "")
        )
        
    except HTTPException as e:
        logger.error(f"HTTP 예외: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"예상치 못한 오류: {str(e)}")
        logger.error(f"스택 트레이스: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"컬럼 후보 추출 중 오류가 발생했습니다: {str(e)}")


@router.post("/update-embeddings", response_model=UpdateEmbeddingsResponse)
async def update_embeddings(
    db: Session = Depends(get_db)
):
    """
    모든 컬럼 설명에 대한 임베딩 갱신
    
    Args:
        db: 데이터베이스 세션
    
    Returns:
        갱신 결과 정보
    """
    try:
        result = ai_service.update_embeddings()
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return UpdateEmbeddingsResponse(
            message=result["message"],
            count=result["count"],
            total_columns=result.get("total_columns", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"임베딩 갱신 중 오류가 발생했습니다: {str(e)}")


@router.get("/health")
async def ai_health_check():
    """AI 서비스 상태 확인"""
    try:
        # 임베딩 모델이 로드되었는지 확인
        test_embedding = ai_service.generate_embedding("test")
        
        return {
            "status": "healthy",
            "model_loaded": True,
            "embedding_dimension": len(test_embedding),
            "message": "AI 서비스가 정상적으로 작동 중입니다."
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e),
            "message": "AI 서비스에 문제가 있습니다."
        }
