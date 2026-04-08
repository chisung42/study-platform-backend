"""
Reservations Router — 예약 API

Phase 1: 예약 생성/조회/취소 (user_id 쿼리 파라미터)
Phase 4: JWT 인증으로 변경
Phase 6: group_id 추가
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services import reservation_service

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/room/{room_id}", response_model=list[ReservationResponse])
def get_room_reservations(room_id: int, db: Session = Depends(get_db)):
    """특정 방의 예약 목록 — GET /reservations/room/{room_id}"""
    return reservation_service.get_reservations_by_room(db, room_id)


@router.get("/me", response_model=list[ReservationResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """내 예약 목록 — GET /reservations/me"""
    return reservation_service.get_my_reservations(db, current_user.id)


@router.post("/", response_model=ReservationResponse)
def create_reservation(
    request: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    예약 생성 — POST /reservations/

    개인 예약: {"room_id": 1, "start_time": "...", "end_time": "..."}
    그룹 예약: {"room_id": 1, "start_time": "...", "end_time": "...", "group_id": 3}
    """
    try:
        return reservation_service.create_reservation(db, current_user.id, request)
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """예약 취소 (본인만) — DELETE /reservations/{reservation_id}"""
    try:
        reservation_service.cancel_reservation(db, current_user.id, reservation_id)
        return {"message": "예약이 취소되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
