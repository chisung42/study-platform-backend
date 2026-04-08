"""
Groups Router — 스터디 모집 시스템 API (Phase 5)

모집글: 누구나 조회, 로그인 필요 작성/수정/삭제
신청: 로그인 필요, 조장만 신청 목록/수락/거절 가능
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.group import (
    ApplicationCreate, ApplicationResponse, ApplicationUpdate,
    GroupCreate, GroupResponse, GroupUpdate,
)
from app.services import group_service

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=list[GroupResponse])
def get_groups(db: Session = Depends(get_db)):
    """모집글 전체 목록 — GET /groups/"""
    return group_service.get_groups(db)


@router.post("/", response_model=GroupResponse)
def create_group(
    request: GroupCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """모집글 작성 — POST /groups/"""
    return group_service.create_group(db, current_user.id, request)


@router.get("/{group_id}")
def get_group(group_id: int, db: Session = Depends(get_db)):
    """모집글 상세 (신청 목록 포함) — GET /groups/{group_id}"""
    try:
        return group_service.get_group(db, group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: int,
    request: GroupUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """모집글 수정 (조장만) — PATCH /groups/{group_id}"""
    try:
        return group_service.update_group(db, current_user.id, group_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{group_id}")
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """모집글 삭제 (조장만) — DELETE /groups/{group_id}"""
    try:
        group_service.delete_group(db, current_user.id, group_id)
        return {"message": "모집글이 삭제되었습니다"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


# ── 신청 ──

@router.post("/{group_id}/apply", response_model=ApplicationResponse)
def apply(
    group_id: int,
    request: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """스터디 신청 — POST /groups/{group_id}/apply"""
    try:
        return group_service.apply(db, current_user.id, group_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{group_id}/applications", response_model=list[ApplicationResponse])
def get_applications(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """신청 목록 (조장만) — GET /groups/{group_id}/applications"""
    try:
        return group_service.get_applications(db, current_user.id, group_id)
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def decide_application(
    application_id: int,
    request: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """신청 수락/거절 (조장만) — PATCH /groups/applications/{application_id}"""
    try:
        return group_service.decide_application(db, current_user.id, application_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
