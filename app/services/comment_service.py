"""
Comment Service (ERD Phase 1)
"""

from supabase import Client
from app.repositories import comment_repo, post_repo
from app.schemas.comment import CommentCreate


def get_comments(db: Client, post_id: int):
    return comment_repo.get_comments_by_post(db, post_id)


def create_comment(db: Client, user_id: int, post_id: int, request: CommentCreate):
    post = post_repo.get_post_by_id(db, post_id)
    if not post:
        raise ValueError("게시글을 찾을 수 없습니다")

    data = {
        "post_id": post_id,
        "user_id": user_id,
        "content": request.content,
    }
    return comment_repo.create_comment(db, data)


def delete_comment(db: Client, user_id: int, comment_id: int):
    comment = comment_repo.get_comment_by_id(db, comment_id)
    if not comment:
        raise ValueError("댓글을 찾을 수 없습니다")
    if int(comment.user_id) != user_id:
        raise PermissionError("본인의 댓글만 삭제할 수 있습니다")

    comment_repo.delete_comment(db, comment_id)
