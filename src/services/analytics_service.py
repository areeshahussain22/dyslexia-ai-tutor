"""
Analytics Service implementation.
Calculates academic metrics (mastery, weak concepts, improvement trends, completion statistics)
returning structured dictionaries for future frontend dashboard consumption.
"""
from typing import List, Dict, Any

class AnalyticsService:
    def __init__(self):
        """
        Initializes the Analytics Service.
        """
        pass
        
    def calculate_topic_mastery(self, quiz_scores: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculates mastery levels grouped by lesson topic.
        
        Args:
            quiz_scores (List[Dict[str, Any]]): List of historical quiz score records.
            
        Returns:
            Dict[str, float]: Dictionary mapping topic/quiz ID to mastery percentage.
        """
        mastery = {}
        for q in quiz_scores:
            quiz_id = q.get("quiz_id", "unknown")
            score = q.get("score", 0.0)
            mastery[quiz_id] = score
        return mastery

    def identify_weak_concepts(self, quiz_scores: List[Dict[str, Any]]) -> List[str]:
        """
        Identifies concepts where the learner scored less than 70%.
        
        Args:
            quiz_scores (List[Dict[str, Any]]): List of historical quiz score records.
            
        Returns:
            List[str]: List of weak concept quiz/topic IDs.
        """
        weak = []
        for q in quiz_scores:
            quiz_id = q.get("quiz_id", "unknown")
            score = q.get("score", 0.0)
            if score < 0.7:
                weak.append(quiz_id)
        return list(set(weak))

    def analyze_improvement_trends(self, quiz_scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Builds a time-series list of scores to depict the learning improvement curve.
        
        Args:
            quiz_scores (List[Dict[str, Any]]): List of historical quiz score records.
            
        Returns:
            List[Dict[str, Any]]: List of dictionary points with date and score.
        """
        trends = []
        # Sort quiz scores chronologically
        sorted_scores = sorted(quiz_scores, key=lambda x: x.get("completed_at", ""))
        for idx, q in enumerate(sorted_scores):
            trends.append({
                "sequence_index": idx + 1,
                "quiz_id": q.get("quiz_id"),
                "score": q.get("score"),
                "completed_at": q.get("completed_at")
            })
        return trends

    def calculate_completion_statistics(self, completed_lessons: List[str], total_lessons_available: int = 10) -> Dict[str, Any]:
        """
        Calculates lesson progress ratios.
        
        Args:
            completed_lessons (List[str]): List of completed lesson IDs.
            total_lessons_available (int): Total lessons available in curriculum.
            
        Returns:
            Dict[str, Any]: Progress statistics.
        """
        completed_count = len(completed_lessons)
        completion_ratio = completed_count / total_lessons_available if total_lessons_available > 0 else 0.0
        return {
            "completed_lessons_count": completed_count,
            "total_lessons_curriculum": total_lessons_available,
            "completion_percentage": completion_ratio * 100.0,
            "is_curriculum_finished": completed_count >= total_lessons_available
        }
        
    def calculate_progress_metrics(self, quiz_scores: List[Dict[str, Any]], engagements: Dict[str, int]) -> Dict[str, Any]:
        """
        Combines other sub-metrics for backwards compatibility and dashboard summary views.
        """
        mastery = self.calculate_topic_mastery(quiz_scores)
        weak_concepts = self.identify_weak_concepts(quiz_scores)
        trends = self.analyze_improvement_trends(quiz_scores)
        
        avg_score = sum(q.get("score", 0.0) for q in quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
        preferred_channel = max(engagements, key=engagements.get) if engagements else "text"
        
        return {
            "average_quiz_accuracy": avg_score,
            "total_quizzes_completed": len(quiz_scores),
            "dominant_learning_channel": preferred_channel,
            "topic_mastery": mastery,
            "weak_concepts": weak_concepts,
            "improvement_trends": trends
        }
