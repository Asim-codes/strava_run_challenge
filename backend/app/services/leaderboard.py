import re
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pandas as pd

from app.models.schemas import (
    ArchivePeriod,
    ArchivePeriodResponse,
    CurrentChallengeResponse,
    Highlight,
    IndividualStanding,
    Summary,
    TeamContribution,
    TeamStanding,
)


ARCHIVED_VALUES = {"TRUE", "T", "1", "YES", "Y"}
TEAM_COLORS = [
    "#f97316",
    "#22c55e",
    "#3b82f6",
    "#a855f7",
    "#ec4899",
    "#14b8a6",
    "#eab308",
    "#ef4444",
]
MEDALS = ["🥇", "🥈", "🥉"]


def normalize_frame(raw: pd.DataFrame) -> pd.DataFrame:
    frame = raw.copy()
    frame.columns = [str(column).strip() for column in frame.columns]

    for column in ["Runner", "Team", "Distance", "Date", "Archive", "Period"]:
        if column not in frame.columns:
            frame[column] = None

    frame["Runner"] = frame["Runner"].astype(str).str.strip()
    frame["Team"] = frame["Team"].astype(str).str.strip()
    frame["Distance"] = pd.to_numeric(frame["Distance"], errors="coerce")
    frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce")
    frame["Archive"] = (
        frame["Archive"].astype(str).str.upper().str.strip().isin(ARCHIVED_VALUES)
    )
    frame["Period"] = frame["Period"].fillna("").astype(str).str.strip()

    return frame[
        (frame["Runner"] != "")
        & (frame["Runner"].str.lower() != "nan")
        & (frame["Team"] != "")
        & (frame["Team"].str.lower() != "nan")
        & frame["Distance"].notna()
        & (frame["Distance"] > 0)
    ].copy()


def build_current_response(
    raw: pd.DataFrame,
    challenge_start_date: date,
    challenge_end_date: date,
    challenge_timezone: str,
    current_period: str | None = None,
) -> CurrentChallengeResponse:
    frame = normalize_frame(raw)
    current = _current_frame(
        frame, current_period, challenge_start_date, challenge_end_date
    )
    return _build_response(current, challenge_end_date, challenge_timezone)


def list_archive_periods(
    raw: pd.DataFrame, current_period: str | None = None
) -> list[ArchivePeriod]:
    frame = normalize_frame(raw)
    archived = _archive_frame(frame, current_period)
    periods: list[ArchivePeriod] = []

    for period, period_frame in archived.groupby("Period", sort=False):
        label = _period_label(str(period), period_frame)
        periods.append(
            ArchivePeriod(
                period=period,
                label=label,
                total_distance=round(float(period_frame["Distance"].sum()), 1),
                total_runs=int(len(period_frame)),
                active_runners=int(period_frame["Runner"].nunique()),
                active_teams=int(period_frame["Team"].nunique()),
            )
        )

    return sorted(periods, key=lambda item: item.period, reverse=True)


def build_archive_response(
    raw: pd.DataFrame,
    period: str,
    challenge_end_date: date,
    challenge_timezone: str,
    current_period: str | None = None,
) -> ArchivePeriodResponse:
    frame = normalize_frame(raw)
    archived = _archive_frame(frame, current_period)
    archived = archived[archived["Period"] == period].copy()
    response = _build_response(archived, challenge_end_date, challenge_timezone)
    return ArchivePeriodResponse(
        period=period,
        summary=response.summary,
        teams=response.teams,
        individuals=response.individuals,
        highlights=response.highlights,
    )


def build_team_contributions(
    raw: pd.DataFrame,
    team: str,
    challenge_start_date: date,
    challenge_end_date: date,
    current_period: str | None = None,
) -> list[TeamContribution]:
    frame = normalize_frame(raw)
    team_frame = _current_frame(
        frame, current_period, challenge_start_date, challenge_end_date
    )
    team_frame = team_frame[team_frame["Team"] == team].copy()
    return _team_contributions(team_frame).get(team, [])


