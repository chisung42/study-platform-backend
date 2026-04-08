"""
Post Service — 게시글 비즈니스 로직

규칙:
- 게시글 수정/삭제는 작성자 본인만 가능
- 게시글 조회 시 조회수 +1
- Phase 3: 이미지 업로드/삭제
"""

import uuid
from sqlalchemy.orm import Session

from app.models.post import Post
from app.models.post_image import PostImage
from app.repositories import post_repo
from app.schemas.post import PostCreate, PostUpdate

BUCKET = "post-images"


def get_posts(db: Session):
    """게시글 전체 목록 (이미지 포함)"""
    posts = post_repo.get_posts(db)
    for post in posts:
        post.images = post_repo.get_images_by_post(db, post.id)
    return posts


def get_post(db: Session, post_id: int):
    """게시글 상세 조회 + 조회수 증가"""
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")

    # 조회수 +1
    post.view_count += 1
    post_repo.update_post(db, post)

    post.images = post_repo.get_images_by_post(db, post.id)
    return post


def create_post(db: Session, user_id: int, request: PostCreate):
    """게시글 작성"""
    new_post = Post(
        user_id=user_id,
        title=request.title,
        content=request.content,
    )
    post = post_repo.create_post(db, new_post)
    post.images = []
    return post


def update_post(db: Session, user_id: int, post_id: int, request: PostUpdate):
    """게시글 수정 — 작성자 본인만 가능"""
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글만 수정할 수 있습니다")

    if request.title is not None:
        post.title = request.title
    if request.content is not None:
        post.content = request.content

    post_repo.update_post(db, post)
    post.images = post_repo.get_images_by_post(db, post.id)
    return post


def delete_post(db: Session, user_id: int, post_id: int):
    """게시글 삭제 — 작성자 본인만 가능"""
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글만 삭제할 수 있습니다")

    post_repo.delete_post(db, post)


# ── 이미지 (Phase 3) ──

def upload_image(db: Session, user_id: int, post_id: int, file_bytes: bytes, filename: str):
    """Supabase Storage에 업로드 후 URL을 post_images에 저장"""
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글에만 이미지를 업로드할 수 있습니다")

    from app.database import get_storage_client
    storage = get_storage_client()
    if not storage:
        raise ValueError("Storage 클라이언트를 사용할 수 없습니다")

    ext = filename.rsplit(".", 1)[-1] if "." in filename else "png"
    storage_path = f"{post_id}/{uuid.uuid4()}.{ext}"

    storage.storage.from_(BUCKET).upload(
        path=storage_path,
        file=file_bytes,
        file_options={"content-type": f"image/{ext}"},
    )
    public_url = storage.storage.from_(BUCKET).get_public_url(storage_path)

    image = PostImage(post_id=post_id, image_url=public_url)
    return post_repo.add_image(db, image)


def delete_image(db: Session, user_id: int, post_id: int, image_id: int):
    """이미지 삭제 — 게시글 작성자만 가능"""
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if post.user_id != user_id:
        raise PermissionError("본인의 게시글 이미지만 삭제할 수 있습니다")

    image = post_repo.get_image_by_id(db, image_id)
    if not image:
        raise ValueError("이미지를 찾을 수 없습니다")
    if image.post_id != post_id:
        raise ValueError("해당 게시글의 이미지가 아닙니다")

    post_repo.delete_image(db, image)
