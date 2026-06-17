"""
Progress Analytics Agent.
Logs user study milestones, completion rates, and learning channel interactions
into progress.json, using analytics helper stubs.
"""
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from src.models.progress import Progress, QuizScore
from src.utils.helpers import load_json_db, save_json_db
from src.config.settings import DATABASE_DIR
from src.services.analytics_service import AnalyticsService

class ProgressAnalyticsAgent:
    def __init__(self, analytics_service: AnalyticsService, db_path: Optional[Path] = None):
        """
        Initializes the ProgressAnalyticsAgent.
        
        Args:
            analytics_service (AnalyticsService): Calculations service.
            db_path (Optional[Path]): Database path.
        """
        self.analytics_service = analytics_service
        self.db_path = db_path or (DATABASE_DIR / "progress.json")
        
    def get_progress(self, user_id: str) -> Progress:
        """
        Loads the user's progress log from the database.
        
        Args:
            user_id (str): Unique learner ID.
            
        Returns:
            Progress: Loaded Progress object (new object created if missing).
        """
        data = load_json_db(self.db_path)
        progress_data = data.get(user_id)
        if progress_data:
            return Progress(**progress_data)
        return Progress(user_id=user_id)

    def save_progress(self, progress: Progress) -> None:
        """
        Saves the learner's progress metrics back to the database.
        
        Args:
            progress (Progress): The progress log details.
        """
        data = load_json_db(self.db_path)
        data[progress.user_id] = progress.model_dump()
        save_json_db(self.db_path, data)
        
    def record_activity(self, user_id: str, lesson_id: str, channel: str, quiz_score: Optional[float] = None, total_questions: int = 0) -> Progress:
        """
        Registers a study interaction (reading lesson, completing quiz) and calculates new analytics.
        
        Args:
            user_id (str): Learner ID.
            lesson_id (str): Lesson ID.
            channel (str): Interaction format ("text", "audio", "visual", "comic").
            quiz_score (Optional[float]): Optional quiz percentage (0.0 to 1.0) achieved.
            total_questions (int): Total questions in the quiz.
            
        Returns:
            Progress: The updated Progress profile log.
        """
        # TODO: Log details to analytics history charts
        progress = self.get_progress(user_id)
        
        # Track lesson completion
        if lesson_id not in progress.completed_lessons:
            progress.completed_lessons.append(lesson_id)
            
        # Increment channel interaction count
        if channel in progress.channel_engagement:
            progress.channel_engagement[channel] += 1
        else:
            progress.channel_engagement[channel] = 1
            
        # Record quiz attempt details
        if quiz_score is not None:
            new_score = QuizScore(
                quiz_id=f"quiz_{lesson_id}",
                score=quiz_score,
                total_questions=total_questions,
                completed_at=datetime.now().isoformat()
            )
            progress.quiz_scores.append(new_score)
            
        self.save_progress(progress)
        return progress
