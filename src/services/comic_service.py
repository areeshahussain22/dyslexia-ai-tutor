"""
Comic Service implementation.
Generates dyslexia-friendly learning comic strips to explain abstract topics.

Supports two paths:
  - PATH 1 (ACTIVE): OpenAI DALL-E image generation (requires OPENAI_API_KEY)
  - PATH 2 (FALLBACK): SVG string generation for testing/offline mode
"""
import os
from src.config.settings import OPENAI_API_KEY
from src.config.prompts import COMIC_GENERATION_PROMPT

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class ComicService:
    def __init__(self):
        """
        Initializes the Comic Service with OpenAI client.
        """
        self.api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if self.api_key and OpenAI is not None:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    # =========================================================================
    # PATH 1 (ACTIVE DEFAULT): OpenAI DALL-E image generation
    # =========================================================================
    def generate_comic_svg(self, topic: str, explanation: str) -> str:
        """
        Uses OpenAI DALL-E to generate a dyslexia-friendly comic strip image.
        
        Args:
            topic (str): The subject area.
            explanation (str): Core educational content.
            
        Returns:
            str: Image URL or fallback SVG if API not available.
        """
        if not self.client:
            # Fallback mockup high-contrast stick figure SVG if API key is not set
            return self._generate_fallback_svg(topic, explanation)

        try:
            prompt = f"Create a simple, dyslexia-friendly educational comic strip about: {topic}. {explanation}. Use clear colors, large fonts, and simple drawings."
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Return the image URL
            return response.data[0].url
        except Exception as e:
            # Fallback to SVG if DALL-E fails
            return self._generate_fallback_svg(topic, explanation)

    def _generate_fallback_svg(self, topic: str, explanation: str) -> str:
        """
        Generates a fallback dyslexia-friendly SVG comic layout for test/offline use.
        """
        svg = (
            '<svg viewBox="0 0 800 240" xmlns="http://www.w3.org/2000/svg" style="background:#FDFBF7; border:3px solid #0D5C75; border-radius:8px;">'
            '  <!-- Header -->'
            f'  <text x="20" y="30" font-family="OpenDyslexic, sans-serif" font-size="16" font-weight="bold" fill="#0D5C75">Topic comic: {topic[:40]}...</text>'
            '  '
            '  <!-- Panel 1 -->'
            '  <g transform="translate(20, 50)">'
            '    <rect width="230" height="160" fill="#FFFFFF" stroke="#0D5C75" stroke-width="2" rx="6"/>'
            '    <text x="15" y="25" font-family="OpenDyslexic, sans-serif" font-size="11" font-weight="bold" fill="#1A1A1A">Step 1: Introduction</text>'
            '    <circle cx="50" cy="90" r="12" fill="none" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="102" x2="50" y2="135" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="110" x2="35" y2="120" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="110" x2="65" y2="120" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="135" x2="40" y2="155" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="135" x2="60" y2="155" stroke="#A84C00" stroke-width="2"/>'
            '    <!-- Speech bubble -->'
            '    <path d="M 70,75 Q 110,60 150,75 Q 150,95 120,95 L 105,105 L 110,95 Z" fill="#F0F8FF" stroke="#0D5C75" stroke-width="1.5"/>'
            '    <text x="80" y="85" font-family="OpenDyslexic, sans-serif" font-size="9" fill="#1A1A1A">What is this?</text>'
            '    <text x="15" y="150" font-family="OpenDyslexic, sans-serif" font-size="9" fill="#555555">Let\'s break it down.</text>'
            '  </g>'
            '  '
            '  <!-- Panel 2 -->'
            '  <g transform="translate(280, 50)">'
            '    <rect width="230" height="160" fill="#FFFFFF" stroke="#0D5C75" stroke-width="2" rx="6"/>'
            '    <text x="15" y="25" font-family="OpenDyslexic, sans-serif" font-size="11" font-weight="bold" fill="#1A1A1A">Step 2: Core Concept</text>'
            '    <circle cx="50" cy="90" r="12" fill="none" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="102" x2="50" y2="135" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="110" x2="35" y2="105" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="110" x2="65" y2="105" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="135" x2="40" y2="155" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="135" x2="60" y2="155" stroke="#A84C00" stroke-width="2"/>'
            '    <!-- Speech bubble -->'
            '    <path d="M 70,75 Q 120,60 160,75 Q 160,95 130,95 L 115,105 L 120,95 Z" fill="#F0F8FF" stroke="#0D5C75" stroke-width="1.5"/>'
            f'    <text x="75" y="85" font-family="OpenDyslexic, sans-serif" font-size="8" fill="#1A1A1A">It is simple!</text>'
            f'    <text x="15" y="150" font-family="OpenDyslexic, sans-serif" font-size="8" fill="#555555">{explanation[:40]}...</text>'
            '  </g>'
            '  '
            '  <!-- Panel 3 -->'
            '  <g transform="translate(540, 50)">'
            '    <rect width="240" height="160" fill="#FFFFFF" stroke="#0D5C75" stroke-width="2" rx="6"/>'
            '    <text x="15" y="25" font-family="OpenDyslexic, sans-serif" font-size="11" font-weight="bold" fill="#1A1A1A">Step 3: Summary</text>'
            '    <circle cx="50" cy="90" r="12" fill="none" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="102" x2="50" y2="135" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="110" x2="35" y2="125" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="110" x2="65" y2="125" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="135" x2="40" y2="155" stroke="#A84C00" stroke-width="2"/>'
            '    <line x1="50" y1="135" x2="60" y2="155" stroke="#A84C00" stroke-width="2"/>'
            '    <!-- Speech bubble -->'
            '    <path d="M 70,75 Q 120,60 170,75 Q 170,95 130,95 L 115,105 L 120,95 Z" fill="#F0F8FF" stroke="#0D5C75" stroke-width="1.5"/>'
            '    <text x="75" y="85" font-family="OpenDyslexic, sans-serif" font-size="8" fill="#1A1A1A">Got it! Multi-cues work!</text>'
            '    <text x="15" y="150" font-family="OpenDyslexic, sans-serif" font-size="9" fill="#555555">Ready for practice.</text>'
            '  </g>'
            '</svg>'
        )
        return svg

    # =========================================================================
    # PATH 2 (FALLBACK): SVG string generation for testing/offline mode
    # =========================================================================
    # If OpenAI DALL-E fails or API key is not available, fallback to SVG generation.
