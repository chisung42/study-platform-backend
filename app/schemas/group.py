"""
StudyGroup / Application 스키마 (Phase 5)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# ── 스터디 그룹 ──

class GroupCreate(BaseModel):
    title: str
    description: Optional[str] = None
    max_members: int


class GroupUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    max_members: Optional[int] = None
    status: Optional[str] = None


class GroupResponse(BaseModel):
    id: int
    leader_id: int
    title: str
    description: Optional[str] = None
    max_members: int
    current_members: int
    status: str
    created_at: datetime


# ── 신청 ──

class ApplicationCreate(BaseModel):
    message: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: str   # "accepted" | "rejected"


class ApplicationResponse(BaseModel):
    id: int
    group_id: int
    applicant_id: int
    status: str
    message: Optional[str] = None
    created_at: datetime
