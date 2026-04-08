from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, posts, comments, rooms, reservations, groups

app = FastAPI(title="스터디 플랫폼 API", version="Phase 6")


@app.on_event("startup")
def startup():
    """앱 시작 시 Supabase Storage 버킷 초기화 (Phase 3)"""
    from app.database import get_db
    db = get_db()
    try:
        buckets = [b.name for b in db.storage.list_buckets()]
        if "post-images" not in buckets:
            db.storage.create_bucket("post-images", options={"public": True})
    except Exception:
        pass  # 이미 존재하거나 권한 없을 경우 무시

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(auth.router, prefix=PREFIX)
app.include_router(posts.router, prefix=PREFIX)
app.include_router(comments.router, prefix=PREFIX)
app.include_router(rooms.router, prefix=PREFIX)
app.include_router(reservations.router, prefix=PREFIX)
app.include_router(groups.router, prefix=PREFIX)


@app.get("/")
def root():
    return {"message": "스터디 플랫폼 API — Phase 6"}
