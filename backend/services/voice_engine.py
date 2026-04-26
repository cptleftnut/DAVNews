"""TTS engine – synthesises narration audio.

Provider priority (configurable via TTS_PROVIDER env var):
  1. ElevenLabs  – paid, highest quality voice cloning
  2. Edge TTS    – FREE, Microsoft neural voices, no API key needed
  3. Silent fallback
"""

import asyncio
import os
import uuid

from core.config import settings


def synthesize_speech(script: str) -> str:
    """Convert *script* to speech and return the path to the audio file.

    Tries providers in priority order:
      - ElevenLabs (if ELEVENLABS_API_KEY is set)
      - Edge TTS (free, no key needed)
      - Silent placeholder as last resort
    """
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(settings.OUTPUT_DIR, f"tts_{uuid.uuid4().hex[:8]}.mp3")

    provider = settings.TTS_PROVIDER.lower()

    # --- ElevenLabs (paid) ------------------------------------------------
    if provider in ("auto", "elevenlabs") and settings.ELEVENLABS_API_KEY:
        result = _try_elevenlabs(script, out_path)
        if result:
            return result

    # --- Edge TTS (free) --------------------------------------------------
    if provider in ("auto", "edge-tts"):
        result = _try_edge_tts(script, out_path)
        if result:
            return result

    # --- Silent fallback --------------------------------------------------
    _write_silent_mp3(out_path)
    return out_path


def _try_elevenlabs(script: str, out_path: str) -> str | None:
    """Attempt synthesis via ElevenLabs API."""
    try:
        from elevenlabs import generate, save, set_api_key

        set_api_key(settings.ELEVENLABS_API_KEY)
        audio = generate(
            text=script,
            voice=settings.ELEVENLABS_VOICE_ID,
            model="eleven_monolingual_v1",
        )
        save(audio, out_path)
        return out_path
    except Exception:
        return None


def _try_edge_tts(script: str, out_path: str) -> str | None:
    """Attempt synthesis via Microsoft Edge TTS (free, no API key)."""
    try:
        import edge_tts

        voice = settings.EDGE_TTS_VOICE

        async def _generate():
            communicate = edge_tts.Communicate(script, voice)
            await communicate.save(out_path)

        # Run the async Edge TTS call
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Already inside an event loop (e.g. FastAPI) — run in a new thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pool.submit(lambda: asyncio.run(_generate())).result(timeout=60)
        else:
            asyncio.run(_generate())

        if os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
            return out_path
        return None
    except Exception:
        return None


def _write_silent_mp3(path: str) -> None:
    """Write a minimal valid MP3 file (~0.5 s of silence)."""
    frame = (
        b"\xff\xfb\x90\x00"  # sync + header
        + b"\x00" * 413  # silent frame body (417 bytes total)
    )
    with open(path, "wb") as f:
        for _ in range(20):
            f.write(frame)
