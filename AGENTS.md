# Agent Guide

## Project Purpose

This repo is migrating from a Streamlit running challenge prototype to a mobile-first app with a Next.js frontend and FastAPI backend. Google Sheets remains the manual logging source for now.

## Architecture

- `frontend/`: Next.js app for the public challenge scoreboard.
- `backend/`: FastAPI service that loads Google Sheets data, normalizes it, caches it, and exposes leaderboard APIs.
- `app.py` and `pages/`: existing Streamlit prototype retained as reference during migration.
- `GOALS.md`: product direction, design principles, and feature priorities.

## Development Commands

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Backend:

- `GOOGLE_SHEET_CSV_URL`: preferred simple setup for a published Google Sheet CSV export.
- `GOOGLE_SHEET_ID`: sheet ID for private Sheets access.
- `GOOGLE_WORKSHEET_NAME`: optional worksheet tab name, default `Sheet1`.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: service account JSON string for private Sheets access.
- `CACHE_TTL_SECONDS`: API cache lifetime, default `300`.
- `FRONTEND_ORIGIN`: allowed CORS origin, default `http://localhost:3000`.

Frontend:

- `NEXT_PUBLIC_API_BASE_URL`: FastAPI base URL, default `http://localhost:8000`.

## Coding Guidelines

- Keep Google Sheets as an input source, not a place for frontend-specific logic.
- Keep ranking, summaries, archive filtering, and data validation in the backend.
- Keep the frontend focused on mobile-first presentation and interaction.
- Avoid committing secrets, local virtual environments, `node_modules`, or generated build output.
- Preserve the existing Streamlit app until the new app fully replaces it.

## Product Tone

The app should feel competitive, laid back, encouraging, and fun. Prefer clean cards, team colors, progress visuals, badges, highlights, and friendly copy over dense spreadsheet-like tables.
