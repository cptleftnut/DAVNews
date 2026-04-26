# DAVNews Dashboard Testing

## Overview
The DAVNews dashboard is a React + Vite + Tailwind frontend with a FastAPI backend. The frontend pipeline simulation is entirely client-side (no backend calls needed for the main dashboard flow).

## Local Setup

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Note: `elevenlabs` package version in requirements.txt might not be available. For testing purposes, install the core deps (fastapi, uvicorn, websockets, pydantic, python-dotenv) — the ElevenLabs/OpenAI/Google integrations gracefully degrade without API keys.

### Frontend
```bash
cd frontend
npm install
npm run dev     # Dev server on port 5173
npm run build   # Verify production build
```

## Key Test Flows

### 1. Idle State Verification
- Open `http://localhost:5173`
- Verify header: "DAVNews AI Hedge Network"
- Verify initial metrics: Views=14,500, RPM=$0.120, Revenue=$1.74, AUM=$1,250
- Verify status badges: INGEST=IDLE, AI=WAITING, VIDEO=WAITING, STORAGE=WAITING, HEDGE=WAITING, PUBLISH=IDLE, WS=CONNECTED
- Verify log shows "Waiting for pipeline trigger..."
- Verify Published Feed shows "No assets published yet."

### 2. Pipeline Execution
- Click "Auto-Scout Viral Trend" button
- Button should disable and show "Processing..." with spinner
- Logs appear with timestamps and stage prefixes: CRON JOB, TREND SCOUT, AI SCOUT, INGESTION, AI ENGINE, A/B TESTING, AI PREDICT, SCRIPT ENGINE, TTS ENGINE, VIDEO ENGINE, G-DRIVE, QUALITY GATE, HEDGE ENGINE, DISTRIBUTION, WS BROADCAST
- A/B Hook Test Results panel appears with 3 hooks, winner starred in green
- Active Asset panel shows: Topic, Script, Voice (Dylan Page), Subs (EN/DA/ES/DE/ZH/FR), Status
- Pipeline takes ~20 seconds to complete

### 3. Quality Gate Behavior
- The quality gate randomly rejects ~33% of runs (score 1 out of range 1-3)
- On rejection: error log appears, pipeline aborts, metrics unchanged, no feed entry added
- On success: metrics increment, new feed entry appears at top
- You may need to run the pipeline multiple times to see both pass and reject scenarios

### 4. Metric Accumulation
- After successful runs, Total Views increases by 5,000-55,000 (random)
- Revenue and AUM also increase
- Published Feed stacks entries (newest on top, max 5 visible)

### 5. Backend Health
- `GET http://localhost:8000/health` returns `{"status":"production_ready"}`

## Known Issues
- `elevenlabs==0.3.0` in requirements.txt might not resolve. Install other deps individually if needed.
- The frontend pipeline is a client-side simulation — no real API calls are made to OpenAI/ElevenLabs/Google Drive during dashboard testing.

## Devin Secrets Needed
No secrets needed for basic dashboard testing. For full integration testing:
- `OPENAI_API_KEY` — GPT-4 content generation
- `ELEVENLABS_API_KEY` — TTS voice synthesis
- `GOOGLE_APPLICATION_CREDENTIALS` — Google Drive upload (Service Account JSON path)
