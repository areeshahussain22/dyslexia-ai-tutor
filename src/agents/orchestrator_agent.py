"""
Orchestrator Agent.
Coordinates all sub-agents (Ingestion, Profile, Adaptation, Practice, Assessment, Spaced Repetition, and Analytics)
to manage the end-to-end learning workflow for dyslexic learners.
"""
from typing import Dict, Any, List, Optional
from src.utils.logger import logger
from src.models.learner_profile import LearnerProfile
from src.models.lesson import Lesson
from src.models.quiz import Quiz
from src.agents.user_profile_agent import UserProfileAgent
from src.agents.content_ingestion_agent import ContentIngestionAgent
from src.agents.adaptation_agent import AdaptationAgent
from src.agents.visual_learning_agent import VisualLearningAgent
from src.agents.audio_learning_agent import AudioLearningAgent
from src.agents.practice_agent import PracticeAgent
from src.agents.assessment_agent import AssessmentAgent
from src.agents.review_scheduler_agent import ReviewSchedulerAgent
from src.agents.progress_analytics_agent import ProgressAnalyticsAgent
from src.rag.retriever import Retriever

class OrchestratorAgent:
    def __init__(
        self,
        user_profile_agent: UserProfileAgent,
        content_ingestion_agent: ContentIngestionAgent,
        adaptation_agent: AdaptationAgent,
        visual_learning_agent: VisualLearningAgent,
        audio_learning_agent: AudioLearningAgent,
        practice_agent: PracticeAgent,
        assessment_agent: AssessmentAgent,
        review_scheduler_agent: ReviewSchedulerAgent,
        progress_analytics_agent: ProgressAnalyticsAgent,
        retriever: Retriever
    ):
        """
        Initializes the Orchestrator agent with all sub-agents.
        """
        self.user_profile_agent = user_profile_agent
        self.content_ingestion_agent = content_ingestion_agent
        self.adaptation_agent = adaptation_agent
        self.visual_learning_agent = visual_learning_agent
        self.audio_learning_agent = audio_learning_agent
        self.practice_agent = practice_agent
        self.assessment_agent = assessment_agent
        self.review_scheduler_agent = review_scheduler_agent
        self.progress_analytics_agent = progress_analytics_agent
        self.retriever = retriever
        
        logger.info("OrchestratorAgent initialized with all sub-agents.")

    def run_full_workflow(
        self,
        user_id: str,
        file_path: str,
        topic_query: str,
        user_answers: List[int],
        preferred_channel: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the full simulated workflow pipeline.
        
        Steps:
        1. Load / Create Profile
        2. Ingest & Index Document
        3. Retrieve Relevant Context Chunks
        4. Adapt Topic Content for Dyslexia
        5. Generate Practice material
        6. Create & Evaluate Assessment Quiz
        7. Update Review Scheduling
        8. Log Progress Analytics
        
        Args:
            user_id (str): Learner's ID.
            file_path (str): Document path to ingest.
            topic_query (str): Topic we want to study.
            user_answers (List[int]): Quiz answers selected by the user.
            preferred_channel (Optional[str]): Temporary override for preferred learning channel.
            
        Returns:
            Dict[str, Any]: Execution state and results summary of the learning session.
        """
        logger.info(f"Starting workflow for user={user_id}, file={file_path}, query='{topic_query}'")

        # 1. Load Profile
        profile = self.user_profile_agent.get_profile(user_id)
        if not profile:
            logger.info(f"User profile '{user_id}' not found. Creating default profile.")
            profile = LearnerProfile(
                user_id=user_id,
                name=user_id.capitalize(),
                dyslexia_level="moderate",
                preferred_channels=[preferred_channel] if preferred_channel else ["text", "visual"]
            )
            self.user_profile_agent.save_profile(profile)
            
        if preferred_channel and preferred_channel not in profile.preferred_channels:
            logger.info(f"Overriding preferences with channel: {preferred_channel}")
            profile.preferred_channels = [preferred_channel]

        # 2. Ingest & Index (RAG Ingestion)
        logger.info(f"Ingesting file: {file_path}")
        chunks = self.content_ingestion_agent.ingest_document(file_path)
        logger.info(f"Document chunked into {len(chunks)} fragments.")

        # 3. Retrieve Topic Context
        logger.info(f"Retrieving context for query: '{topic_query}'")
        retrieved_contexts = self.retriever.retrieve(topic_query)
        # Fallback to combined text if retrieval is empty (mock vector DB)
        if retrieved_contexts:
            combined_text = "\n\n".join([c["text"] for c in retrieved_contexts])
        else:
            combined_text = f"Sample retrieved study content about: {topic_query}"
        logger.info(f"Context retrieved successfully ({len(combined_text)} characters).")

        # 4. Adapt Topic Content
        logger.info("Routing content to adaptation agents.")
        lesson = self.adaptation_agent.adapt_content(
            original_text=combined_text,
            profile=profile,
            audio_agent=self.audio_learning_agent,
            visual_agent=self.visual_learning_agent
        )
        logger.info(f"Lesson created. Adapted text, audio={lesson.audio_content_path}, visual={lesson.visual_content_path}")

        # 5. Generate Practice material
        logger.info("Generating active practice exercises.")
        practice_cards = self.practice_agent.generate_practice_material(lesson.adapted_text or combined_text)

        # 6. Create Quiz & Evaluate Assessment
        logger.info("Creating assessment quiz.")
        quiz = self.assessment_agent.generate_quiz(lesson.adapted_text or combined_text, lesson.lesson_id)
        
        logger.info(f"Evaluating user answers: {user_answers}")
        grade_results = self.assessment_agent.evaluate_answers(quiz, user_answers, context=combined_text)
        quiz_score = grade_results["score"]

        # 7. Update Spaced Repetition Scheduling
        logger.info("Updating spaced repetition reviews.")
        schedule_item = self.review_scheduler_agent.schedule_review(
            user_id=user_id,
            topic_id=lesson.lesson_id,
            score=quiz_score
        )

        # 8. Log Progress Analytics
        logger.info("Updating learner progress database.")
        primary_channel = profile.preferred_channels[0] if profile.preferred_channels else "text"
        progress = self.progress_analytics_agent.record_activity(
            user_id=user_id,
            lesson_id=lesson.lesson_id,
            channel=primary_channel,
            quiz_score=quiz_score,
            total_questions=len(quiz.questions)
        )
        
        logger.info(f"Workflow completed successfully for user={user_id}. Score={quiz_score}")

        return {
            "profile": profile,
            "lesson": lesson,
            "practice_cards": practice_cards,
            "quiz": quiz,
            "grade_results": grade_results,
            "schedule_item": schedule_item,
            "progress": progress
        }
