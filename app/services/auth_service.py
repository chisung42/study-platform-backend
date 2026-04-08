"""
Auth Service — 회원가입/로그인 비즈니스 로직

Phase 1: 비밀번호 평문 저장/비교
Phase 2: bcrypt 해싱, role 추가
Phase 4: JWT 발급
"""

from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories import user_repo
from app.schemas.auth import LoginRequest, SignupRequest


def signup(db: Session, request: SignupRequest):
    """
    회원가입

    1. 이메일 중복 체크
    2. bcrypt로 비밀번호 해싱 후 저장 (Phase 2)
    """
    if user_repo.get_user_by_email(db, request.email):
        raise ValueError("이미 존재하는 이메일입니다")

    new_user = User(
        email=request.email,
        username=request.username,
        password=hash_password(request.password),
        nickname=request.nickname,
    )
    return user_repo.create_user(db, new_user)


def login(db: Session, request: LoginRequest):
    """
    로그인

    1. email로 유저 조회
    2. bcrypt verify (Phase 2)
    3. JWT 발급 (Phase 4)
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
