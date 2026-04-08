"""
Room Repository — 스터디룸 DB 조작 (Phase 2: 관리자 CRUD, Phase 4: 설정)
"""

from sqlalchemy.orm import Session
from app.models.study_room import StudyRoom
from app.models.room_settings import RoomSettings


# ── 스터디룸 ──

def get_rooms(db: Session):
    """SQL: SELECT * FROM study_rooms;"""
    return db.query(StudyRoom).all()


def get_room_by_id(db: Session, room_id: int):
    """SQL: SELECT * FROM study_rooms WHERE id = ? LIMIT 1;"""
    return db.query(StudyRoom).filter(StudyRoom.id == room_id).first()


def create_room(db: Session, room: StudyRoom):
    """스터디룸 생성 (관리자 전용)"""
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def update_room(db: Session, room: StudyRoom):
    """스터디룸 수정"""
    db.commit()
    db.refresh(room)
    return room


def delete_room(db: Session, room: StudyRoom):
    """스터디룸 삭제"""
    db.delete(room)
    db.commit()


# ── 룸 설정 (Phase 4) ──

def get_settings(db: Session, room_id: int):
    """룸 운영시간/슬롯 설정 조회"""
    return db.query(RoomSettings).filter(RoomSettings.room_id == room_id).first()


def create_or_update_settings(db: Session, room_id: int, updates: dict):
    """룸 설정 생성 또는 수정 (upsert)"""
    settings = get_settings(db, room_id)
    if not settings:
        settings = RoomSettings(room_id=room_id)
        db.add(settings)
    for key, value in updates.items():
        setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings
