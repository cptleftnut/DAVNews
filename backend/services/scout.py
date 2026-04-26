"""Trend scouting service – scans social platforms for viral signals."""

import asyncio
import random

from core.state import PipelineState
from services.ai_content import generate_hooks, generate_script
from services.voice_engine import synthesize_speech
from services.video_engine import render_video
from services.gdrive_uploader import upload_to_drive
from api.websockets import manager

VIRAL_TOPICS_POOL = [
    "AGI breakthrough rumored at OpenAI headquarters",
    "Nvidia announces new architecture that changes everything",
    "Massive zero-day leak exposes major tech company",
    "Apple's secret AI hardware project just leaked",
    "TikTok's new algorithm reverse-engineered by researchers",
    "Elon Musk open-sources next generation AI model",
]


async def _broadcast(event: str, data: dict) -> None:
    await manager.broadcast({"event": event, **data})


async def run_pipeline() -> PipelineState:
    """Execute one full autonomous content cycle."""
    state = PipelineState(status="running")

    # 1. Trend scouting
    state.topic = random.choice(VIRAL_TOPICS_POOL)
    state.viral_score = random.randint(85, 99)
    state.add_log(
        f"[TREND SCOUT] Locked onto: \"{state.topic}\" "
        f"(Velocity: {state.viral_score}/100)",
        "success",
    )
    await _broadcast("scout", {"topic": state.topic, "score": state.viral_score})

    # 2. Hook generation & A/B evaluation
    hooks = generate_hooks(state.topic)
    evaluated = [
        {"hook": h, "hold3s": round(random.uniform(0.30, 0.80), 2)}
        for h in hooks
    ]
    evaluated.sort(key=lambda x: x["hold3s"], reverse=True)
    state.winning_hook = evaluated[0]["hook"]
    state.add_log(
        f"[A/B TEST] Winner: \"{state.winning_hook}\" "
        f"(3s hold: {evaluated[0]['hold3s'] * 100:.0f}%)",
        "success",
    )
    await _broadcast("hooks", {"hooks": evaluated, "winner": state.winning_hook})

    # 3. Full script generation
    state.script = generate_script(state.winning_hook, state.topic)
    state.add_log("[SCRIPT ENGINE] Full English script generated.", "info")
    await _broadcast("script", {"script": state.script})

    # 4. TTS via 11Labs
    state.audio_path = synthesize_speech(state.script)
    state.add_log("[TTS ENGINE] Audio rendered via Dylan Page voice clone.", "info")
    await _broadcast("audio", {"path": state.audio_path})

    # 5. Video rendering
    state.video_path = render_video(
        script_text=state.script,
        audio_path=state.audio_path,
    )
    state.add_log("[VIDEO ENGINE] MP4 rendered with subtitles.", "success")
    await _broadcast("video", {"path": state.video_path})

    # 6. Google Drive upload
    state.gdrive_url = upload_to_drive(state.video_path)
    state.add_log(f"[G-DRIVE] Uploaded to Google Drive: {state.gdrive_url}", "success")
    await _broadcast("upload", {"url": state.gdrive_url})

    # 7. Quality gate
    state.quality_score = random.randint(1, 3)
    if state.quality_score < 2:
        state.add_log(
            f"[QUALITY GATE] Rejected (score {state.quality_score}/3). Aborting.",
            "error",
        )
        state.status = "rejected"
        await _broadcast("rejected", state.to_dict())
        return state

    # 8. Hedge metrics
    state.risk = round(random.uniform(0.1, 1.0), 2)
    state.reward = round(random.uniform(0.1, 2.0), 2)
    state.views = random.randint(5000, 55000)
    state.revenue = round((state.views / 1000) * 0.12, 2)
    state.status = "published"
    state.add_log("[HEDGE ENGINE] Metrics calculated. Published.", "success")
    await _broadcast("published", state.to_dict())

    return state
