"""
Reservation Repository (Phase 6: group_id, 인원 계산)
"""

from datetime import datetime
from supabase import Client
from app.database import to_row, to_rows


def get_reservations_by_room(db: Client, room_id: int):
    res = (
        db.table("reservations")
        .select("*")
        .eq("room_id", room_id)
        .order("start_time")
        .execute()
    )
    return to_rows(res.data)


def get_reservations_by_user(db: Client, user_id: int):
    res = (
        db.table("reservations")
        .select("*")
        .eq("user_id", user_id)
        .order("start_time")
        .execute()
    )
    return to_rows(res.data)


def get_reservation_by_id(db: Client, reservation_id: int):
    res = db.table("reservations").select("*").eq("id", reservation_id).execute()
    return to_row(res.data[0]) if res.data else None


def get_overlapping_reservations(db: Client, room_id: int, start_time: datetime, end_time: datetime):
    """겹치는 예약 전체 반환 (Phase 6 capacity 계산용)"""
    res = (
        db.table("reservations")
        .select("*")
        .eq("room_id", room_id)
        .lt("start_time", end_time.isoformat())
        .gt("end_time", start_time.isoformat())
        .execute()
    )
    return to_rows(res.data)


def create_reservation(db: Client, data: dict):
    res = db.table("reservations").insert(data).execute()
    return to_row(res.data[0]) if res.data else None


def delete_reservation(db: Client, reservation_id: int):
    db.table("reservations").delete().eq("id", reservation_id).execute()
