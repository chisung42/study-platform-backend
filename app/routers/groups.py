"""
Groups Router (Phase 5: 스터디 모집 시스템)
"""

from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.group import (
    ApplicationCreate, ApplicationResponse, ApplicationUpdate,
    GroupCreate, GroupResponse, GroupUpdate,
)
from app.services import group_service

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=list[GroupResponse])
def get_groups(db: Client = Depends(get_db)):
    return group_service.get_groups(db)


@router.post("/", response_model=GroupResponse)
def create_group(
    request: GroupCreate,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return group_service.create_group(db, current_user.id, request)


@router.get("/{group_id}")
def get_group(group_id: int, db: Client = Depends(get_db)):
    try:
        return group_service.get_group(db, group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: int,
    request: GroupUpdate,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return group_service.update_group(db, current_user.id, group_id, request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{group_id}")
def delete_group(
    group_id: int,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
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
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return group_service.apply(db, current_user.id, group_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{group_id}/applications", response_model=list[ApplicationResponse])
def get_applications(
    group_id: int,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return group_service.get_applications(db, current_user.id, group_id)
    except (ValueError, PermissionError) as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
def decide_application(
    application_id: int,
    request: ApplicationUpdate,
    db: Client = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return group_service.decide_application(db, current_user.id, application_id, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
