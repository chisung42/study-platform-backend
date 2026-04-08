"""
Room Service (Phase 2: 관리자 CRUD, Phase 4: 설정)
"""

from supabase import Client
from app.repositories import room_repo
from app.schemas.room import RoomCreate, RoomUpdate
from app.schemas.room_settings import RoomSettingsUpdate


def get_rooms(db: Client):
    return room_repo.get_rooms(db)


def get_room(db: Client, room_id: int):
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    return room


def create_room(db: Client, request: RoomCreate):
    data = {"name": request.name, "capacity": request.capacity}
    if request.description:
        data["description"] = request.description
    return room_repo.create_room(db, data)


def update_room(db: Client, room_id: int, request: RoomUpdate):
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    return room_repo.update_room(db, room_id, updates)


def delete_room(db: Client, room_id: int):
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    room_repo.delete_room(db, room_id)


# ── 설정 (Phase 4) ──

def get_settings(db: Client, room_id: int):
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    settings = room_repo.get_settings(db, room_id)
    if not settings:
        raise ValueError("룸 설정이 없습니다")
    return settings


def update_settings(db: Client, room_id: int, request: RoomSettingsUpdate):
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    return room_repo.upsert_settings(db, room_id, updates)
