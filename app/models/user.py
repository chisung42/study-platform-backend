"""
User 모델 — users 테이블 (ERD Phase 1)

id        INTEGER PK (BIGSERIAL)
username  VARCHAR
password  VARCHAR
email     VARCHAR UNIQUE
nickname  VARCHAR
created_at DATETIME
"""

from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    nickname = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
