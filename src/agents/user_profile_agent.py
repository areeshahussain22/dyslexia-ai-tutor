"""
User Profile Agent.
Manages persistent learner records, default accessibility configurations,
and custom display styles.
"""
from pathlib import Path
from typing import Optional
from src.models.learner_profile import LearnerProfile
from src.utils.helpers import load_json_db, save_json_db
from src.config.settings import DATABASE_DIR

class UserProfileAgent:
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initializes the UserProfileAgent.
        
        Args:
            db_path (Optional[Path]): Filepath of learner profiles database.
        """
        self.db_path = db_path or (DATABASE_DIR / "learner_profiles.json")
        
    def get_profile(self, user_id: str) -> Optional[LearnerProfile]:
        """
        Loads the LearnerProfile for a specific user ID.
        
        Args:
            user_id (str): The unique identifier of the learner.
            
        Returns:
            Optional[LearnerProfile]: The profile if found, otherwise None.
        """
        # TODO: Implement profile load verification
        data = load_json_db(self.db_path)
        user_data = data.get(user_id)
        if user_data:
            return LearnerProfile(**user_data)
        return None
        
    def save_profile(self, profile: LearnerProfile) -> None:
        """
        Persists a LearnerProfile into the database.
        
        Args:
            profile (LearnerProfile): The profile details to save.
        """
        # TODO: Validate schema constraints before write
        data = load_json_db(self.db_path)
        data[profile.user_id] = profile.model_dump()
        save_json_db(self.db_path, data)
        
    def update_preference(self, user_id: str, key: str, value: any) -> Optional[LearnerProfile]:
        """
        Updates a specific user preference and returns the updated profile.
        
        Args:
            user_id (str): Learner's identifier.
            key (str): Preference key (e.g. 'font_size').
            value (any): Value to assign.
            
        Returns:
            Optional[LearnerProfile]: The updated profile or None.
        """
        profile = self.get_profile(user_id)
        if profile:
            if hasattr(profile, key):
                setattr(profile, key, value)
            else:
                profile.additional_preferences[key] = value
            self.save_profile(profile)
            return profile
        return None
