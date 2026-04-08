"""
Like 모델 — likes 테이블

UNIQUE(user_id, post_id): 한 사용자가 같은 게시글에 좋아요를 두 번 누를 수 없다.
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Like(Base):
    __tablename__ = "likes"

    # (user_id, post_id) 조합이 중복되면 DB가 에러를 낸다
    __table_args__ = (
        UniqueConstraint("user_id", "post_id"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
