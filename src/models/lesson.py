from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Lesson(BaseModel):
    lesson_id: str
    title: str
    original_text: str
    adapted_text: Optional[str] = None
    visual_content_path: Optional[str] = None
    audio_content_path: Optional[str] = None
    comic_content_path: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
