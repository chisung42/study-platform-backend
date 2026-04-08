"""
database.py — Supabase Python 클라이언트 설정

SQLAlchemy 대신 supabase-py를 사용한다.
supabase-py는 Supabase의 REST API(PostgREST)를 통해 DB를 조작한다.

연결에 필요한 것:
  SUPABASE_URL  — Supabase 프로젝트 URL
  SUPABASE_ANON_KEY — anon(공개) API 키
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# 앱 전체에서 공유하는 싱글턴 클라이언트
_client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_db() -> Client:
    """
    FastAPI Depends()에서 사용하는 DB 클라이언트 반환 함수.

    SQLAlchemy와 달리 supabase-py 클라이언트는 연결을 자동으로 관리하므로
    별도의 open/close 처리가 필요 없다.
    """
    return _client


class Row(dict):
    """
    Supabase 응답(dict)을 객체처럼 접근 가능하게 해주는 래퍼.

    row['id'] 와 row.id 두 방식 모두 동작한다.
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"Row has no attribute '{key}'")

    def __setattr__(self, key, val):
        self[key] = val

    def __delattr__(self, key):
        del self[key]


def to_row(data: dict | None) -> Row | None:
    return Row(data) if data else None


def to_rows(data_list: list | None) -> list[Row]:
    return [Row(d) for d in (data_list or [])]
