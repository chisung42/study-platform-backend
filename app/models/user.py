"""
User 모델 — users 테이블

Phase 1: id, username, password, email, nickname, created_at
Phase 2: role 추가 (user / admin)
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    # primary_key=True: 각 행을 구분하는 고유 번호 (PK)
    # DB에서 자동으로 1, 2, 3... 증가한다 (SERIAL)
    id = Column(Integer, primary_key=True)

    # nullable=False: NULL 허용 안 함 → 반드시 입력해야 함
    username = Column(String(50), nullable=False)

    # 비밀번호는 해싱하면 길어지므로 넉넉하게 255
    password = Column(String(255), nullable=False)

    # unique=True: 같은 이메일로 두 번 가입 불가
    email = Column(String(255), unique=True, nullable=False)

    nickname = Column(String(50), nullable=False)

    # Phase 2: 역할 (user / admin), 기본값 'user'
    role = Column(String(20), nullable=False, default="user")

    # server_default=func.now(): INSERT 시 DB가 자동으로 현재 시각 입력
    created_at = Column(DateTime(timezone=True), server_default=func.now())
