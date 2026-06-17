"""
Practice Agent.
Generates interactive, dyslexia-friendly practice and study exercises (flashcards/quizzes)
by calling the LLM Service.
"""
from typing import Dict, Any, List
from src.services.llm_service import LLMService

class PracticeAgent:
    def __init__(self, llm_service: LLMService):
        """
        Initializes the PracticeAgent.
        
        Args:
            llm_service (LLMService): LLM communication service.
        """
        self.llm_service = llm_service
        
    def generate_practice_material(self, text: str) -> List[Dict[str, Any]]:
        """
        Creates active recall exercises. Uses create_quiz internally.
        
        Args:
            text (str): Source topic content.
            
        Returns:
            List[Dict[str, Any]]: List of quiz-style question cards.
        """
        quiz_data = self.llm_service.create_quiz(text, num_questions=2)
        
        # Format the quiz questions as flashcard representations
        flashcards = []
        for q in quiz_data:
            correct_idx = q.get("correct_choice_index", 0)
            choices = q.get("choices", [])
            correct_answer = choices[correct_idx] if correct_idx < len(choices) else ""
            
            flashcards.append({
                "exercise_type": "flashcard",
                "question": q.get("prompt"),
                "answer": correct_answer,
                "tip": q.get("dyslexia_tips")
            })
            
        # Fallback list if the Gemini LLM service is not configured / returns empty list
        if not flashcards:
            flashcards = [
                {
                    "exercise_type": "flashcard",
                    "question": "What is the core theme of this section?",
                    "answer": "Active multimodal learning helps process knowledge efficiently.",
                    "tip": "Multi-sensory cues improve learning retention."
                }
            ]
            
        return flashcards
