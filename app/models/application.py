"""
Application 모델 — applications 테이블 (Phase 5)

스터디 신청.
status: 'pending' → 'accepted' / 'rejected'
UNIQUE(group_id, applicant_id): 한 모집에 중복 신청 불가
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    __table_args__ = (
        UniqueConstraint("group_id", "applicant_id"),
    )

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey("study_groups.id", ondelete="CASCADE"), nullable=False)
    applicant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 'pending' / 'accepted' / 'rejected'
    status = Column(String(20), nullable=False, default="pending")

    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
