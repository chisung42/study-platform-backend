"""
RoomSettings 모델 — room_settings 테이블 (Phase 4)

룸별 운영시간과 타임슬롯 단위를 관리한다.
study_rooms와 1:1 관계 (UNIQUE on room_id).
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class RoomSettings(Base):
    __tablename__ = "room_settings"

    __table_args__ = (
        UniqueConstraint("room_id"),
    )

    id = Column(Integer, primary_key=True)

    room_id = Column(Integer, ForeignKey("study_rooms.id", ondelete="CASCADE"), nullable=False)

    # 운영 시작/종료 시간 (문자열 "HH:MM" 형태)
    open_time = Column(String(5), nullable=False, default="09:00")
    close_time = Column(String(5), nullable=False, default="22:00")

    # 타임슬롯 단위 (분): 60 = 1시간 단위로만 예약 가능
    slot_duration = Column(Integer, nullable=False, default=60)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
