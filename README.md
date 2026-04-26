# DAVNews AI Media Hedge Network

**Autonomous Media Hedge Fund — Viral Content Engine**

DAVNews is an autonomous media hedge fund that operates as a viral content engine. It scouts viral trends, generates optimised content, renders video programmatically, uploads to Google Drive, and exposes a live React dashboard for monitoring.

## Architecture

```
davnews-monorepo/
├── backend/           # FastAPI + Python services
│   ├── main.py        # API entrypoint
│   ├── core/          # Config & shared state
│   ├── services/      # Scout, AI, TTS, Video, GDrive
│   ├── api/           # WebSocket broadcast
│   └── output/        # Rendered video files
├── frontend/          # React + Vite + Tailwind dashboard
├── infra/             # Docker Compose
└── README.md
```

## Pipeline

1. **Trend Scouting** — Scans Twitter / Reddit / HackerNews for viral velocity signals.
2. **A/B Hook Generation** — Creates and scores multiple hooks for 3-second retention.
3. **Script Generation** — Expands the winning hook into a full English narration (GPT-4 or Ollama).
4. **TTS** — Renders audio via Edge TTS (free) or ElevenLabs voice clone (Dylan Page / "News Daddy").
5. **Video Rendering** — Assembles B-roll, TTS audio, and multi-language subtitles (EN, DA, ES, DE, ZH, FR) using MoviePy/FFmpeg.
6. **Google Drive Upload** — Authenticates via Service Account, locates or creates a "DAVNews" folder, and uploads the `.mp4`.
7. **Hedge Metrics** — Calculates simulated PnL (views, RPM, revenue, AUM).
8. **Dashboard** — Real-time React UI with WebSocket updates.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- FFmpeg & ImageMagick (for video rendering)
- Docker & Docker Compose (optional)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
cd infra
docker compose up --build
```

## Free Alternatives (No API Keys Needed)

DAVNews works fully without paid APIs using these free alternatives:

| Component | Free Alternative | Paid Option |
|---|---|---|
| **LLM** | [Ollama](https://ollama.ai) (local Llama 3, Mistral, etc.) | OpenAI GPT-4 |
| **TTS** | [Edge TTS](https://github.com/rany2/edge-tts) (Microsoft neural voices) | ElevenLabs |

### Quick setup with Ollama

```bash
# Install Ollama (one-liner)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3

# DAVNews will auto-detect it at http://localhost:11434
```

Edge TTS is included in `requirements.txt` — it works immediately with no setup.

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `LLM_PROVIDER` | `auto` (default), `openai`, or `ollama` | No |
| `TTS_PROVIDER` | `auto` (default), `elevenlabs`, or `edge-tts` | No |
| `OLLAMA_BASE_URL` | Ollama server URL (default: `http://localhost:11434`) | No |
| `OLLAMA_MODEL` | Ollama model name (default: `llama3`) | No |
| `EDGE_TTS_VOICE` | Edge TTS voice (default: `en-US-GuyNeural`) | No |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 content generation | No |
| `ELEVENLABS_API_KEY` | ElevenLabs API key for TTS | No |
| `ELEVENLABS_VOICE_ID` | Voice clone ID (default: "default") | No |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to Google Service Account JSON | No |

> **Note:** With `auto` provider mode (default), the system tries paid APIs first, then free alternatives, then template fallbacks. Set `LLM_PROVIDER=ollama` or `TTS_PROVIDER=edge-tts` to force free-only mode.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/trigger-cycle` | Trigger autonomous content pipeline |
| `WS` | `/ws/live` | WebSocket for real-time dashboard updates |

## Google Drive Integration

1. Create a Google Cloud project and enable the Drive API.
2. Create a Service Account and download the credentials JSON.
3. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON file.
4. The uploader will automatically create a "DAVNews" folder and upload rendered videos.

## License

MIT
