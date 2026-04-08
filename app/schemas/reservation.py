"""
Reservation 스키마 (Phase 4: 운영시간 검증, Phase 6: group_id)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReservationCreate(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    group_id: Optional[int] = None   # Phase 6: 그룹 예약


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    group_id: Optional[int] = None
    created_at: datetime
