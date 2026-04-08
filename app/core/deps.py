"""
deps.py — FastAPI 공통 의존성 (Phase 4)

get_current_user : JWT 검증 → 현재 유저 반환
require_admin    : admin 역할 확인
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from supabase import Client

from app.core.security import decode_token
from app.database import get_db
from app.repositories import user_repo

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Client = Depends(get_db),
):
    """
    Authorization: Bearer <token> 헤더에서 JWT를 추출하여 검증.
    유효하면 users 테이블의 Row를 반환.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


def require_admin(current_user=Depends(get_current_user)):
    """admin 역할이 아니면 403"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다")
    return current_user
