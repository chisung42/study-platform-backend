"""
Group / Application Service (Phase 5)
"""

from supabase import Client
from app.repositories import group_repo
from app.schemas.group import GroupCreate, GroupUpdate, ApplicationCreate, ApplicationUpdate


# ── 스터디 그룹 ──

def get_groups(db: Client):
    return group_repo.get_groups(db)


def get_group(db: Client, group_id: int):
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    group["applications"] = group_repo.get_applications_by_group(db, group_id)
    return group


def create_group(db: Client, user_id: int, request: GroupCreate):
    data = {
        "leader_id": user_id,
        "title": request.title,
        "max_members": request.max_members,
        "current_members": 1,
    }
    if request.description:
        data["description"] = request.description
    return group_repo.create_group(db, data)


def update_group(db: Client, user_id: int, group_id: int, request: GroupUpdate):
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if int(group.leader_id) != user_id:
        raise PermissionError("조장만 수정할 수 있습니다")
    updates = {k: v for k, v in request.model_dump().items() if v is not None}
    return group_repo.update_group(db, group_id, updates)


def delete_group(db: Client, user_id: int, group_id: int):
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if int(group.leader_id) != user_id:
        raise PermissionError("조장만 삭제할 수 있습니다")
    group_repo.delete_group(db, group_id)


# ── 신청 ──

def apply(db: Client, user_id: int, group_id: int, request: ApplicationCreate):
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if group.status != "모집중":
        raise ValueError("모집이 마감되었습니다")
    if int(group.current_members) >= int(group.max_members):
        raise ValueError("인원이 가득 찼습니다")
    if int(group.leader_id) == user_id:
        raise ValueError("조장은 자신의 그룹에 신청할 수 없습니다")

    existing = group_repo.get_application_by_user_and_group(db, group_id, user_id)
    if existing:
        raise ValueError("이미 신청하였습니다")

    data = {"group_id": group_id, "applicant_id": user_id}
    if request.message:
        data["message"] = request.message
    return group_repo.create_application(db, data)


def get_applications(db: Client, user_id: int, group_id: int):
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if int(group.leader_id) != user_id:
        raise PermissionError("조장만 신청 목록을 조회할 수 있습니다")
    return group_repo.get_applications_by_group(db, group_id)


def decide_application(db: Client, user_id: int, application_id: int, request: ApplicationUpdate):
    app = group_repo.get_application_by_id(db, application_id)
    if not app:
        raise ValueError("신청을 찾을 수 없습니다")

    group = group_repo.get_group_by_id(db, app.group_id)
    if int(group.leader_id) != user_id:
        raise PermissionError("조장만 수락/거절할 수 있습니다")

    if request.status not in ("accepted", "rejected"):
        raise ValueError("status는 accepted 또는 rejected여야 합니다")

    updated_app = group_repo.update_application(db, application_id, {"status": request.status})

    # 수락 시 인원 증가 + 모집완료 자동 전환
    if request.status == "accepted":
        new_count = int(group.current_members) + 1
        group_updates = {"current_members": new_count}
        if new_count >= int(group.max_members):
            group_updates["status"] = "모집완료"
        group_repo.update_group(db, group.id, group_updates)

    return updated_app
