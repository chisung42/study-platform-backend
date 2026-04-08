"""
Room Repository (Phase 2: capacity/description, Phase 4: settings)
"""

from supabase import Client
from app.database import to_row, to_rows


def get_rooms(db: Client):
    res = db.table("study_rooms").select("*").execute()
    return to_rows(res.data)


def get_room_by_id(db: Client, room_id: int):
    res = db.table("study_rooms").select("*").eq("id", room_id).execute()
    return to_row(res.data[0]) if res.data else None


def create_room(db: Client, data: dict):
    res = db.table("study_rooms").insert(data).execute()
    return to_row(res.data[0]) if res.data else None


def update_room(db: Client, room_id: int, data: dict):
    res = db.table("study_rooms").update(data).eq("id", room_id).execute()
    return to_row(res.data[0]) if res.data else None


def delete_room(db: Client, room_id: int):
    db.table("study_rooms").delete().eq("id", room_id).execute()


# ── 룸 설정 ──

def get_settings(db: Client, room_id: int):
    res = db.table("room_settings").select("*").eq("room_id", room_id).execute()
    return to_row(res.data[0]) if res.data else None


def upsert_settings(db: Client, room_id: int, data: dict):
    data["room_id"] = room_id
    res = db.table("room_settings").upsert(data, on_conflict="room_id").execute()
    return to_row(res.data[0]) if res.data else None
