"""
StudyGroup 모델 — study_groups 테이블 (Phase 5)

스터디 모집글.
status: '모집중' → '모집완료' → '종료'
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class StudyGroup(Base):
    __tablename__ = "study_groups"

    id = Column(Integer, primary_key=True)

    # 모집자(조장)
    leader_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    max_members = Column(Integer, nullable=False)

    # 현재 인원 (조장 포함, 기본값 1)
    current_members = Column(Integer, nullable=False, default=1)

    # '모집중' / '모집완료' / '종료'
    status = Column(String(20), nullable=False, default="모집중")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
