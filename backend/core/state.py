from dataclasses import dataclass, field
from typing import Any


@dataclass
class PipelineState:
    """Mutable state container shared across a single pipeline run."""

    topic: str = ""
    viral_score: int = 0
    winning_hook: str = ""
    script: str = ""
    audio_path: str = ""
    video_path: str = ""
    gdrive_url: str = ""
    quality_score: int = 0
    risk: float = 0.0
    reward: float = 0.0
    views: int = 0
    revenue: float = 0.0
    logs: list[dict[str, Any]] = field(default_factory=list)
    status: str = "idle"

    def add_log(self, message: str, level: str = "info") -> None:
        self.logs.append({"message": message, "level": level})

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "viral_score": self.viral_score,
            "winning_hook": self.winning_hook,
            "script": self.script,
            "audio_path": self.audio_path,
            "video_path": self.video_path,
            "gdrive_url": self.gdrive_url,
            "quality_score": self.quality_score,
            "risk": self.risk,
            "reward": self.reward,
            "views": self.views,
            "revenue": self.revenue,
            "status": self.status,
        }
