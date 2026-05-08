# Product Goals

## Vision

Build a running challenge app that turns manually logged activities into a live, mobile-friendly scoreboard. The experience should increase competitive spirit while staying laid back, encouraging, and fun.

## Current Migration Goal

Move from Streamlit to:

- FastAPI for data loading, validation, caching, and leaderboard APIs.
- Next.js for a modern, minimal, mobile-first user experience.
- Google Sheets for manual logging until a better logging workflow is needed.

## Experience Principles

- Mobile-first: ranking screens should feel natural on a phone.
- Competitive without being harsh: celebrate close races, effort, streaks, and team contribution.
- Minimal and modern: use clear cards, strong spacing, readable type, and restrained visuals.
- Fun and alive: include race progress, badges, weekly highlights, team colors, and friendly microcopy.
- Stable under growth: avoid recomputing everything in the UI and avoid fragile spreadsheet assumptions.

## Initial Features

- Current challenge overview with days left, total distance, total runs, active runners, and average distance.
- Team leaderboard with medals, team colors, compact progress bars, and member counts.
- Individual leaderboard with ranks, teams, totals, streak indicators, and badges.
- Team contribution detail view.
- Weekly highlights such as biggest week, most active runner, close battle, and latest logged effort.
- Archive periods with team and individual results.

## Non-Goals For Now

- Replacing Google Sheets manual logging.
- Full Strava API ingestion.
- User accounts for every runner.
- Payment, invites, or complex admin workflows.
- Removing the Streamlit prototype before the new app has feature parity.

## Future Ideas

- Custom log-a-run form backed by Supabase or Postgres.
- Strava link validation where useful, without depending on the API.
- Team avatars, seasonal themes, and challenge recap cards.
- Admin dashboard for periods, runners, teams, and duplicate review.