def _current_frame(
    frame: pd.DataFrame,
    current_period: str | None,
    challenge_start_date: date,
    challenge_end_date: date,
) -> pd.DataFrame:
    current = frame[~frame["Archive"]].copy()
    if current_period:
        current = current[current["Period"] == current_period].copy()
    current = current[
        current["Date"].notna()
        & (current["Date"].dt.date >= challenge_start_date)
        & (current["Date"].dt.date <= challenge_end_date)
    ].copy()
    return current


def _archive_frame(frame: pd.DataFrame, current_period: str | None) -> pd.DataFrame:
    has_period = frame["Period"] != ""
    if current_period:
        is_archived_period = frame["Archive"] | (frame["Period"] != current_period)
        return frame[has_period & is_archived_period].copy()
    return frame[frame["Archive"] & has_period].copy()


def _build_response(
    frame: pd.DataFrame, challenge_end_date: date, challenge_timezone: str
) -> CurrentChallengeResponse:
    timezone = _safe_timezone(challenge_timezone)
    today_hkt = datetime.now(timezone).date()
    frame_hkt = _with_hkt_dates(frame, timezone)
    teams = _team_standings(frame, frame_hkt, today_hkt)
    individuals = _individual_standings(frame_hkt, today_hkt)
    return CurrentChallengeResponse(
        summary=_summary(frame, challenge_end_date, challenge_timezone),
        teams=teams,
        individuals=individuals,
        contributions=_team_contributions(frame_hkt),
        highlights=_highlights(teams),
    )


def _summary(
    frame: pd.DataFrame, challenge_end_date: date, challenge_timezone: str
) -> Summary:
    total_distance = float(frame["Distance"].sum()) if not frame.empty else 0.0
    total_runs = int(len(frame))
    try:
        today = datetime.now(ZoneInfo(challenge_timezone)).date()
    except ZoneInfoNotFoundError:
        today = date.today()
    return Summary(
        total_distance=round(total_distance, 1),
        total_runs=total_runs,
        average_distance=round(total_distance / total_runs, 1) if total_runs else 0.0,
        active_runners=int(frame["Runner"].nunique()) if not frame.empty else 0,
        active_teams=int(frame["Team"].nunique()) if not frame.empty else 0,
        days_left=max((challenge_end_date - today).days, 0),
    )


def _team_standings(
    frame: pd.DataFrame, frame_hkt: pd.DataFrame, today_hkt: date
) -> list[TeamStanding]:
    if frame.empty:
        return []

    members = (
        frame.groupby("Team")["Runner"]
        .apply(lambda rows: sorted(set(rows)))
        .to_dict()
    )
    all_teams = sorted({str(t) for t in frame["Team"].unique()})

    period_by_team: dict[str, float] = {}
    if not frame_hkt.empty:
        period_by_team = (
            frame_hkt.groupby("Team")["Distance"].sum().astype(float).to_dict()
        )

    rows = [{"Team": t, "Distance": float(period_by_team.get(t, 0.0))} for t in all_teams]
    totals = (
        pd.DataFrame(rows)
        .sort_values("Distance", ascending=False)
        .reset_index(drop=True)
    )
    leader_distance = float(totals.iloc[0]["Distance"]) if not totals.empty else 0.0
    top_distance = leader_distance or 1.0

    standings: list[TeamStanding] = []
    for index, row in totals.iterrows():
        team = str(row["Team"])
        distance = round(float(row["Distance"]), 1)
        this_distance = float(row["Distance"])
        distance_to_leader = round(leader_distance - this_distance, 1)
        if index == 0:
            distance_to_team_above: float | None = None
        else:
            prev = float(totals.iloc[index - 1]["Distance"])
            distance_to_team_above = round(prev - this_distance, 1)
        standings.append(
            TeamStanding(
                rank=index + 1,
                medal=MEDALS[index] if index < len(MEDALS) else None,
                team=team,
                distance=distance,
                member_count=len(members.get(team, [])),
                runners=members.get(team, []),
                color=TEAM_COLORS[index % len(TEAM_COLORS)],
                progress=round((this_distance / top_distance) * 100, 1),
                distance_to_leader=distance_to_leader,
                distance_to_team_above=distance_to_team_above,
            )
        )
    return standings


