"""
Group / Application Repository — 스터디 모집 DB 조작 (Phase 5)
"""

from sqlalchemy.orm import Session
from app.models.study_group import StudyGroup
from app.models.application import Application


# ── 스터디 그룹 ──

def get_groups(db: Session):
    """모집글 전체 목록 (최신순)"""
    return db.query(StudyGroup).order_by(StudyGroup.created_at.desc()).all()


def get_group_by_id(db: Session, group_id: int):
    """모집글 1개 조회"""
    return db.query(StudyGroup).filter(StudyGroup.id == group_id).first()


def create_group(db: Session, group: StudyGroup):
    """모집글 생성"""
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def update_group(db: Session, group: StudyGroup):
    """모집글 수정 (이미 변경된 객체를 commit으로 반영)"""
    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, group: StudyGroup):
    """모집글 삭제"""
    db.delete(group)
    db.commit()


# ── 신청 ──

def get_application_by_id(db: Session, application_id: int):
    """신청 1개 조회"""
    return db.query(Application).filter(Application.id == application_id).first()


def get_applications_by_group(db: Session, group_id: int):
    """특정 모집글의 신청 목록"""
    return db.query(Application).filter(Application.group_id == group_id).all()


def get_application_by_user_and_group(db: Session, group_id: int, applicant_id: int):
    """중복 신청 체크용 조회"""
    return db.query(Application).filter(
        Application.group_id == group_id,
        Application.applicant_id == applicant_id,
    ).first()


def create_application(db: Session, application: Application):
    """신청 생성"""
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def update_application(db: Session, application: Application):
    """신청 상태 변경 (수락/거절)"""
    db.commit()
    db.refresh(application)
    return application
