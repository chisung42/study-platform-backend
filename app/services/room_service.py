"""
Room Service — 스터디룸 비즈니스 로직

Phase 1: 목록 조회
Phase 2: 관리자 CRUD, capacity/description 추가
Phase 4: 룸 설정 (운영시간, 슬롯 단위)
"""

from sqlalchemy.orm import Session

from app.models.study_room import StudyRoom
from app.repositories import room_repo
from app.schemas.room import RoomCreate, RoomUpdate
from app.schemas.room_settings import RoomSettingsUpdate


def get_rooms(db: Session):
    """스터디룸 전체 목록"""
    return room_repo.get_rooms(db)


def get_room(db: Session, room_id: int):
    """스터디룸 1개 조회"""
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    return room


def create_room(db: Session, request: RoomCreate):
    """스터디룸 생성 (관리자 전용)"""
    new_room = StudyRoom(
        name=request.name,
        capacity=request.capacity,
        description=request.description,
    )
    return room_repo.create_room(db, new_room)


def update_room(db: Session, room_id: int, request: RoomUpdate):
    """스터디룸 수정 (관리자 전용)"""
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")

    if request.name is not None:
        room.name = request.name
    if request.capacity is not None:
        room.capacity = request.capacity
    if request.description is not None:
        room.description = request.description

    return room_repo.update_room(db, room)


def delete_room(db: Session, room_id: int):
    """스터디룸 삭제 (관리자 전용)"""
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    room_repo.delete_room(db, room)


# ── 룸 설정 (Phase 4) ──

def get_settings(db: Session, room_id: int):
    """룸 운영시간 설정 조회"""
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")
    settings = room_repo.get_settings(db, room_id)
    if not settings:
        raise ValueError("룸 설정이 없습니다. 먼저 설정을 생성해주세요")
    return settings


def update_settings(db: Session, room_id: int, request: RoomSettingsUpdate):
    """룸 운영시간 설정 생성 또는 수정 (upsert)"""
    room = room_repo.get_room_by_id(db, room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")

    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    return room_repo.create_or_update_settings(db, room_id, updates)