def _stealable_crown_holders(frame: pd.DataFrame) -> dict[str, set[str]]:
    """Runners tied for the most qualifying runs in each pocket (period frame)."""
    empty = {"67 King": set(), "Tenner Tyrant": set(), "Long Haul Crown": set()}
    if frame.empty:
        return empty

    def leaders(mask: pd.Series) -> set[str]:
        sub = frame.loc[mask, "Runner"]
        if sub.empty:
            return set()
        counts = sub.astype(str).value_counts()
        top = int(counts.max())
        if top < 1:
            return set()
        return {str(r) for r in counts[counts == top].index}

    return {
        "67 King": leaders((frame["Distance"] >= 6.65) & (frame["Distance"] <= 6.75)),
        "Tenner Tyrant": leaders((frame["Distance"] >= 9.5) & (frame["Distance"] <= 10.5)),
        "Long Haul Crown": leaders(frame["Distance"] >= 15.0),
    }


def _individual_standings(frame: pd.DataFrame, today_hkt: date) -> list[IndividualStanding]:
    if frame.empty:
        return []

    totals = (
        frame.groupby(["Runner", "Team"], as_index=False)
        .agg(Distance=("Distance", "sum"), Runs=("Distance", "count"))
        .sort_values("Distance", ascending=False)
        .reset_index(drop=True)
    )
    top_distance = float(totals["Distance"].max()) or 1.0
    runner_metrics = _runner_badge_metrics(frame, today_hkt)
    crown_holders = _stealable_crown_holders(frame)

    standings: list[IndividualStanding] = []
    for index, row in totals.iterrows():
        runner = str(row["Runner"])
        distance = round(float(row["Distance"]), 1)
        metrics = runner_metrics.get(runner, {})
        streak_weeks = int(metrics.get("consecutive_active_weeks", 0))
        badges = _badges(index + 1, metrics, runner, crown_holders)
        standings.append(
            IndividualStanding(
                rank=index + 1,
                medal=MEDALS[index] if index < len(MEDALS) else None,
                runner=runner,
                team=str(row["Team"]),
                distance=distance,
                runs=int(row["Runs"]),
                streak_weeks=streak_weeks,
                badges=badges,
                progress=round((distance / top_distance) * 100, 1),
            )
        )
    return standings


def _team_contributions(frame: pd.DataFrame) -> dict[str, list[TeamContribution]]:
    if frame.empty:
        return {}

    contributions: dict[str, list[TeamContribution]] = {}
    grouped = (
        frame.groupby(["Team", "Runner"], as_index=False)
        .agg(Distance=("Distance", "sum"), Runs=("Distance", "count"))
        .sort_values(["Team", "Distance"], ascending=[True, False])
    )

    for team, team_frame in grouped.groupby("Team", sort=False):
        top_distance = float(team_frame["Distance"].max()) or 1.0
        contributions[str(team)] = [
            TeamContribution(
                runner=str(row["Runner"]),
                distance=round(float(row["Distance"]), 1),
                runs=int(row["Runs"]),
                progress=round((float(row["Distance"]) / top_distance) * 100, 1),
            )
            for _, row in team_frame.iterrows()
        ]

    return contributions


def _safe_timezone(challenge_timezone: str) -> ZoneInfo:
    try:
        return ZoneInfo(challenge_timezone)
    except ZoneInfoNotFoundError:
        return ZoneInfo("Asia/Hong_Kong")


