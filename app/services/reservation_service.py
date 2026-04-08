"""
Reservation Service (Phase 4: 운영시간/슬롯 검증, Phase 6: 그룹 예약)
"""

from datetime import datetime, time
from supabase import Client

from app.repositories import reservation_repo, room_repo, group_repo
from app.schemas.reservation import ReservationCreate


def get_reservations_by_room(db: Client, room_id: int):
    return reservation_repo.get_reservations_by_room(db, room_id)


def get_my_reservations(db: Client, user_id: int):
    return reservation_repo.get_reservations_by_user(db, user_id)


def create_reservation(db: Client, user_id: int, request: ReservationCreate):
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
    if request.group_id is not None:
        group = group_repo.get_group_by_id(db, request.group_id)
        if not group:
            raise ValueError("스터디 그룹을 찾을 수 없습니다")
        if group.status != "모집완료":
            raise ValueError("모집이 완료된 그룹만 예약할 수 있습니다")
        if int(group.leader_id) != user_id:
            raise PermissionError("조장만 그룹 예약을 할 수 있습니다")
        new_members = int(group.current_members)
        if new_members > int(room.capacity):
            raise ValueError("그룹 인원이 룸 수용 인원을 초과합니다")

    # 5. 수용 인원 겹침 체크 (Phase 2/6)
    overlapping = reservation_repo.get_overlapping_reservations(
        db, request.room_id, request.start_time, request.end_time
    )
    total_occupancy = _calc_occupancy(db, overlapping)
    if total_occupancy + new_members > int(room.capacity):
        raise ValueError("수용 인원을 초과합니다")

    data = {
        "user_id": user_id,
        "room_id": request.room_id,
        "start_time": request.start_time.isoformat(),
        "end_time": request.end_time.isoformat(),
    }
    if request.group_id is not None:
        data["group_id"] = request.group_id
    return reservation_repo.create_reservation(db, data)


def cancel_reservation(db: Client, user_id: int, reservation_id: int):
    reservation = reservation_repo.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise ValueError("예약을 찾을 수 없습니다")
    if int(reservation.user_id) != user_id:
        raise PermissionError("본인의 예약만 취소할 수 있습니다")
    reservation_repo.delete_reservation(db, reservation_id)


# ── 헬퍼 ──

def _validate_operating_hours(start: datetime, end: datetime, settings):
    """예약 시간이 운영시간 내인지, 슬롯 단위에 맞는지 검증"""
    open_h, open_m = map(int, settings.open_time[:5].split(":"))
    close_h, close_m = map(int, settings.close_time[:5].split(":"))
    open_t = time(open_h, open_m)
    close_t = time(close_h, close_m)

    if start.time() < open_t:
        raise ValueError(f"운영 시작 시간({settings.open_time}) 이전에는 예약할 수 없습니다")
    if end.time() > close_t:
        raise ValueError(f"운영 종료 시간({settings.close_time}) 이후에는 예약할 수 없습니다")

    duration_minutes = int((end - start).total_seconds() // 60)
    slot = int(settings.slot_duration)
    if duration_minutes % slot != 0:
        raise ValueError(f"예약 시간은 {slot}분 단위여야 합니다")


def _calc_occupancy(db: Client, overlapping: list) -> int:
    """겹치는 예약들의 총 인원 계산 (Phase 6: 그룹 예약은 그룹 인원으로 계산)"""
    total = 0
    for r in overlapping:
        if r.get("group_id"):
            group = group_repo.get_group_by_id(db, r["group_id"])
            total += int(group.current_members) if group else 1
        else:
            total += 1
    return total
