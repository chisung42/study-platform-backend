"""
Auth 스키마 (Phase 1~4)
"""

from datetime import datetime
from pydantic import BaseModel


class SignupRequest(BaseModel):
    username: str
    password: str
    email: str
    nickname: str


class SignupResponse(BaseModel):
    id: int
    username: str
    email: str
    nickname: str
    role: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    nickname: str
    role: str


class MeResponse(BaseModel):
    id: int
    username: str
    email: str
    nickname: str
    role: str
    created_at: datetime
