"""
Auth Router — 회원가입/로그인/내 정보 API

Phase 1: 회원가입, 로그인 (user_id 반환)
Phase 2: bcrypt 해싱
Phase 4: JWT 발급, GET /auth/me 추가
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, MeResponse, SignupRequest, SignupResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=SignupResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    회원가입 API

    POST /auth/signup
    요청: {"email": "...", "username": "...", "password": "...", "nickname": "..."}
    응답: {"id": 1, "email": "...", "username": "...", "nickname": "...", "role": "user", ...}
    """
    try:
        return auth_service.signup(db, request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    로그인 API

    POST /auth/login
    요청: {"email": "...", "password": "..."}
    응답: {"access_token": "...", "user_id": 1, "nickname": "...", "role": "user"}
    """
    try:
        return auth_service.login(db, request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=MeResponse)
def me(current_user=Depends(get_current_user)):
    """
    내 정보 조회 (Phase 4)

    GET /auth/me
    Authorization: Bearer {token} 헤더 필요
    """
    return current_user
