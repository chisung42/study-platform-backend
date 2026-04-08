"""
Post Service (Phase 3: 이미지 업로드 포함)
"""

import os
import uuid
from supabase import Client

from app.repositories import post_repo
from app.schemas.post import PostCreate, PostUpdate

BUCKET = "post-images"


def get_posts(db: Client):
    posts = post_repo.get_posts(db)
    for post in posts:
        post["images"] = post_repo.get_post_images(db, post.id)
    return posts


def get_post(db: Client, post_id: int):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    post_repo.increment_view_count(db, post_id, int(post.view_count))
    post["view_count"] = int(post.view_count) + 1
    post["images"] = post_repo.get_post_images(db, post_id)
    return post


def create_post(db: Client, user_id: int, request: PostCreate):
    data = {"user_id": user_id, "title": request.title, "content": request.content}
    post = post_repo.create_post(db, data)
    post["images"] = []
    return post


def update_post(db: Client, user_id: int, post_id: int, request: PostUpdate):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if int(post.user_id) != user_id:
        raise PermissionError("본인의 게시글만 수정할 수 있습니다")

    updates = {}
    if request.title is not None:
        updates["title"] = request.title
    if request.content is not None:
        updates["content"] = request.content

    updated = post_repo.update_post(db, post_id, updates)
    updated["images"] = post_repo.get_post_images(db, post_id)
    return updated


def delete_post(db: Client, user_id: int, post_id: int):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if int(post.user_id) != user_id:
        raise PermissionError("본인의 게시글만 삭제할 수 있습니다")
    post_repo.delete_post(db, post_id)


# ── 이미지 (Phase 3) ──

def upload_image(db: Client, user_id: int, post_id: int, file_bytes: bytes, filename: str):
    """Supabase Storage에 이미지 업로드 후 URL을 post_images에 저장"""
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if int(post.user_id) != user_id:
        raise PermissionError("본인의 게시글에만 이미지를 업로드할 수 있습니다")

    ext = filename.rsplit(".", 1)[-1] if "." in filename else "png"
    storage_path = f"{post_id}/{uuid.uuid4()}.{ext}"

    db.storage.from_(BUCKET).upload(
        path=storage_path,
        file=file_bytes,
        file_options={"content-type": f"image/{ext}"},
    )
    public_url = db.storage.from_(BUCKET).get_public_url(storage_path)
    return post_repo.add_image(db, post_id, public_url)


def delete_image(db: Client, user_id: int, post_id: int, image_id: int):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")
    if int(post.user_id) != user_id:
        raise PermissionError("본인의 게시글 이미지만 삭제할 수 있습니다")

    image = post_repo.get_image_by_id(db, image_id)
    if not image:
        raise ValueError("이미지를 찾을 수 없습니다")
    if int(image.post_id) != post_id:
        raise ValueError("해당 게시글의 이미지가 아닙니다")

    post_repo.delete_image(db, image_id)
