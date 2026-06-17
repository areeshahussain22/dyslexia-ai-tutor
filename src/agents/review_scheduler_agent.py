"""
Review Scheduler Agent.
Calculates spaced repetition intervals using the SuperMemo-2 (SM-2) algorithm
and updates review schedules in review_schedule.json.
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.utils.helpers import load_json_db, save_json_db
from src.config.settings import DATABASE_DIR

class ReviewSchedulerAgent:
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initializes the ReviewSchedulerAgent.
        
        Args:
            db_path (Optional[Path]): Database file path.
        """
        self.db_path = db_path or (DATABASE_DIR / "review_schedule.json")
        
    def get_user_schedule(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Loads the list of scheduled reviews for a user.
        
        Args:
            user_id (str): Learner's identifier.
            
        Returns:
            List[Dict[str, Any]]: Review tasks.
        """
        data = load_json_db(self.db_path)
        return data.get(user_id, [])

    def schedule_review(self, user_id: str, topic_id: str, score: float) -> Dict[str, Any]:
        """
        Calculates and updates spaced repetition intervals using the SM-2 algorithm.
        
        Args:
            user_id (str): Learner's ID.
            topic_id (str): ID of the topic/lesson reviewed.
            score (float): Percentage accuracy (0.0 to 1.0) on the topic quiz.
            
        Returns:
            Dict[str, Any]: The updated schedule item details.
        """
        # Map score (0.0 - 1.0) to quality q (0 - 5)
        if score >= 1.0:
            q = 5
        elif score >= 0.8:
            q = 4
        elif score >= 0.6:
            q = 3
        elif score >= 0.4:
            q = 2
        elif score >= 0.2:
            q = 1
        else:
            q = 0

        # Load existing user schedule
        data = load_json_db(self.db_path)
        user_scheds = data.get(user_id, [])
        
        # Find existing item or create new default
        item = None
        for s in user_scheds:
            if s["topic_id"] == topic_id:
                item = s
                break
                
        if not item:
            item = {
                "topic_id": topic_id,
                "interval_days": 1,
                "ease_factor": 2.5,
                "repetitions": 0
            }
            user_scheds.append(item)
            
        # Apply SM-2 Spaced Repetition logic
        # q < 3 means the response was incorrect (reset repetition counter)
        if q < 3:
            item["repetitions"] = 0
            item["interval_days"] = 1
        else:
            if item["repetitions"] == 0:
                item["interval_days"] = 1
            elif item["repetitions"] == 1:
                item["interval_days"] = 6
            else:
                item["interval_days"] = int(round(item["interval_days"] * item["ease_factor"]))
            item["repetitions"] += 1
            
        # Update Ease Factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ef = item["ease_factor"] + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        item["ease_factor"] = max(1.3, ef)
        
        # Compute next review timestamp
        next_date = datetime.now() + timedelta(days=item["interval_days"])
        item["next_review_date"] = next_date.isoformat()
        
        data[user_id] = user_scheds
        save_json_db(self.db_path, data)
        
        return item
