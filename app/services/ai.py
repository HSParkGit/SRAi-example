"""
AI 서비스 레이어
임베딩 생성, 코사인 유사도 계산, 컬럼 후보 추출
"""

import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.ai import ColumnDescription, ColumnEmbedding
from app.db.session import SessionLocal
import logging
import traceback

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        # 임베딩 모델 로드 (로컬에서 실행)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # all-MiniLM-L6-v2 차원
    
    def generate_embedding(self, text: str) -> List[float]:
        """텍스트를 임베딩으로 변환"""
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            print(f"임베딩 생성 실패: {e}")
            return [0.0] * self.embedding_dim
    
    def calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """코사인 유사도 계산"""
        try:
            # numpy 배열로 변환
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # 코사인 유사도 계산
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            print(f"코사인 유사도 계산 실패: {e}")
            return 0.0
    
    def get_column_candidates(self, user_input: str, top_k: int = 5) -> Dict[str, Any]:
        """사용자 입력에 대한 컬럼 후보 추출"""
        db = SessionLocal()
        try:
            logger.info(f"컬럼 후보 추출 시작 - 입력: {user_input}, top_k: {top_k}")
            
            # 사용자 입력을 임베딩으로 변환
            logger.info("사용자 입력 임베딩 생성 시작")
            user_embedding = self.generate_embedding(user_input)
            logger.info(f"사용자 임베딩 생성 완료 - 차원: {len(user_embedding)}")
            
            # 모든 컬럼 임베딩 조회
            logger.info("컬럼 임베딩 조회 시작")
            embeddings = db.query(ColumnEmbedding).all()
            logger.info(f"조회된 임베딩 개수: {len(embeddings)}")
            
            if not embeddings:
                logger.warning("임베딩이 없습니다")
                return {
                    "candidates": [], 
                    "message": "임베딩이 생성되지 않았습니다. 먼저 임베딩을 생성해주세요.",
                    "input": user_input
                }
            
            # 유사도 계산
            logger.info("유사도 계산 시작")
            similarities = []
            for embedding in embeddings:
                similarity = self.calculate_cosine_similarity(user_embedding, embedding.embedding)
                similarities.append({
                    "column_id": embedding.column_id,
                    "table_name": embedding.column_description.table_name,
                    "column_name": embedding.column_description.column_name,
                    "description": embedding.column_description.description,
                    "similarity": similarity
                })
            
            # 유사도 순으로 정렬
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            logger.info(f"유사도 계산 완료 - 총 {len(similarities)}개")
            
            # 상위 k개 선택
            top_candidates = similarities[:top_k]
            logger.info(f"상위 {top_k}개 후보 선택 완료")
            
            result = {
                "candidates": [candidate["column_name"] for candidate in top_candidates],
                "details": top_candidates,
                "input": user_input
            }
            logger.info(f"최종 결과: {result}")
            return result
            
        except Exception as e:
            logger.error(f"컬럼 후보 추출 실패: {e}")
            logger.error(f"스택 트레이스: {traceback.format_exc()}")
            return {"candidates": [], "error": str(e), "input": user_input}
        finally:
            db.close()
    
    def update_embeddings(self) -> Dict[str, Any]:
        """모든 컬럼 설명에 대한 임베딩 생성 및 저장"""
        db = SessionLocal()
        try:
            # 기존 임베딩 삭제
            db.query(ColumnEmbedding).delete()
            db.commit()
            
            # 모든 컬럼 설명 조회
            columns = db.query(ColumnDescription).all()
            
            if not columns:
                return {"message": "컬럼 설명이 없습니다.", "count": 0}
            
            # 각 컬럼에 대해 임베딩 생성 및 저장
            created_count = 0
            for column in columns:
                try:
                    # 임베딩 생성
                    embedding = self.generate_embedding(column.description)
                    
                    # 데이터베이스에 저장
                    column_embedding = ColumnEmbedding(
                        column_id=column.id,
                        embedding=embedding
                    )
                    db.add(column_embedding)
                    created_count += 1
                    
                except Exception as e:
                    print(f"컬럼 {column.column_name} 임베딩 생성 실패: {e}")
                    continue
            
            db.commit()
            
            return {
                "message": f"{created_count}개의 임베딩이 성공적으로 생성되었습니다.",
                "count": created_count,
                "total_columns": len(columns)
            }
            
        except Exception as e:
            db.rollback()
            print(f"임베딩 업데이트 실패: {e}")
            return {"error": str(e), "count": 0}
        finally:
            db.close()


# 전역 인스턴스
ai_service = AIService()
