"""
Room 스키마 (Phase 2 이후: capacity, description 포함)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str
    capacity: int = 1
    description: Optional[str] = None


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None


class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    description: Optional[str] = None
    created_at: datetime
