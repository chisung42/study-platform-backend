"""
Post Repository — 게시글 DB 조작 (Phase 3: 이미지 포함)
"""

from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.post_image import PostImage


def get_posts(db: Session):
    """
    게시글 전체 목록 (최신순)

    SQL: SELECT * FROM posts ORDER BY created_at DESC;
    """
    return db.query(Post).order_by(Post.created_at.desc()).all()


def get_post_by_id(db: Session, post_id: int):
    """SQL: SELECT * FROM posts WHERE id = ? LIMIT 1;"""
    return db.query(Post).filter(Post.id == post_id).first()


def create_post(db: Session, post: Post):
    """SQL: INSERT INTO posts (user_id, title, content) VALUES (...);"""
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post: Post):
    """
    수정된 post 객체를 DB에 반영.
    db.commit()하면 변경된 필드만 UPDATE된다.
    """
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: Post):
    """SQL: DELETE FROM posts WHERE id = ?;"""
    db.delete(post)
    db.commit()


# ── 이미지 (Phase 3) ──

def get_images_by_post(db: Session, post_id: int):
    """게시글에 첨부된 이미지 목록"""
    return db.query(PostImage).filter(PostImage.post_id == post_id).all()


def get_image_by_id(db: Session, image_id: int):
    """이미지 1개 조회"""
    return db.query(PostImage).filter(PostImage.id == image_id).first()


def add_image(db: Session, image: PostImage):
    """이미지 URL을 post_images에 저장"""
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def delete_image(db: Session, image: PostImage):
    """이미지 레코드 삭제"""
    db.delete(image)
    db.commit()
