"""
Posts Router (Phase 3: 이미지 업로드, Phase 4: JWT 인증)
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from supabase import Client

from app.core.deps import get_current_user
from app.database import get_db
from app.repositories import like_repo
from app.schemas.post import PostCreate, PostImageResponse, PostResponse, PostUpdate
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Client = Depends(get_db)):
    return post_service.get_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Client = Depends(get_db)):
    try:
        return post_service.get_post(db, post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=PostResponse)
def create_post(
    request: PostCreate,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return post_service.create_post(db, current_user.id, request)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    request: PostUpdate,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return post_service.update_post(db, current_user.id, post_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
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
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing = like_repo.get_like(db, current_user.id, post_id)
    if existing:
        like_repo.delete_like(db, existing.id)
        message = "좋아요를 취소했습니다"
    else:
        like_repo.create_like(db, {"user_id": current_user.id, "post_id": post_id})
        message = "좋아요를 눌렀습니다"
    count = like_repo.get_like_count(db, post_id)
    return {"message": message, "like_count": count}


# ── 이미지 (Phase 3) ──

@router.post("/{post_id}/images", response_model=PostImageResponse)
async def upload_image(
    post_id: int,
    file: UploadFile = File(...),
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        file_bytes = await file.read()
        return post_service.upload_image(db, current_user.id, post_id, file_bytes, file.filename)
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{post_id}/images/{image_id}")
def delete_image(
    post_id: int,
    image_id: int,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        post_service.delete_image(db, current_user.id, post_id, image_id)
        return {"message": "이미지가 삭제되었습니다"}
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=400, detail=str(e))
