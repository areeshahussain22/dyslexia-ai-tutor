import unittest
import sys
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.models.learner_profile import LearnerProfile
from src.agents.user_profile_agent import UserProfileAgent
from src.agents.review_scheduler_agent import ReviewSchedulerAgent

class TestAgents(unittest.TestCase):
    def setUp(self):
        # Using temporary databases for test cases
        self.profile_db = Path(__file__).resolve().parent / "test_profiles.json"
        self.scheduler_db = Path(__file__).resolve().parent / "test_schedule.json"
        
        self.profile_agent = UserProfileAgent(db_path=self.profile_db)
        self.scheduler_agent = ReviewSchedulerAgent(db_path=self.scheduler_db)

    def tearDown(self):
        # Cleanup test DBs
        for db in [self.profile_db, self.scheduler_db]:
            if db.exists():
                db.unlink()

    def test_profile_creation_and_load(self):
        profile = LearnerProfile(
            user_id="test_user",
            name="Test Learner",
            dyslexia_level="mild",
            preferred_channels=["text"]
        )
        self.profile_agent.save_profile(profile)
        
        loaded = self.profile_agent.get_profile("test_user")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.name, "Test Learner")
        self.assertEqual(loaded.dyslexia_level, "mild")

    def test_scheduler_sm2(self):
        # Test scheduling with a perfect score (q = 5)
        item = self.scheduler_agent.schedule_review("test_user", "lesson_1", 1.0)
        self.assertEqual(item["repetitions"], 1)
        self.assertEqual(item["interval_days"], 1)
        
        # Test subsequent review repetition
        item2 = self.scheduler_agent.schedule_review("test_user", "lesson_1", 1.0)
        self.assertEqual(item2["repetitions"], 2)
        self.assertEqual(item2["interval_days"], 6)

if __name__ == "__main__":
    unittest.main()
