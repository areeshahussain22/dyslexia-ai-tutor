import unittest
import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.services.analytics_service import AnalyticsService
from src.services.diagram_service import DiagramService

class TestServices(unittest.TestCase):
    def setUp(self):
        self.analytics = AnalyticsService()
        self.diagram = DiagramService()
        
    def test_analytics_calculations(self):
        quiz_attempts = [{"quiz_id": "q1", "score": 0.8}, {"quiz_id": "q2", "score": 1.0}]
        engagements = {"text": 5, "audio": 2}
        
        metrics = self.analytics.calculate_progress_metrics(quiz_attempts, engagements)
        self.assertEqual(metrics["average_quiz_accuracy"], 0.9)
        self.assertEqual(metrics["dominant_learning_channel"], "text")
        
    def test_diagram_rendering(self):
        # DiagramService now returns Mermaid string definitions
        mermaid_code = self.diagram.generate_flowchart("Sample Topic", "Context data")
        self.assertTrue(len(mermaid_code) > 0)
        self.assertIn("flowchart TD", mermaid_code)

if __name__ == "__main__":
    unittest.main()
