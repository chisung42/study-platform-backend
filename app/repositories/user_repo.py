"""
User Repository — DB에서 유저를 조회하고 생성하는 계층

이 파일은 오직 DB 작업만 한다.
비즈니스 규칙은 Service의 역할.
"""

from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_email(db: Session, email: str):
    """
    이메일로 유저 조회

    SQL: SELECT * FROM users WHERE email = ? LIMIT 1;
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """
    id로 유저 조회

    SQL: SELECT * FROM users WHERE id = ? LIMIT 1;
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: User):
    """
    새 유저를 DB에 저장

    db.add(user)     → INSERT 준비
    db.commit()      → 실제로 DB에 반영
    db.refresh(user) → DB가 자동 생성한 값(id, created_at)을 user 객체에 채워줌
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
