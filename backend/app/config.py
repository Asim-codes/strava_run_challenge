import os
from dataclasses import dataclass
from datetime import date

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    google_sheet_csv_url: str | None
    google_sheet_id: str | None
    google_worksheet_name: str
    google_service_account_json: str | None
    current_period: str | None
    cache_ttl_seconds: int
    frontend_origin: str
    challenge_start_date: date
    challenge_end_date: date
    challenge_timezone: str


def _optional_env(name: str) -> str | None:
    value = os.getenv(name)
    return value.strip() if value and value.strip() else None


def get_settings() -> Settings:
    return Settings(
        google_sheet_csv_url=_optional_env("GOOGLE_SHEET_CSV_URL"),
        google_sheet_id=_optional_env("GOOGLE_SHEET_ID"),
        google_worksheet_name=os.getenv("GOOGLE_WORKSHEET_NAME", "Sheet1"),
        google_service_account_json=_optional_env("GOOGLE_SERVICE_ACCOUNT_JSON"),
        current_period=_optional_env("CURRENT_PERIOD"),
        cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "300")),
        frontend_origin=os.getenv("FRONTEND_ORIGIN", "http://localhost:3000"),
        challenge_start_date=date.fromisoformat(
            os.getenv("CHALLENGE_START_DATE", "2026-05-08")
        ),
        challenge_end_date=date.fromisoformat(
            os.getenv("CHALLENGE_END_DATE", "2026-06-08")
        ),
        challenge_timezone=os.getenv("CHALLENGE_TIMEZONE", "Asia/Hong_Kong"),
    )
