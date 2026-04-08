"""
RoomSettings 스키마 (Phase 4)
"""

from datetime import datetime
from pydantic import BaseModel


class RoomSettingsUpdate(BaseModel):
    open_time: str | None = None    # "09:00"
    close_time: str | None = None   # "22:00"
    slot_duration: int | None = None  # 분 단위


class RoomSettingsResponse(BaseModel):
    id: int
    room_id: int
    open_time: str
    close_time: str
    slot_duration: int
    created_at: datetime
    updated_at: datetime
