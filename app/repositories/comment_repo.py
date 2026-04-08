"""
Comment Repository (ERD Phase 1) — comments 테이블
"""

from supabase import Client
from app.database import to_row, to_rows


def get_comments_by_post(db: Client, post_id: int):
    res = db.table("comments").select("*").eq("post_id", post_id).order("created_at").execute()
    return to_rows(res.data)


def get_comment_by_id(db: Client, comment_id: int):
    res = db.table("comments").select("*").eq("id", comment_id).execute()
    return to_row(res.data[0]) if res.data else None


def create_comment(db: Client, data: dict):
    res = db.table("comments").insert(data).execute()
    return to_row(res.data[0]) if res.data else None


def delete_comment(db: Client, comment_id: int):
    db.table("comments").delete().eq("id", comment_id).execute()
