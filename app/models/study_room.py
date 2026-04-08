"""
StudyRoom 모델 — study_rooms 테이블 (ERD Phase 1)

id         INTEGER PK
name       VARCHAR
created_at DATETIME
"""

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class StudyRoom(Base):
    __tablename__ = "study_rooms"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
