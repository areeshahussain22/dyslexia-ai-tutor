"""
LLM Service implementation.
Centralizes all calls to LLMs using the OpenAI SDK.
"""
import json
import os
from typing import List, Dict, Any
from src.config.settings import OPENAI_API_KEY, LLM_MODEL
from src.config.prompts import (
    DYSLEXIA_REWRITE_PROMPT,
    QUIZ_GENERATION_PROMPT,
    MISCONCEPTION_ANALYSIS_PROMPT
)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class LLMService:
    def __init__(self):
        """
        Initializes the LLM service with the OpenAI SDK.
        """
        self.api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        self.model = LLM_MODEL or "gpt-4o-mini"
        
        if self.api_key and OpenAI is not None:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def _call_api(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        """
        Internal helper to centralize API requests.
        """
        if not self.client:
            # Fallback mock response if API key is not configured (e.g., testing environment)
            if "Mermaid" in system_prompt or "diagram" in system_prompt:
                return "flowchart TD\n  A-->B"
            if json_mode:
                return "[]"
            return f"[MOCK LLM RESPONSE] API Key not set. Prompt: {user_prompt[:50]}..."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content or ""

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates standard completion text.
        """
        return self._call_api(system_prompt, user_prompt, json_mode=False)

    def summarize(self, text: str, max_words: int = 100) -> str:
        """
        Summarizes the input text.
        """
        system_prompt = f"Summarize the text clearly. Keep the summary under {max_words} words."
        user_prompt = f"Text to summarize:\n{text}"
        return self._call_api(system_prompt, user_prompt, json_mode=False)

    def create_quiz(self, content: str, num_questions: int = 3) -> List[Dict[str, Any]]:
        """
        Generates dyslexia-friendly multiple-choice quiz questions.
        """
        system_prompt = QUIZ_GENERATION_PROMPT.format(content="", num_questions=num_questions)
        user_prompt = f"Content:\n{content}"
        raw_json = self._call_api(system_prompt, user_prompt, json_mode=True)
        
        try:
            return json.loads(raw_json)
        except (json.JSONDecodeError, TypeError):
            # Fallback safe array structure
            return []

    def explain_misconception(self, question: str, choices: List[str], correct: str, selected: str, context: str) -> str:
        """
        Provides friendly, dyslexia-supportive analysis of quiz answers.
        """
        system_prompt = "You are a dyslexia-supportive tutor explaining a misconception."
        user_prompt = MISCONCEPTION_ANALYSIS_PROMPT.format(
            question_prompt=question,
            choices=", ".join(choices),
            correct_choice=correct,
            user_choice=selected,
            context=context
        )
        return self._call_api(system_prompt, user_prompt, json_mode=False)

    def rewrite_for_dyslexia(self, text: str, dyslexia_level: str) -> str:
        """
        Re-structures study content to be dyslexia-accessible.
        """
        system_prompt = DYSLEXIA_REWRITE_PROMPT.format(dyslexia_level=dyslexia_level)
        return self._call_api(system_prompt, text, json_mode=False)