def _with_hkt_dates(frame: pd.DataFrame, timezone: ZoneInfo) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()
    with_dates = frame.copy()
    if "Date" in with_dates.columns:
        date_series = pd.to_datetime(with_dates["Date"], errors="coerce")
        with_dates["DateHKT"] = (
            date_series.dt.tz_localize(timezone, nonexistent="shift_forward", ambiguous="NaT")
            if getattr(date_series.dt, "tz", None) is None
            else date_series.dt.tz_convert(timezone)
        )
        with_dates["DateOnlyHKT"] = with_dates["DateHKT"].dt.date
    else:
        with_dates["DateOnlyHKT"] = None
    return with_dates


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def _month_end(d: date) -> date:
    next_month = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
    return next_month - timedelta(days=1)


def _month_start(d: date) -> date:
    return d.replace(day=1)


_PALINDROME_TARGETS = [5.05, 6.06, 7.07, 8.08, 9.09]


def _runner_badge_metrics(frame: pd.DataFrame, today_hkt: date) -> dict[str, dict[str, float | int | bool]]:
    if frame.empty:
        return {}

    metrics: dict[str, dict[str, float | int | bool]] = {}
    current_week_start = _week_start(today_hkt)
    # Last fully completed week (ended before this week started)
    last_week_start = current_week_start - timedelta(days=7)

    for runner, runner_frame in frame.groupby("Runner", sort=False):
        dated = runner_frame[runner_frame["DateOnlyHKT"].notna()].copy()
        if dated.empty:
            metrics[str(runner)] = {
                "total_distance_period": 0.0,
                "total_runs_period": 0,
                "single_run_max": 0.0,
                "has_double_digits": False,
                "consecutive_active_weeks": 0,
                "consistency_club": False,
                "hat_trick": False,
                "high_volume_machine": False,
                "century_club": False,
                "double_century": False,
                "ultra_engine": False,
                "perfect_month": False,
                "palindrome": False,
                "balanced_diet": False,
            }
            continue

        dates = pd.to_datetime(dated["DateOnlyHKT"])
        dated["WeekStart"] = dates.dt.date.apply(_week_start)
        dated["MonthStart"] = dates.dt.date.apply(_month_start)

        # Consecutive active weeks streaking back from current week
        week_any_counts = dated.groupby("WeekStart")["Distance"].count().to_dict()
        consecutive_weeks = 0
        check_week = current_week_start
        while week_any_counts.get(check_week, 0) >= 1:
            consecutive_weeks += 1
            check_week = check_week - timedelta(days=7)

        # Consistency Club: ≥2 qualifying runs (≥5 km) in the last completed week
        last_week_qualifying = int(
            ((dated["DateOnlyHKT"] >= last_week_start)
             & (dated["DateOnlyHKT"] < current_week_start)
             & (dated["Distance"] >= 5.0)).sum()
        )
        consistency_club = last_week_qualifying >= 2

        # Hat Trick: any single week within the period has ≥3 qualifying runs (≥5 km)
        qualifying_runs = dated[dated["Distance"] >= 5.0].copy()
        if not qualifying_runs.empty:
            weekly_qualifying = qualifying_runs.groupby("WeekStart")["Distance"].count()
            hat_trick = bool((weekly_qualifying >= 3).any())
        else:
            hat_trick = False

        # Period-level distance totals
        total_distance_period = round(float(dated["Distance"].sum()), 2)

        # Perfect Month (calendar-month scoped, needs completed months)
        month_runs_by_start = dated.groupby("MonthStart")["Distance"].count()
        current_month_start = _month_start(today_hkt)
        perfect_month = False
        for month_start, month_total_runs in month_runs_by_start.items():
            month_end_date = _month_end(month_start)
            month_completed = month_end_date < today_hkt or (
                month_end_date == today_hkt and month_start == current_month_start
            )
            if not month_completed or month_total_runs < 4:
                continue
            month_rows = dated[dated["MonthStart"] == month_start]
            active_weeks = month_rows.groupby("WeekStart")["Distance"].count()
            if (active_weeks >= 1).sum() >= 4:
                perfect_month = True
                break

        # Palindrome: any run within 0.05 km of 5.05, 6.06, 7.07, 8.08, 9.09
        palindrome = bool(any(
            ((dated["Distance"] >= t - 0.05) & (dated["Distance"] <= t + 0.05)).any()
            for t in _PALINDROME_TARGETS
        ))

        # Balanced Diet: ≥1 run in [5,10), ≥1 run in [10,15), ≥1 run ≥15
        balanced_diet = bool(
            ((dated["Distance"] >= 5.0) & (dated["Distance"] < 10.0)).any()
            and ((dated["Distance"] >= 10.0) & (dated["Distance"] < 15.0)).any()
            and (dated["Distance"] >= 15.0).any()
        )

        metrics[str(runner)] = {
            "total_distance_period": total_distance_period,
            "total_runs_period": int(len(dated)),
            "single_run_max": float(dated["Distance"].max()),
            "has_double_digits": bool((dated["Distance"] >= 10.0).any()),
            "consecutive_active_weeks": consecutive_weeks,
            "consistency_club": consistency_club,
            "hat_trick": hat_trick,
            "high_volume_machine": bool(int((dated["Distance"] >= 5.0).sum()) >= 15),
            "century_club": total_distance_period >= 100,
            "double_century": total_distance_period >= 200,
            "ultra_engine": total_distance_period >= 300,
            "perfect_month": perfect_month,
            "palindrome": palindrome,
            "balanced_diet": balanced_diet,
        }

    return metrics


