"""
TTS Service implementation.
Generates intelligent, explanatory spoken audio narration files using gTTS and LLM.
Saves audio output files to generated_content/audio/.
Uses LLM to generate smart explanations that explain content clearly.
"""
import os
from pathlib import Path
from gtts import gTTS
from src.config.settings import GENERATED_CONTENT_DIR

class TTSService:
    def __init__(self, llm_service=None, adaptation_agent=None):
        """
        Initializes the TTS Service with optional LLM and adaptation support.
        
        Args:
            llm_service: LLM service for generating intelligent explanations
            adaptation_agent: Adaptation agent for dyslexia-level customization
        """
        self.output_dir = GENERATED_CONTENT_DIR / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.llm_service = llm_service
        self.adaptation_agent = adaptation_agent
        
    def _generate_intelligent_explanation(self, text: str, topic: str = "") -> str:
        """
        Uses LLM to generate an intelligent explanation of the content.
        This makes the audio explanatory and educational.
        
        Args:
            text (str): Original lesson text
            topic (str): Topic name for context
            
        Returns:
            str: Intelligent explanation text suitable for audio narration
        """
        if not self.llm_service:
            # Fallback: just use the original text
            return text
            
        try:
            system_prompt = """You are an expert educator specializing in explaining complex concepts clearly and engagingly.
Your task is to create an engaging audio narration script that explains content in a way that:
1. Breaks down complex ideas into simple, understandable parts
2. Uses real-world examples and analogies
3. Emphasizes key concepts and their importance
4. Maintains an encouraging, supportive tone
5. Is paced for easy listening (not too fast, natural pauses)

Keep the explanation conversational and friendly, as if speaking directly to a learner."""

            user_prompt = f"""Create an engaging audio narration script explaining the following content:

Topic: {topic if topic else "Subject"}

Content to explain:
{text}

Generate a script that:
- Opens with an engaging hook
- Explains main concepts clearly with examples
- Highlights key takeaways
- Closes with encouragement
- Is approximately 2-3 minutes of speaking time (500-600 words)"""

            explanation = self.llm_service.generate_text(system_prompt, user_prompt)
            return explanation or text
        except Exception as e:
            print(f"Warning: Failed to generate intelligent explanation: {e}")
            return text
        
    def generate_audio(self, text: str, filename: str, make_intelligent: bool = True) -> str:
        """
        Synthesizes speech from text and saves it as an MP3.
        
        Args:
            text (str): Readable lesson text.
            filename (str): Base filename (e.g., 'lesson_1.mp3').
            make_intelligent (bool): If True, uses LLM to generate explanatory content.
            
        Returns:
            str: Absolute file path where the audio is saved.
        """
        if not filename.endswith(".mp3"):
            filename += ".mp3"
            
        filepath = self.output_dir / filename
        
        # Generate intelligent explanation if requested
        audio_text = text
        if make_intelligent and self.llm_service:
            audio_text = self._generate_intelligent_explanation(text, "")
        
        # Use slightly slower speech for better dyslexia-friendly audio comprehension
        # slow=False is standard, but we keep it for reasonable playback speed
        tts = gTTS(text=audio_text, lang='en', slow=False)
        tts.save(str(filepath))
        
        return str(filepath)

    def generate_lesson_audio(self, topic: str, lesson_text: str, dyslexia_level: str = "moderate") -> str:
        """
        Generates intelligent spoken narration specifically for a lesson context.
        
        Args:
            topic (str): Lesson topic.
            lesson_text (str): Lesson body.
            dyslexia_level (str): User's dyslexia level for adaptation.
            
        Returns:
            str: Resolved filepath of the generated audio.
        """
        # Generate intelligent explanation
        explanation = self._generate_intelligent_explanation(lesson_text, topic)
        
        # Optionally adapt the explanation based on dyslexia level
        if self.adaptation_agent:
            try:
                explanation = self.adaptation_agent._adapt_text(explanation, dyslexia_level)
            except Exception as e:
                print(f"Warning: Adaptation failed: {e}")
        
        safe_topic_name = "".join([c if c.isalnum() else "_" for c in topic.lower()])
        filename = f"lesson_{safe_topic_name[:20]}_intelligent.mp3"
        
        audio_text = f"Today's lesson on {topic}. {explanation}"
        
        # Use standard speed for comfortable listening
        tts = gTTS(text=audio_text, lang='en', slow=False)
        filepath = self.output_dir / filename
        tts.save(str(filepath))
        
        return str(filepath)
        
    def generate_summary_audio(self, text: str, lesson_id: str) -> str:
        """
        Generates concise audio summary of the content.
        Perfect for quick review and reinforcement.
        
        Args:
            text (str): Full lesson text
            lesson_id (str): Unique lesson ID
            
        Returns:
            str: Path to summary audio file
        """
        if self.llm_service:
            try:
                summary = self.llm_service.summarize(text, max_words=200)
            except Exception:
                summary = text[:500]  # Fallback to first 500 chars
        else:
            summary = text[:500]
            
        filename = f"{lesson_id}_summary.mp3"
        filepath = self.output_dir / filename
        
        tts = gTTS(text=summary, lang='en', slow=False)
        tts.save(str(filepath))
        
        return str(filepath)
