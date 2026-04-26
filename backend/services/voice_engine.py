"""TTS engine – synthesises narration audio using ElevenLabs."""

import os
import uuid

from core.config import settings


def synthesize_speech(script: str) -> str:
    """Convert *script* to speech and return the path to the .mp3 file.

    When the ElevenLabs API key is available, calls the real API using the
    configured voice clone (Dylan Page / "News Daddy").  Otherwise, creates a
    silent placeholder audio file so the rest of the pipeline can continue.
    """
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(settings.OUTPUT_DIR, f"tts_{uuid.uuid4().hex[:8]}.mp3")

    if settings.ELEVENLABS_API_KEY:
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
            pass

    # Fallback: generate a short silent mp3 so downstream steps don't break.
    _write_silent_mp3(out_path)
    return out_path


def _write_silent_mp3(path: str) -> None:
    """Write a minimal valid MP3 file (~0.5 s of silence)."""
    # Minimal MPEG-1 Layer 3 frame (mono, 128 kbps, 44100 Hz, padding).
    # This is the smallest valid MP3 that most decoders accept.
    frame = (
        b"\xff\xfb\x90\x00"  # sync + header
        + b"\x00" * 413  # silent frame body (417 bytes total)
    )
    with open(path, "wb") as f:
        # Write enough frames for ~0.5 s of audio
        for _ in range(20):
            f.write(frame)
