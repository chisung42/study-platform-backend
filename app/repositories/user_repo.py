"""
User Repository (ERD Phase 1) — users 테이블
"""

from supabase import Client
from app.database import to_row


def get_user_by_email(db: Client, email: str):
    res = db.table("users").select("*").eq("email", email).execute()
    return to_row(res.data[0]) if res.data else None


def get_user_by_id(db: Client, user_id: int):
    res = db.table("users").select("*").eq("id", user_id).execute()
    return to_row(res.data[0]) if res.data else None


def create_user(db: Client, data: dict):
    res = db.table("users").insert(data).execute()
    return to_row(res.data[0]) if res.data else None
