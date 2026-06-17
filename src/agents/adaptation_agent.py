"""
Adaptation Agent.
Coordinates and routes content adaptation requests based on learner profiles.
Supports Text, Audio, Visual, Comic, and Mixed adaptation formats.
"""
from typing import Dict, Any, List, Optional
from src.models.learner_profile import LearnerProfile
from src.models.lesson import Lesson
from src.services.llm_service import LLMService

class AdaptationAgent:
    def __init__(self, llm_service: LLMService):
        """
        Initializes the AdaptationAgent.
        
        Args:
            llm_service (LLMService): Unified LLM wrapper.
        """
        self.llm_service = llm_service
        
    def adapt_content(self, original_text: str, profile: LearnerProfile, 
                      audio_agent: Any, visual_agent: Any) -> Lesson:
        """
        Routes text content adaptation based on user preference channels.
        
        Args:
            original_text (str): Raw material text retrieved via RAG.
            profile (LearnerProfile): User's profile preferences.
            audio_agent (Any): Instance of AudioLearningAgent.
            visual_agent (Any): Instance of VisualLearningAgent.
            
        Returns:
            Lesson: Adapted lesson containing formatted content and media file paths.
        """
        lesson = Lesson(
            lesson_id=f"lesson_{hash(original_text) % 10000}",
            title=f"Adapted Lesson for {profile.name}",
            original_text=original_text
        )
        
        channels = profile.preferred_channels
        if not channels:
            channels = ["text"]
            
        # Mixed support: if mixed, generate all content formats
        if "mixed" in channels:
            channels = ["text", "audio", "visual", "comic"]
            
        # Route to appropriate channels
        for channel in channels:
            if channel == "text":
                lesson.adapted_text = self._adapt_text(original_text, profile.dyslexia_level)
            elif channel == "audio":
                # Ensure text is adapted first for speech narration
                if not lesson.adapted_text:
                    lesson.adapted_text = self._adapt_text(original_text, profile.dyslexia_level)
                lesson.audio_content_path = audio_agent.generate_audio_narration(lesson.adapted_text, lesson.lesson_id)
            elif channel == "visual":
                # Default to flowchart for general visual preference
                lesson.visual_content_path = visual_agent.generate_diagram(
                    topic=lesson.title, 
                    context=original_text, 
                    lesson_id=lesson.lesson_id,
                    diagram_type=profile.additional_preferences.get("diagram_type", "flowchart")
                )
            elif channel == "comic":
                lesson.comic_content_path = visual_agent.generate_comic(
                    topic=lesson.title, 
                    context=original_text, 
                    lesson_id=lesson.lesson_id
                )
                
        return lesson

    def _adapt_text(self, text: str, dyslexia_level: str) -> str:
        """
        Adapts source text by querying rewrite_for_dyslexia on LLMService.
        
        Args:
            text (str): Original text block.
            dyslexia_level (str): Level of dyslexia.
            
        Returns:
            str: Reformatted/adapted text.
        """
        return self.llm_service.rewrite_for_dyslexia(text, dyslexia_level)
