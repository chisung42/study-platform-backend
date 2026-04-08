"""
PostImage 모델 — post_images 테이블 (Phase 3)

게시글에 첨부된 이미지 URL을 저장한다.
파일 자체는 Supabase Storage에, URL만 DB에 저장한다.
"""

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class PostImage(Base):
    __tablename__ = "post_images"

    id = Column(Integer, primary_key=True)

    # ON DELETE CASCADE: 게시글이 삭제되면 이미지 레코드도 자동 삭제
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    image_url = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
