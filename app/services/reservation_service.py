"""
Reservation Service — 예약 비즈니스 로직

Phase 1: 1인 예약, 시간 겹침 방지
Phase 2: capacity 기반 인원 합산 체크
Phase 4: 운영시간/슬롯 단위 검증
Phase 6: 그룹 예약 (group_id)
"""

from datetime import datetime, time
from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.repositories import reservation_repo, room_repo, group_repo
from app.schemas.reservation import ReservationCreate


def get_reservations_by_room(db: Session, room_id: int):
    """특정 방의 예약 목록"""
    return reservation_repo.get_reservations_by_room(db, room_id)


def get_my_reservations(db: Session, user_id: int):
    """내 예약 목록"""
    return reservation_repo.get_reservations_by_user(db, user_id)


def create_reservation(db: Session, user_id: int, request: ReservationCreate):
    """
    예약 생성

    1. 스터디룸 존재 확인
    2. 시작 < 종료 시간 확인
    3. 운영시간/슬롯 단위 검증 (Phase 4, 설정 있을 때만)
    4. 그룹 예약 검증 (Phase 6)
    5. capacity 기반 인원 합산 체크 (Phase 2/6)
    6. 예약 생성
    """
    # 1. 룸 존재 확인
    room = room_repo.get_room_by_id(db, request.room_id)
    if not room:
        raise ValueError("스터디룸을 찾을 수 없습니다")

    # 2. 시간 유효성
    if request.start_time >= request.end_time:
        raise ValueError("시작 시간은 종료 시간보다 앞이어야 합니다")

    # 3. 운영시간 검증 (Phase 4)
    settings = room_repo.get_settings(db, request.room_id)
    if settings:
        _validate_operating_hours(request.start_time, request.end_time, settings)

    # 4. 그룹 예약 검증 (Phase 6)
    new_members = 1
    group_id = getattr(request, "group_id", None)
    if group_id:
        group = group_repo.get_group_by_id(db, group_id)
        if not group:
            raise ValueError("스터디 그룹을 찾을 수 없습니다")
        if group.status != "모집완료":
            raise ValueError("모집이 완료된 그룹만 예약할 수 있습니다")
        if group.leader_id != user_id:
            raise PermissionError("조장만 그룹 예약을 할 수 있습니다")
        new_members = group.current_members
        if new_members > room.capacity:
            raise ValueError("그룹 인원이 룸 수용 인원을 초과합니다")

    # 5. 겹치는 예약의 총 인원 체크 (Phase 2/6)
    overlapping = reservation_repo.get_overlapping_reservations(
        db, request.room_id, request.start_time, request.end_time
    )
    total_occupancy = _calc_occupancy(db, overlapping)
    if total_occupancy + new_members > room.capacity:
        raise ValueError("수용 인원을 초과합니다")

    # 6. 예약 생성
    new_reservation = Reservation(
        user_id=user_id,
        room_id=request.room_id,
        start_time=request.start_time,
        end_time=request.end_time,
        group_id=group_id,
    )
    return reservation_repo.create_reservation(db, new_reservation)


def cancel_reservation(db: Session, user_id: int, reservation_id: int):
    """예약 취소 — 본인만 가능"""
    reservation = reservation_repo.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise ValueError("예약을 찾을 수 없습니다")
    if reservation.user_id != user_id:
        raise PermissionError("본인의 예약만 취소할 수 있습니다")

    reservation_repo.delete_reservation(db, reservation)


# ── 헬퍼 ──

def _validate_operating_hours(start: datetime, end: datetime, settings):
    """운영시간 내인지, 슬롯 단위에 맞는지 검증"""
    open_h, open_m = map(int, settings.open_time[:5].split(":"))
    close_h, close_m = map(int, settings.close_time[:5].split(":"))
    open_t = time(open_h, open_m)
    close_t = time(close_h, close_m)

    if start.time() < open_t:
        raise ValueError(f"운영 시작 시간({settings.open_time}) 이전에는 예약할 수 없습니다")
    if end.time() > close_t:
        raise ValueError(f"운영 종료 시간({settings.close_time}) 이후에는 예약할 수 없습니다")

    duration_minutes = int((end - start).total_seconds() // 60)
    if duration_minutes % settings.slot_duration != 0:
        raise ValueError(f"예약 시간은 {settings.slot_duration}분 단위여야 합니다")


def _calc_occupancy(db: Session, overlapping: list) -> int:
    """겹치는 예약들의 총 인원 계산 (그룹 예약은 그룹 인원으로 계산)"""
    total = 0
    for r in overlapping:
        if r.group_id:
            group = group_repo.get_group_by_id(db, r.group_id)
            total += group.current_members if group else 1
        else:
            total += 1
    return total
