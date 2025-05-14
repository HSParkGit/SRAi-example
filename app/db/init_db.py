from sqlalchemy.orm import Session

from app import models, schemas, services
from app.core.config import settings
from app.db.base import Base, engine

def init_db(db: Session) -> None:
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    
    # 관리자 계정 생성
    admin = services.user.get_by_email(db, email=settings.ADMIN_EMAIL)
    if not admin:
        admin_in = schemas.UserCreate(
            email=settings.ADMIN_EMAIL,
            username="관리자",
            password=settings.ADMIN_PASSWORD,
            confirm_password=settings.ADMIN_PASSWORD,
        )
        admin = services.user.create_user(db, obj_in=admin_in)
        
        # 관리자 권한 부여
        admin.is_admin = True
        db.add(admin)
        db.commit()
        db.refresh(admin) 