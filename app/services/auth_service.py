"""
Auth Service (Phase 2: bcrypt, Phase 4: JWT)
"""

from supabase import Client

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories import user_repo
from app.schemas.auth import LoginRequest, SignupRequest


def signup(db: Client, request: SignupRequest):
    """
    회원가입
    - 이메일 중복 체크
    - bcrypt로 비밀번호 해싱 (Phase 2)
    """
    if user_repo.get_user_by_email(db, request.email):
        raise ValueError("이미 존재하는 이메일입니다")

    data = {
        "username": request.username,
        "password": hash_password(request.password),
        "email": request.email,
        "nickname": request.nickname,
    }
    return user_repo.create_user(db, data)


def login(db: Client, request: LoginRequest):
    """
    로그인
    - bcrypt verify
    - JWT 발급 (Phase 4)
    """
    user = user_repo.get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.password):
        raise ValueError("이메일 또는 비밀번호가 올바르지 않습니다")

    token = create_access_token(user_id=user.id, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "nickname": user.nickname,
        "role": user.role,
    }
