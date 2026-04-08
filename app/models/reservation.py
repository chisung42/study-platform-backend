"""
Reservation 모델 — reservations 테이블 (ERD Phase 1)

id         INTEGER PK
user_id    INTEGER FK→users
room_id    INTEGER FK→study_rooms
start_time DATETIME
end_time   DATETIME
created_at DATETIME
"""

from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    room_id = Column(BigInteger, ForeignKey("study_rooms.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
