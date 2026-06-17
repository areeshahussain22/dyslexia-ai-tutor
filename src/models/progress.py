from pydantic import BaseModel, Field
from typing import List, Dict, Any

class QuizScore(BaseModel):
    quiz_id: str
    score: float
    total_questions: int
    completed_at: str

class Progress(BaseModel):
    user_id: str
    completed_lessons: List[str] = Field(default_factory=list)
    quiz_scores: List[QuizScore] = Field(default_factory=list)
    channel_engagement: Dict[str, int] = Field(
        default_factory=lambda: {"text": 0, "audio": 0, "visual": 0, "comic": 0}
    )
