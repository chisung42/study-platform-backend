"""
Group / Application Repository (Phase 5)
"""

from supabase import Client
from app.database import to_row, to_rows


# ── study_groups ──

def get_groups(db: Client):
    res = db.table("study_groups").select("*").order("created_at", desc=True).execute()
    return to_rows(res.data)


def get_group_by_id(db: Client, group_id: int):
    res = db.table("study_groups").select("*").eq("id", group_id).execute()
    return to_row(res.data[0]) if res.data else None


def create_group(db: Client, data: dict):
    res = db.table("study_groups").insert(data).execute()
    return to_row(res.data[0]) if res.data else None


def update_group(db: Client, group_id: int, data: dict):
    res = db.table("study_groups").update(data).eq("id", group_id).execute()
    return to_row(res.data[0]) if res.data else None


def delete_group(db: Client, group_id: int):
    db.table("study_groups").delete().eq("id", group_id).execute()


# ── applications ──

def get_application_by_id(db: Client, application_id: int):
    res = db.table("applications").select("*").eq("id", application_id).execute()
    return to_row(res.data[0]) if res.data else None


def get_applications_by_group(db: Client, group_id: int):
    res = db.table("applications").select("*").eq("group_id", group_id).execute()
    return to_rows(res.data)


def get_application_by_user_and_group(db: Client, group_id: int, applicant_id: int):
    res = (
        db.table("applications")
        .select("*")
        .eq("group_id", group_id)
        .eq("applicant_id", applicant_id)
        .execute()
    )
    return to_row(res.data[0]) if res.data else None


def create_application(db: Client, data: dict):
    res = db.table("applications").insert(data).execute()
    return to_row(res.data[0]) if res.data else None


def update_application(db: Client, application_id: int, data: dict):
    res = db.table("applications").update(data).eq("id", application_id).execute()
    return to_row(res.data[0]) if res.data else None
