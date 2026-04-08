"""
database.py — Supabase(PostgreSQL) 연결 설정

이 파일이 하는 일:
1. .env 파일에서 DB 주소(DATABASE_URL)를 읽어온다
2. SQLAlchemy가 DB에 연결할 수 있도록 설정한다
3. API 요청마다 DB 세션을 열고 닫는 함수를 제공한다

Supabase는 내부적으로 PostgreSQL이다.
SQLAlchemy는 PostgreSQL에 직접 연결할 수 있다.
그래서 Supabase를 "그냥 PostgreSQL DB"로 쓰는 것.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")

# engine: 어떤 DB에 어떻게 연결할지 설정 (아직 실제 연결 X)
engine = create_engine(DATABASE_URL)

# SessionLocal: DB와 대화하는 통로(세션) 공장
# autocommit=False → 명시적으로 commit()을 호출해야 DB에 반영된다
# autoflush=False  → commit() 전에 자동으로 DB에 보내지 않는다
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: 모든 Model 클래스가 상속받는 부모 클래스
Base = declarative_base()


def get_db():
    """
    FastAPI Depends()에서 사용하는 DB 세션 생성/반환 함수.

    사용법:
        @router.get("/posts")
        def get_posts(db: Session = Depends(get_db)):
            ...

    요청이 들어오면 세션을 열고, 응답이 끝나면 자동으로 닫는다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Phase 3: Supabase Storage 전용 클라이언트 ──
# 이미지 파일 업로드에만 사용 (DB 연결은 위의 SQLAlchemy 사용)

def get_storage_client():
    """Supabase Storage 업로드용 클라이언트 반환"""
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if url and key:
        return create_client(url, key)
    return None
