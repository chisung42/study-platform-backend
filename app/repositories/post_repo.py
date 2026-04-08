"""
Post Repository (Phase 3: images 포함)
"""

from datetime import datetime, timezone
from supabase import Client
from app.database import to_row, to_rows


def get_posts(db: Client):
    res = db.table("posts").select("*").order("created_at", desc=True).execute()
    return to_rows(res.data)


def get_post_by_id(db: Client, post_id: int):
    res = db.table("posts").select("*").eq("id", post_id).execute()
    return to_row(res.data[0]) if res.data else None


def get_post_images(db: Client, post_id: int):
    res = db.table("post_images").select("*").eq("post_id", post_id).execute()
    return to_rows(res.data)


def create_post(db: Client, data: dict):
    res = db.table("posts").insert(data).execute()
    return to_row(res.data[0]) if res.data else None


def increment_view_count(db: Client, post_id: int, current_count: int):
    db.table("posts").update({"view_count": current_count + 1}).eq("id", post_id).execute()


def update_post(db: Client, post_id: int, data: dict):
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    res = db.table("posts").update(data).eq("id", post_id).execute()
    return to_row(res.data[0]) if res.data else None


def delete_post(db: Client, post_id: int):
    db.table("posts").delete().eq("id", post_id).execute()


# ── 이미지 ──

def add_image(db: Client, post_id: int, image_url: str):
    res = db.table("post_images").insert({"post_id": post_id, "image_url": image_url}).execute()
    return to_row(res.data[0]) if res.data else None


def get_image_by_id(db: Client, image_id: int):
    res = db.table("post_images").select("*").eq("id", image_id).execute()
    return to_row(res.data[0]) if res.data else None


def delete_image(db: Client, image_id: int):
    db.table("post_images").delete().eq("id", image_id).execute()
