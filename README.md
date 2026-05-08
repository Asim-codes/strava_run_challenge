# Running Challenge

A mobile-first running challenge scoreboard. The original prototype is Streamlit, and the new app is being migrated to a Next.js frontend with a FastAPI backend while keeping Google Sheets as the manual logging source.

## Structure

- `frontend/`: Next.js scoreboard experience.
- `backend/`: FastAPI API for Google Sheets loading, normalization, caching, current rankings, and archive rankings.
- `app.py` and `pages/`: existing Streamlit prototype kept for reference.
- `AGENTS.md`: project guidance for future AI/coding agents.
- `GOALS.md`: product and design direction.

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Set either:

- `GOOGLE_SHEET_CSV_URL` for a published CSV export, or
- `GOOGLE_SHEET_ID` and `GOOGLE_SERVICE_ACCOUNT_JSON` for private Sheet access.

## Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The frontend expects `NEXT_PUBLIC_API_BASE_URL`, defaulting to `http://localhost:8000`.

## API Endpoints

- `GET /health`
- `GET /api/current`
- `GET /api/current/teams/{team}/contributions`
- `GET /api/archive/periods`
- `GET /api/archive/{period}`
- `POST /api/cache/refresh`

## Deployment (GitHub -> Render + Vercel)

This setup keeps the backend and frontend separate:

- Backend (`FastAPI`) on Render
- Frontend (`Next.js`) on Vercel

### 1) Push to GitHub

```bash
git add .
git commit -m "deployment-ready app setup"
git push
```

### 2) Backend on Render

Create a Render **Web Service** from this repo with:

- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Set environment variables:

- `GOOGLE_SHEET_CSV_URL` = your published sheet CSV URL
- `CURRENT_PERIOD` = `MAY-JUN`
- `CHALLENGE_START_DATE` = `2026-05-08`
- `CHALLENGE_END_DATE` = `2026-06-08`
- `CHALLENGE_TIMEZONE` = `Asia/Hong_Kong`
- `CACHE_TTL_SECONDS` = `300`
- `FRONTEND_ORIGIN` = your Vercel URL (set after frontend deploy)

Verify:

- `https://<render-service>/health`
- `https://<render-service>/api/current`

### 3) Frontend on Vercel

Import this repo into Vercel with:

- Root Directory: `frontend`

Set environment variable:

- `NEXT_PUBLIC_API_BASE_URL` = `https://<render-service>`

Deploy and verify:

- `https://<vercel-project>.vercel.app`

### 4) Final CORS wiring

After Vercel deploy, update Render:

- `FRONTEND_ORIGIN` = `https://<vercel-project>.vercel.app`

Redeploy backend.

### Notes

- Keep `.env` files local (already ignored by git).
- Google Sheet must be accessible to the backend for CSV reads.
- Data updates are cached based on `CACHE_TTL_SECONDS`.
