"""
Rooms Router — 스터디룸 API

Phase 1: 목록 조회
Phase 2: 관리자 전용 CRUD (admin role 필요)
Phase 4: 룸 설정 (운영시간/슬롯) 조회·수정
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_admin
from app.database import get_db
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate
from app.schemas.room_settings import RoomSettingsResponse, RoomSettingsUpdate
from app.services import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    """스터디룸 전체 목록 — GET /rooms/"""
    return room_service.get_rooms(db)


@router.post("/", response_model=RoomResponse)
def create_room(
    request: RoomCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """스터디룸 생성 (admin 전용) — POST /rooms/"""
    return room_service.create_room(db, request)


@router.patch("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    request: RoomUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """스터디룸 수정 (admin 전용) — PATCH /rooms/{room_id}"""
    try:
        return room_service.update_room(db, room_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """스터디룸 삭제 (admin 전용) — DELETE /rooms/{room_id}"""
    try:
        room_service.delete_room(db, room_id)
        return {"message": "스터디룸이 삭제되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── 룸 설정 (Phase 4) ──

@router.get("/{room_id}/settings", response_model=RoomSettingsResponse)
def get_settings(
    room_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """룸 설정 조회 (admin 전용) — GET /rooms/{room_id}/settings"""
    try:
        return room_service.get_settings(db, room_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{room_id}/settings", response_model=RoomSettingsResponse)
def update_settings(
    room_id: int,
    request: RoomSettingsUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    """룸 설정 수정 (admin 전용) — PATCH /rooms/{room_id}/settings"""
    try:
        return room_service.update_settings(db, room_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
