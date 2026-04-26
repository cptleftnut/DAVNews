"""Video engine – assembles B-roll, TTS audio and multi-language subtitles
into a final MP4 using MoviePy / FFmpeg.
"""

import os
import uuid
import textwrap

from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips,
)

from core.config import settings

# Subtitle translations (simplified – a production system would call a
# translation API).  Keys match settings.SUBTITLE_LANGUAGES.
_TRANSLATIONS = {
    "EN": None,  # original
    "DA": "Seneste nyheder inden for tech",
    "ES": "Últimas noticias de tecnología",
    "DE": "Neueste Tech-Nachrichten",
    "ZH": "最新科技新闻",
    "FR": "Dernières nouvelles technologiques",
}


def render_video(
    script_text: str,
    audio_path: str,
    broll_path: str | None = None,
) -> str:
    """Render the final .mp4 video.

    Parameters
    ----------
    script_text:
        Full narration script (used for subtitle overlay).
    audio_path:
        Path to TTS audio file (.mp3 / .wav).
    broll_path:
        Optional path to a background B-roll video.  When *None* a dark
        gradient background is generated automatically.

    Returns
    -------
    str – absolute path to the rendered .mp4 file.
    """
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(settings.OUTPUT_DIR, f"davnews_{uuid.uuid4().hex[:8]}.mp4")

    width = settings.VIDEO_WIDTH
    height = settings.VIDEO_HEIGHT
    fps = settings.VIDEO_FPS

    # --- Audio -----------------------------------------------------------
    try:
        audio_clip = AudioFileClip(audio_path)
        duration = max(audio_clip.duration, 3.0)
    except Exception:
        audio_clip = None
        duration = 10.0  # fallback duration

    # --- Background ------------------------------------------------------
    if broll_path and os.path.isfile(broll_path):
        from moviepy.editor import VideoFileClip

        bg = VideoFileClip(broll_path).resize((width, height)).loop(duration=duration)
    else:
        bg = ColorClip(size=(width, height), color=(10, 15, 30)).set_duration(duration)

    # --- Subtitle overlays -----------------------------------------------
    subtitle_clips = _build_subtitle_clips(script_text, width, height, duration)

    # --- Compose ---------------------------------------------------------
    layers = [bg] + subtitle_clips
    final = CompositeVideoClip(layers, size=(width, height)).set_duration(duration)

    if audio_clip is not None:
        final = final.set_audio(audio_clip.subclip(0, min(audio_clip.duration, duration)))

    final.write_videofile(
        out_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        logger=None,
    )

    # Clean up
    if audio_clip is not None:
        audio_clip.close()
    final.close()

    return out_path


def _build_subtitle_clips(
    script: str, width: int, height: int, duration: float
) -> list:
    """Create TextClip overlays for each configured language."""
    clips = []
    wrapped = textwrap.fill(script, width=40)

    # English subtitle at bottom-center
    try:
        en_sub = (
            TextClip(
                wrapped,
                fontsize=36,
                color="white",
                font="DejaVu-Sans-Bold",
                size=(width - 80, None),
                method="caption",
            )
            .set_position(("center", height - 350))
            .set_duration(duration)
        )
        clips.append(en_sub)
    except Exception:
        pass

    # Secondary language label (small, top-left)
    y_offset = 60
    for lang in settings.SUBTITLE_LANGUAGES:
        if lang == "EN":
            continue
        label = _TRANSLATIONS.get(lang, lang)
        if not label:
            continue
        try:
            clip = (
                TextClip(
                    f"[{lang}] {label}",
                    fontsize=20,
                    color="#94a3b8",
                    font="DejaVu-Sans",
                )
                .set_position((40, y_offset))
                .set_duration(duration)
            )
            clips.append(clip)
            y_offset += 30
        except Exception:
            continue

    return clips
