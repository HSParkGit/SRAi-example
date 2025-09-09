"""
AI 관련 초기 데이터 설정
기부 관련 컬럼 설명들을 데이터베이스에 삽입
"""

from sqlalchemy.orm import Session
from app.models.ai import ColumnDescription
from app.db.session import SessionLocal


def get_donation_columns():
    """기부 관련 컬럼 설명 데이터"""
    return [
        {
            "table_name": "donations",
            "column_name": "amount",
            "description": "기부 금액, 후원 금액, 기부액, 후원액, 기부비, 후원비, 기부자금, 후원자금, 기부규모, 후원규모, 기부 총액, 후원 총액"
        },
        {
            "table_name": "donations", 
            "column_name": "donor_name",
            "description": "기부자 이름, 후원자 이름, 기부자명, 후원자명, 기부자, 후원자, 기부자 성명, 후원자 성명, 기부자 정보, 후원자 정보"
        },
        {
            "table_name": "donations",
            "column_name": "donation_date", 
            "description": "기부 날짜, 후원 날짜, 기부일, 후원일, 기부 시점, 후원 시점, 기부 일자, 후원 일자, 기부 시간, 후원 시간"
        },
        {
            "table_name": "donations",
            "column_name": "purpose",
            "description": "기부 목적, 후원 목적, 기부 용도, 후원 용도, 기부 취지, 후원 취지, 기부 방향, 후원 방향, 기부 의도, 후원 의도"
        },
        {
            "table_name": "donations",
            "column_name": "status",
            "description": "기부 상태, 후원 상태, 기부 진행상황, 후원 진행상황, 기부 단계, 후원 단계, 기부 현황, 후원 현황, 기부 상태값, 후원 상태값"
        },
        {
            "table_name": "donations",
            "column_name": "category",
            "description": "기부 분야, 후원 분야, 기부 카테고리, 후원 카테고리, 기부 영역, 후원 영역, 기부 부문, 후원 부문, 기부 유형, 후원 유형"
        },
        {
            "table_name": "donations",
            "column_name": "target_amount",
            "description": "목표 금액, 목표 기부액, 목표 후원액, 목표 기부비, 목표 후원비, 목표 기부자금, 목표 후원자금, 목표 기부규모, 목표 후원규모"
        },
        {
            "table_name": "donations",
            "column_name": "campaign_name",
            "description": "기부 캠페인, 후원 캠페인, 기부 운동, 후원 운동, 기부 프로젝트, 후원 프로젝트, 기부 모금, 후원 모금, 기부 이벤트, 후원 이벤트"
        },
        {
            "table_name": "donations",
            "column_name": "beneficiary",
            "description": "수혜자, 기부 수혜자, 후원 수혜자, 기부 대상, 후원 대상, 기부 혜택자, 후원 혜택자, 기부 수혜 대상, 후원 수혜 대상, 기부 수혜 기관"
        },
        {
            "table_name": "donations",
            "column_name": "payment_method",
            "description": "결제 방법, 기부 결제방법, 후원 결제방법, 기부 결제수단, 후원 결제수단, 기부 결제방식, 후원 결제방식, 기부 결제 유형, 후원 결제 유형"
        }
    ]


def init_ai_data():
    """AI 관련 초기 데이터 삽입"""
    db = SessionLocal()
    try:
        # 기존 데이터 삭제
        db.query(ColumnDescription).delete()
        db.commit()
        
        # 새 데이터 삽입
        columns = get_donation_columns()
        for column_data in columns:
            column = ColumnDescription(**column_data)
            db.add(column)
        
        db.commit()
        print(f"✅ {len(columns)}개의 기부 관련 컬럼 설명이 삽입되었습니다.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 데이터 삽입 실패: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    init_ai_data()
