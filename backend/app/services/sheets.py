import json
import time
from typing import Any

import pandas as pd

from app.config import Settings


class SheetConfigurationError(RuntimeError):
    """Raised when the backend cannot determine how to read Google Sheets."""


class SheetDataSource:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._cached_frame: pd.DataFrame | None = None
        self._cache_expires_at = 0.0

    def load(self) -> pd.DataFrame:
        now = time.time()
        if self._cached_frame is not None and now < self._cache_expires_at:
            return self._cached_frame.copy()

        frame = self._read_sheet()
        self._cached_frame = frame
        self._cache_expires_at = now + self.settings.cache_ttl_seconds
        return frame.copy()

    def clear_cache(self) -> None:
        self._cached_frame = None
        self._cache_expires_at = 0.0

    def _read_sheet(self) -> pd.DataFrame:
        if self.settings.google_sheet_csv_url:
            return pd.read_csv(self.settings.google_sheet_csv_url)

        if self.settings.google_sheet_id and self.settings.google_service_account_json:
            try:
                import gspread
            except ImportError as exc:
                raise SheetConfigurationError(
                    "Install gspread to use GOOGLE_SHEET_ID with service account "
                    "credentials, or use GOOGLE_SHEET_CSV_URL."
                ) from exc

            credentials = json.loads(self.settings.google_service_account_json)
            client = gspread.service_account_from_dict(credentials)
            spreadsheet = client.open_by_key(self.settings.google_sheet_id)
            worksheet = spreadsheet.worksheet(self.settings.google_worksheet_name)
            records: list[dict[str, Any]] = worksheet.get_all_records()
            return pd.DataFrame(records)

        raise SheetConfigurationError(
            "Set GOOGLE_SHEET_CSV_URL, or set GOOGLE_SHEET_ID with "
            "GOOGLE_SERVICE_ACCOUNT_JSON."
        )
