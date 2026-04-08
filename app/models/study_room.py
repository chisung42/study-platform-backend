"""
StudyRoom 모델 — study_rooms 테이블

Phase 1: id, name, created_at
Phase 2: capacity(수용 인원), description 추가
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class StudyRoom(Base):
    __tablename__ = "study_rooms"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    # Phase 2: 수용 인원 (기본값 1)
    capacity = Column(Integer, nullable=False, default=1)

    # Phase 2: 룸 설명 (선택)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
