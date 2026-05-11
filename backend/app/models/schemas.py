from pydantic import BaseModel


class Summary(BaseModel):
    total_distance: float
    total_runs: int
    average_distance: float
    active_runners: int
    active_teams: int
    days_left: int


class TeamStanding(BaseModel):
    rank: int
    medal: str | None
    team: str
    distance: float
    member_count: int
    runners: list[str]
    color: str
    progress: float
    distance_to_leader: float
    distance_to_team_above: float | None = None


class IndividualStanding(BaseModel):
    rank: int
    medal: str | None
    runner: str
    team: str
    distance: float
    runs: int
    streak_weeks: int
    badges: list[str]
    progress: float


class TeamContribution(BaseModel):
    runner: str
    distance: float
    runs: int
    progress: float


class Highlight(BaseModel):
    label: str
    value: str
    detail: str


class CurrentChallengeResponse(BaseModel):
    summary: Summary
    teams: list[TeamStanding]
    individuals: list[IndividualStanding]
    contributions: dict[str, list[TeamContribution]]
    highlights: list[Highlight]


class ArchivePeriod(BaseModel):
    period: str
    total_distance: float
    total_runs: int
    active_runners: int
    active_teams: int


class ArchivePeriodResponse(BaseModel):
    period: str
    summary: Summary
    teams: list[TeamStanding]
    individuals: list[IndividualStanding]
    highlights: list[Highlight]
