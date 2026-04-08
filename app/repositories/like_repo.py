"""
Like Repository (ERD Phase 1) — likes 테이블
"""

from supabase import Client
from app.database import to_row


def get_like(db: Client, user_id: int, post_id: int):
    res = (
        db.table("likes")
        .select("*")
        .eq("user_id", user_id)
        .eq("post_id", post_id)
        .execute()
    )
    return to_row(res.data[0]) if res.data else None


def get_like_count(db: Client, post_id: int) -> int:
    res = db.table("likes").select("*", count="exact").eq("post_id", post_id).execute()
    return res.count or 0


def create_like(db: Client, data: dict):
    db.table("likes").insert(data).execute()


def delete_like(db: Client, like_id: int):
    db.table("likes").delete().eq("id", like_id).execute()
