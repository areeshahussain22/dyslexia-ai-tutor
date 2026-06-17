"""
Assessment Agent.
Creates dyslexia-accessible quizzes with multiple-choice options.
Evaluates results and supplies positive reinforcement.
"""
from typing import List, Dict, Any
from src.services.llm_service import LLMService
from src.models.quiz import Quiz, QuizQuestion

class AssessmentAgent:
    def __init__(self, llm_service: LLMService):
        """
        Initializes the AssessmentAgent.
        
        Args:
            llm_service (LLMService): LLM communication.
        """
        self.llm_service = llm_service
        
    def generate_quiz(self, text: str, lesson_id: str) -> Quiz:
        """
        Generates a Quiz with multiple-choice options using LLMService.
        
        Args:
            text (str): Source topic text.
            lesson_id (str): Unique lesson ID.
            
        Returns:
            Quiz: Generated quiz.
        """
        raw_questions = self.llm_service.create_quiz(text, num_questions=2)
        
        questions_list = []
        for idx, q in enumerate(raw_questions):
            questions_list.append(QuizQuestion(
                question_id=q.get("question_id", f"q{idx}"),
                prompt=q.get("prompt", "Question details"),
                choices=q.get("choices", ["Choice A", "Choice B", "Choice C"]),
                correct_choice_index=q.get("correct_choice_index", 0),
                positive_reinforcement=q.get("positive_reinforcement", "Excellent job!"),
                dyslexia_tips=q.get("dyslexia_tips", "")
            ))
            
        # Fallback list if the Gemini LLM service is not configured / returns empty
        if not questions_list:
            q1 = QuizQuestion(
                question_id="q1",
                prompt="Which design approach reduces reading glare for dyslexic learners?",
                choices=["Bright blue backgrounds", "Soft warm cream backgrounds", "Flashing neon highlights"],
                correct_choice_index=1,
                positive_reinforcement="Spot on! Warm cream provides visual comfort by cutting glare.",
                dyslexia_tips="Dyslexic readers often find off-white or cream backgrounds far easier to read."
            )
            q2 = QuizQuestion(
                question_id="q2",
                prompt="True or False: Accessible lessons should omit important details.",
                choices=["True", "False"],
                correct_choice_index=1,
                positive_reinforcement="Great job! Accessible design adjusts the presentation channel, not the intellectual depth.",
                dyslexia_tips="Simplifying layout and styling is key, not lowering content expectations."
            )
            questions_list = [q1, q2]
            
        return Quiz(
            quiz_id=f"quiz_{hash(text) % 1000}",
            lesson_id=lesson_id,
            questions=questions_list
        )
        
    def evaluate_answers(self, quiz: Quiz, user_answers: List[int], context: str = "") -> Dict[str, Any]:
        """
        Scores a learner's quiz selections and produces detailed feedback.
        If the user gets a question wrong, calls explain_misconception.
        
        Args:
            quiz (Quiz): The quiz blueprint.
            user_answers (List[int]): Selected choice indices for each question.
            context (str): Original topic context.
            
        Returns:
            Dict[str, Any]: Assessment metrics and feedback summaries.
        """
        total_questions = len(quiz.questions)
        correct_count = 0
        feedback_details = []
        
        for idx, question in enumerate(quiz.questions):
            selected = user_answers[idx] if idx < len(user_answers) else -1
            is_correct = (selected == question.correct_choice_index)
            
            if is_correct:
                correct_count += 1
                reinforcement = question.positive_reinforcement
            else:
                # Call LLM service to analyze incorrect selection
                correct_text = question.choices[question.correct_choice_index] if question.correct_choice_index < len(question.choices) else "Unknown"
                selected_text = question.choices[selected] if 0 <= selected < len(question.choices) else "None"
                
                reinforcement = self.llm_service.explain_misconception(
                    question=question.prompt,
                    choices=question.choices,
                    correct=correct_text,
                    selected=selected_text,
                    context=context
                )
                
            feedback_details.append({
                "question_id": question.question_id,
                "prompt": question.prompt,
                "selected_index": selected,
                "correct_index": question.correct_choice_index,
                "is_correct": is_correct,
                "reinforcement": reinforcement,
                "tip": question.dyslexia_tips
            })
            
        score = correct_count / total_questions if total_questions > 0 else 0.0
        
        return {
            "score": score,
            "correct_answers": correct_count,
            "total_questions": total_questions,
            "feedback": feedback_details,
            "overall_comment": "Excellent effort! Multimodal learning strengthens pathways." if score >= 0.7 else "Great try! Review the visual diagrams to help consolidate this material."
        }
