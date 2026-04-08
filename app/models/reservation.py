"""
Reservation 모델 — reservations 테이블

Phase 1: id, user_id, room_id, start_time, end_time, created_at
Phase 6: group_id 추가 (NULL이면 개인 예약, 값이 있으면 그룹 예약)
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("study_rooms.id"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    # Phase 6: 그룹 예약 (nullable — 없으면 개인 예약)
    group_id = Column(Integer, ForeignKey("study_groups.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
