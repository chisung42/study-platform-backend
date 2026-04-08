"""
Post 스키마 (Phase 3 이후: images 포함)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PostImageResponse(BaseModel):
    id: int
    post_id: int
    image_url: str
    created_at: datetime


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    view_count: int
    created_at: datetime
    updated_at: datetime
    images: list[PostImageResponse] = []
