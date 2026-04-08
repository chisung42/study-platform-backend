"""
Group / Application Service — 스터디 모집 비즈니스 로직 (Phase 5)

상태 흐름: 모집중 → 모집완료 → 종료
신청 흐름: pending → accepted / rejected
"""

from sqlalchemy.orm import Session

from app.models.study_group import StudyGroup
from app.models.application import Application
from app.repositories import group_repo
from app.schemas.group import GroupCreate, GroupUpdate, ApplicationCreate, ApplicationUpdate


# ── 스터디 그룹 ──

def get_groups(db: Session):
    """모집글 전체 목록"""
    return group_repo.get_groups(db)


def get_group(db: Session, group_id: int):
    """모집글 상세 (신청 목록 포함)"""
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    group.applications = group_repo.get_applications_by_group(db, group_id)
    return group


def create_group(db: Session, user_id: int, request: GroupCreate):
    """모집글 작성"""
    new_group = StudyGroup(
        leader_id=user_id,
        title=request.title,
        description=request.description,
        max_members=request.max_members,
        current_members=1,
    )
    return group_repo.create_group(db, new_group)


def update_group(db: Session, user_id: int, group_id: int, request: GroupUpdate):
    """모집글 수정 — 조장만 가능"""
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if group.leader_id != user_id:
        raise PermissionError("조장만 수정할 수 있습니다")

    if request.title is not None:
        group.title = request.title
    if request.description is not None:
        group.description = request.description
    if request.max_members is not None:
        group.max_members = request.max_members
    if request.status is not None:
        group.status = request.status

    return group_repo.update_group(db, group)


def delete_group(db: Session, user_id: int, group_id: int):
    """모집글 삭제 — 조장만 가능"""
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if group.leader_id != user_id:
        raise PermissionError("조장만 삭제할 수 있습니다")
    group_repo.delete_group(db, group)


# ── 신청 ──

def apply(db: Session, user_id: int, group_id: int, request: ApplicationCreate):
    """스터디 신청"""
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if group.status != "모집중":
        raise ValueError("모집이 마감되었습니다")
    if group.current_members >= group.max_members:
        raise ValueError("인원이 가득 찼습니다")
    if group.leader_id == user_id:
        raise ValueError("조장은 자신의 그룹에 신청할 수 없습니다")
    if group_repo.get_application_by_user_and_group(db, group_id, user_id):
        raise ValueError("이미 신청하였습니다")

    new_app = Application(
        group_id=group_id,
        applicant_id=user_id,
        message=request.message,
    )
    return group_repo.create_application(db, new_app)


def get_applications(db: Session, user_id: int, group_id: int):
    """신청 목록 조회 — 조장만 가능"""
    group = group_repo.get_group_by_id(db, group_id)
    if not group:
        raise ValueError("스터디 그룹을 찾을 수 없습니다")
    if group.leader_id != user_id:
        raise PermissionError("조장만 신청 목록을 조회할 수 있습니다")
    return group_repo.get_applications_by_group(db, group_id)


def decide_application(db: Session, user_id: int, application_id: int, request: ApplicationUpdate):
    """신청 수락/거절 — 조장만 가능"""
    app = group_repo.get_application_by_id(db, application_id)
    if not app:
        raise ValueError("신청을 찾을 수 없습니다")

    group = group_repo.get_group_by_id(db, app.group_id)
    if group.leader_id != user_id:
        raise PermissionError("조장만 수락/거절할 수 있습니다")
    if request.status not in ("accepted", "rejected"):
        raise ValueError("status는 accepted 또는 rejected여야 합니다")

    app.status = request.status
    group_repo.update_application(db, app)

    # 수락 시 현재 인원 +1, 정원 충족 시 모집완료 자동 전환
    if request.status == "accepted":
        group.current_members += 1
        if group.current_members >= group.max_members:
            group.status = "모집완료"
        group_repo.update_group(db, group)

    return app
