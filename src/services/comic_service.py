"""
Comic Service implementation.
Generates dyslexia-friendly learning comic strips to explain abstract topics.

Uses Gemini 2.5 Flash to generate structured SVG comic strips (requires GEMINI_API_KEY).
Falls back to a static SVG template when the API is unavailable.
"""
import os
import re

from src.config.settings import GEMINI_API_KEY, GEMINI_MODEL
from src.config.prompts import COMIC_GENERATION_PROMPT

try:
    from google import genai
except ImportError:
    genai = None


class ComicService:
    def __init__(self):
        """Initializes the Comic Service with the Gemini client."""
        self.api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        self.model = GEMINI_MODEL or "gemini-2.5-flash"

        if self.api_key and genai is not None:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_comic_svg(self, topic: str, explanation: str) -> str:
        """
        Uses Gemini to generate a dyslexia-friendly SVG comic strip.

        Args:
            topic (str): The subject area.
            explanation (str): Core educational content.

        Returns:
            str: SVG markup, or fallback SVG if the API is unavailable.
        """
        if not self.client:
            return self._generate_fallback_svg(topic, explanation)

        try:
            prompt = COMIC_GENERATION_PROMPT.format(topic=topic, explanation=explanation)
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            svg = self._extract_svg(response.text or "")
            if svg:
                return svg
        except Exception:
            pass

        return self._generate_fallback_svg(topic, explanation)

    def _extract_svg(self, raw: str) -> str:
        """Pull a valid SVG document out of the model response."""
        cleaned = raw.strip()
        cleaned = re.sub(r"^```(?:xml|svg|html)?\s*\n?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

        match = re.search(r"(<svg[\s\S]*?</svg>)", cleaned, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        if cleaned.lstrip().lower().startswith("<svg"):
            return cleaned

        return ""

    def _generate_fallback_svg(self, topic: str, explanation: str) -> str:
        """Generates a fallback dyslexia-friendly SVG comic layout for test/offline use."""
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
