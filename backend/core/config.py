import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central configuration for DAVNews backend services."""

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "credentials.json"
    )

    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "default")

    OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    GDRIVE_FOLDER_NAME: str = "DAVNews"

    SUBTITLE_LANGUAGES: list[str] = ["EN", "DA", "ES", "DE", "ZH", "FR"]

    # Video defaults
    VIDEO_WIDTH: int = 1080
    VIDEO_HEIGHT: int = 1920
    VIDEO_FPS: int = 30


settings = Settings()
