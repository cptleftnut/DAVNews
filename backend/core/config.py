import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central configuration for DAVNews backend services."""

    # Paid APIs (optional)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "credentials.json"
    )
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "default")

    # Free alternatives
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")
    EDGE_TTS_VOICE: str = os.getenv("EDGE_TTS_VOICE", "en-US-GuyNeural")

    # TTS provider priority: "elevenlabs", "edge-tts"
    TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "auto")
    # LLM provider priority: "openai", "ollama"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "auto")

    OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    GDRIVE_FOLDER_NAME: str = "DAVNews"

    SUBTITLE_LANGUAGES: list[str] = ["EN", "DA", "ES", "DE", "ZH", "FR"]

    # Video defaults
    VIDEO_WIDTH: int = 1080
    VIDEO_HEIGHT: int = 1920
    VIDEO_FPS: int = 30


settings = Settings()
