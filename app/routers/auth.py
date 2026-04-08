"""
Auth Router (Phase 2: bcrypt, Phase 4: JWT + /me)
"""

from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, MeResponse, SignupRequest, SignupResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=SignupResponse)
def signup(request: SignupRequest, db: Client = Depends(get_db)):
    try:
        return auth_service.signup(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Client = Depends(get_db)):
    try:
        return auth_service.login(db, request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=MeResponse)
def me(current_user=Depends(get_current_user)):
    """토큰에서 추출한 현재 유저 정보 반환 (Phase 4)"""
    return current_user
