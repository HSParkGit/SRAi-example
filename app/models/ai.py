from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base
from datetime import datetime


class ColumnDescription(Base):
    """컬럼 설명 테이블"""
    __tablename__ = "column_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(100), nullable=False, index=True)
    column_name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    embeddings = relationship("ColumnEmbedding", back_populates="column_description", cascade="all, delete-orphan")


class ColumnEmbedding(Base):
    """컬럼 임베딩 테이블"""
    __tablename__ = "column_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    column_id = Column(Integer, ForeignKey("column_descriptions.id"), nullable=False)
    embedding = Column(Vector(384), nullable=False)  # all-MiniLM-L6-v2는 384차원
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    column_description = relationship("ColumnDescription", back_populates="embeddings")
