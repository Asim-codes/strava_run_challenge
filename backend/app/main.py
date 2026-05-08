from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models.schemas import (
    ArchivePeriod,
    ArchivePeriodResponse,
    CurrentChallengeResponse,
    TeamContribution,
)
from app.services.leaderboard import (
    build_archive_response,
    build_current_response,
    build_team_contributions,
    list_archive_periods,
)
from app.services.sheets import SheetConfigurationError, SheetDataSource


settings = get_settings()
sheet_source = SheetDataSource(settings)

app = FastAPI(
    title="Running Challenge API",
    description="Leaderboard API backed by manually logged Google Sheets data.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _load_sheet():
    try:
        return sheet_source.load()
    except SheetConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Failed to load Google Sheets data: {exc}"
        ) from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/current", response_model=CurrentChallengeResponse)
def current_challenge() -> CurrentChallengeResponse:
    return build_current_response(
        _load_sheet(),
        settings.challenge_start_date,
        settings.challenge_end_date,
        settings.challenge_timezone,
        settings.current_period,
    )


@app.get(
    "/api/current/teams/{team}/contributions",
    response_model=list[TeamContribution],
)
def current_team_contributions(team: str) -> list[TeamContribution]:
    return build_team_contributions(
        _load_sheet(),
        team,
        settings.challenge_start_date,
        settings.challenge_end_date,
        settings.current_period,
    )


@app.get("/api/archive/periods", response_model=list[ArchivePeriod])
def archive_periods() -> list[ArchivePeriod]:
    return list_archive_periods(_load_sheet(), settings.current_period)


@app.get("/api/archive/{period}", response_model=ArchivePeriodResponse)
def archive_period(period: str) -> ArchivePeriodResponse:
    response = build_archive_response(
        _load_sheet(),
        period,
        settings.challenge_end_date,
        settings.challenge_timezone,
        settings.current_period,
    )
    if response.summary.total_runs == 0:
        raise HTTPException(status_code=404, detail="Archive period not found.")
    return response


@app.post("/api/cache/refresh")
def refresh_cache() -> dict[str, str]:
    sheet_source.clear_cache()
    return {"status": "refreshed"}
