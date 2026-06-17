"""
Audio Learning Agent.
Handles intelligent audio generation from text inputs using TTS and LLM.
Generates engaging, explanatory audio narration tailored to learners' needs.
"""
from src.services.tts_service import TTSService

class AudioLearningAgent:
    def __init__(self, tts_service: TTSService, adaptation_agent=None, user_profile_agent=None):
        """
        Initializes the AudioLearningAgent.
        
        Args:
            tts_service (TTSService): Speech synthesizer service with LLM capabilities.
            adaptation_agent: Agent for adapting content to dyslexia levels
            user_profile_agent: Agent for retrieving user profile info
        """
        self.tts_service = tts_service
        self.adaptation_agent = adaptation_agent
        self.user_profile_agent = user_profile_agent
        
    def generate_audio_narration(self, text: str, lesson_id: str, user_id: str = "guest") -> str:
        """
        Generates intelligent, explanatory audio narration.
        Creates engaging audio that explains content clearly.
        
        Args:
            text (str): Accessible formatted lesson content.
            lesson_id (str): Unique lesson ID.
            user_id (str): User ID for profile-based adaptation
            
        Returns:
            str: Resolved filepath of the generated audio (.mp3).
        """
        filename = f"{lesson_id}_audio.mp3"
        
        # Generate intelligent explanatory audio
        # The TTS service will use LLM to generate better explanations
        return self.tts_service.generate_audio(text, filename, make_intelligent=True)
        
    def generate_lesson_audio(self, topic: str, lesson_text: str, user_id: str = "guest") -> str:
        """
        Generates intelligent audio specifically for a lesson with user adaptation.
        
        Args:
            topic (str): Lesson topic
            lesson_text (str): Full lesson text
            user_id (str): User ID for getting dyslexia level
            
        Returns:
            str: Path to the generated audio file
        """
        dyslexia_level = "moderate"
        
        # Get user's dyslexia level for personalization
        if self.user_profile_agent:
            try:
                profile = self.user_profile_agent.get_profile(user_id)
                if profile and profile.dyslexia_level:
                    dyslexia_level = profile.dyslexia_level
            except Exception as e:
                print(f"Warning: Could not get user profile: {e}")
        
        return self.tts_service.generate_lesson_audio(topic, lesson_text, dyslexia_level)
        
    def generate_summary_audio(self, text: str, lesson_id: str) -> str:
        """
        Generates a concise summary audio for quick review.
        
        Args:
            text (str): Full content
            lesson_id (str): Unique lesson ID
            
        Returns:
            str: Path to summary audio file
        """
        return self.tts_service.generate_summary_audio(text, lesson_id)
