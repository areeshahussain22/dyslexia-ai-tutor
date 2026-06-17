from pydantic import BaseModel, Field
from typing import List, Dict, Any

class QuizQuestion(BaseModel):
    question_id: str
    prompt: str
    choices: List[str]
    correct_choice_index: int
    positive_reinforcement: str
    dyslexia_tips: str = ""

class Quiz(BaseModel):
    quiz_id: str
    lesson_id: str
    questions: List[QuizQuestion] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
