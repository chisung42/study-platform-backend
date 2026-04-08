"""
Posts Router — 게시글 CRUD API

목록/상세 조회: 누구나 가능
작성/수정/삭제/좋아요/이미지: JWT 인증 필요 (Phase 4)
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.like import Like
from app.repositories import like_repo
from app.schemas.post import PostCreate, PostImageResponse, PostResponse, PostUpdate
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """게시글 전체 목록 — GET /posts/"""
    return post_service.get_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 조회 (조회수 +1) — GET /posts/{post_id}"""
    try:
        return post_service.get_post(db, post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=PostResponse)
def create_post(
    request: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """게시글 작성 — POST /posts/"""
    return post_service.create_post(db, current_user.id, request)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    request: PostUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """게시글 수정 (본인만) — PATCH /posts/{post_id}"""
    try:
        return post_service.update_post(db, current_user.id, post_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """게시글 삭제 (본인만) — DELETE /posts/{post_id}"""
    try:
        post_service.delete_post(db, current_user.id, post_id)
        return {"message": "게시글이 삭제되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/{post_id}/like")
def toggle_like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    좋아요 토글 — POST /posts/{post_id}/like
    이미 좋아요 했으면 취소, 아니면 좋아요
    """
    existing = like_repo.get_like(db, current_user.id, post_id)
    if existing:
        like_repo.delete_like(db, existing)
        message = "좋아요를 취소했습니다"
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        like_repo.create_like(db, new_like)
        message = "좋아요를 눌렀습니다"

    count = like_repo.get_like_count(db, post_id)
    return {"message": message, "like_count": count}


# ── 이미지 (Phase 3) ──

@router.post("/{post_id}/images", response_model=PostImageResponse)
async def upload_image(
    post_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """이미지 업로드 — POST /posts/{post_id}/images"""
    try:
        file_bytes = await file.read()
        return post_service.upload_image(db, current_user.id, post_id, file_bytes, file.filename)
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}/images/{image_id}")
def delete_image(
    post_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """이미지 삭제 — DELETE /posts/{post_id}/images/{image_id}"""
    try:
        post_service.delete_image(db, current_user.id, post_id, image_id)
        return {"message": "이미지가 삭제되었습니다"}
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))
