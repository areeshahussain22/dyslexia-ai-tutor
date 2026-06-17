from pydantic import BaseModel, Field
from typing import List, Dict, Any

class LearnerProfile(BaseModel):
    user_id: str
    name: str
    dyslexia_level: str = "moderate"  # mild, moderate, severe
    preferred_channels: List[str] = Field(default_factory=lambda: ["text", "visual"])
    reading_speed_wpm: int = 120
    font_size: str = "18px"
    color_theme: str = "default"  # default, high_contrast, inverse_mode
    additional_preferences: Dict[str, Any] = Field(default_factory=dict)
