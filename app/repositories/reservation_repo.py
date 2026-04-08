"""
Reservation Repository — 예약 DB 조작 (Phase 6: group_id, 인원 계산)
"""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reservation import Reservation


def get_reservations_by_room(db: Session, room_id: int):
    """
    특정 스터디룸의 예약 목록 (시작 시간 순)

    SQL: SELECT * FROM reservations WHERE room_id = ? ORDER BY start_time;
    """
    return db.query(Reservation).filter(Reservation.room_id == room_id).order_by(Reservation.start_time.asc()).all()


def get_reservations_by_user(db: Session, user_id: int):
    """
    특정 유저의 예약 목록

    SQL: SELECT * FROM reservations WHERE user_id = ? ORDER BY start_time;
    """
    return db.query(Reservation).filter(Reservation.user_id == user_id).order_by(Reservation.start_time.asc()).all()


def get_reservation_by_id(db: Session, reservation_id: int):
    """예약 1개 조회"""
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()


def get_overlapping_reservations(db: Session, room_id: int, start_time: datetime, end_time: datetime):
    """
    겹치는 예약 목록 반환 (Phase 6: 인원 합산 계산용)

    겹치는 조건: 기존 start < 새 end AND 기존 end > 새 start

    SQL: SELECT * FROM reservations
         WHERE room_id = ? AND start_time < ? AND end_time > ?;
    """
    return db.query(Reservation).filter(
        and_(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time,
        )
    ).all()


def create_reservation(db: Session, reservation: Reservation):
    """예약 생성"""
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


def delete_reservation(db: Session, reservation: Reservation):
    """예약 취소"""
    db.delete(reservation)
    db.commit()