def _badges(
    rank: int,
    metrics: dict[str, float | int | bool],
    runner: str,
    crown_holders: dict[str, set[str]],
) -> list[str]:
    badges: list[str] = []
    dist = float(metrics.get("total_distance_period", 0.0))

    # Crowns
    if runner in crown_holders.get("67 King", set()):
        badges.append("67 King")
    if runner in crown_holders.get("Tenner Tyrant", set()):
        badges.append("Tenner Tyrant")
    if runner in crown_holders.get("Long Haul Crown", set()):
        badges.append("Long Haul Crown")

    # Distance milestones (period-based, highest first so they're shown before lower tiers)
    if dist >= 300:
        badges.append("Ultra Engine")
    elif dist >= 200:
        badges.append("Double Century")
    elif dist >= 100:
        badges.append("Century Club")
    if dist >= 75:
        badges.append("Mileage Monster")

    # Volume
    if bool(metrics.get("high_volume_machine", False)):
        badges.append("High Volume Machine")
    if bool(metrics.get("has_double_digits", False)):
        badges.append("Double Digits")

    # Consistency
    if bool(metrics.get("consistency_club", False)):
        badges.append("Consistency Club")
    if bool(metrics.get("hat_trick", False)):
        badges.append("Hat Trick")
    if int(metrics.get("consecutive_active_weeks", 0)) >= 2:
        badges.append("Streak Chef")

    # Patterns
    if bool(metrics.get("palindrome", False)):
        badges.append("Palindrome")
    if bool(metrics.get("balanced_diet", False)):
        badges.append("Balanced Diet")
    if bool(metrics.get("perfect_month", False)):
        badges.append("Perfect Month")

    # Prestige
    if rank <= 3:
        badges.append("Podium Menace")

    return badges


def _period_label(period: str, period_frame: pd.DataFrame) -> str:
    if re.search(r"\b\d{4}\b", period):
        return period
    years = sorted(
        int(y)
        for y in period_frame["Date"].dt.year.dropna().unique().tolist()
    )
    if not years:
        return period
    year_str = f"{years[0]}–{years[-1]}" if len(years) > 1 else str(years[0])
    return f"{period} {year_str}"


def _highlights(teams: list[TeamStanding]) -> list[Highlight]:
    highlights: list[Highlight] = []

    if len(teams) >= 2:
        gap = round(teams[0].distance - teams[1].distance, 1)
        highlights.append(
            Highlight(
                label="Closest chase",
                value=f"{gap} km",
                detail=f"{teams[1].team} is chasing {teams[0].team}.",
            )
        )

    return highlights
