import sys
import os
from pathlib import Path

# Add project root directory to sys.path to allow absolute imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.utils.logger import logger
from src.utils.constants import ACCESSIBILITY_COLORS, DEFAULT_FONT
from src.config.settings import VECTOR_DB_PATH

# Models
from src.models.learner_profile import LearnerProfile

# RAG Core
from src.rag.document_loader import DocumentLoader
from src.rag.chunker import Chunker
from src.rag.embedding_service import EmbeddingService
from src.rag.vector_store import VectorStore
from src.rag.retriever import Retriever

# Services
from src.services.llm_service import LLMService
from src.services.tts_service import TTSService
from src.services.diagram_service import DiagramService
from src.services.comic_service import ComicService
from src.services.analytics_service import AnalyticsService

# Agents
from src.agents.user_profile_agent import UserProfileAgent
from src.agents.content_ingestion_agent import ContentIngestionAgent
from src.agents.adaptation_agent import AdaptationAgent
from src.agents.visual_learning_agent import VisualLearningAgent
from src.agents.audio_learning_agent import AudioLearningAgent
from src.agents.practice_agent import PracticeAgent
from src.agents.assessment_agent import AssessmentAgent
from src.agents.review_scheduler_agent import ReviewSchedulerAgent
from src.agents.progress_analytics_agent import ProgressAnalyticsAgent
from src.agents.orchestrator_agent import OrchestratorAgent

def initialize_tutor() -> OrchestratorAgent:
    """
    Initializes all RAG skeletons, service stubs, and agents,
    returning the central Orchestrator agent instance.
    """
    # 1. Initialize RAG Components
    doc_loader = DocumentLoader()
    chunker = Chunker()
    embed_service = EmbeddingService()
    vector_db = VectorStore(db_path=VECTOR_DB_PATH)
    retriever = Retriever(embedding_service=embed_service, vector_store=vector_db)

    # 2. Initialize Services (Stubs)
    llm = LLMService()
    tts = TTSService(llm_service=llm)  # Pass LLM service for intelligent audio
    diagram = DiagramService()
    comic = ComicService()
    analytics = AnalyticsService()

    # 3. Initialize Sub-Agents
    profile_agent = UserProfileAgent()
    ingestion_agent = ContentIngestionAgent(
        document_loader=doc_loader,
        chunker=chunker,
        embedding_service=embed_service,
        vector_store=vector_db
    )
    adaptation_agent = AdaptationAgent(llm_service=llm)
    visual_agent = VisualLearningAgent(
        diagram_service=diagram,
        comic_service=comic
    )
    # Pass adaptation and profile agents to audio agent for intelligent audio
    audio_agent = AudioLearningAgent(
        tts_service=tts, 
        adaptation_agent=adaptation_agent,
        user_profile_agent=profile_agent
    )
    practice_agent = PracticeAgent(llm_service=llm)
    assessment_agent = AssessmentAgent(llm_service=llm)
    scheduler_agent = ReviewSchedulerAgent()
    progress_agent = ProgressAnalyticsAgent(analytics_service=analytics)

    # 4. Instantiate Orchestrator
    orchestrator = OrchestratorAgent(
        user_profile_agent=profile_agent,
        content_ingestion_agent=ingestion_agent,
        adaptation_agent=adaptation_agent,
        visual_learning_agent=visual_agent,
        audio_learning_agent=audio_agent,
        practice_agent=practice_agent,
        assessment_agent=assessment_agent,
        review_scheduler_agent=scheduler_agent,
        progress_analytics_agent=progress_agent,
        retriever=retriever
    )

    return orchestrator

def main():
    # Print the required success message
    print("\nDyslexia AI Tutor initialized successfully.\n")
    logger.info("Dyslexia AI Tutor startup complete.")

    # Check if a simulation run is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--run-demo":
        print("--- RUNNING WORKFLOW DEMO SIMULATION ---")
        orchestrator = initialize_tutor()
        
        # Setup dummy files for demonstration
        uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
        uploads_dir.mkdir(exist_ok=True)
        sample_file = uploads_dir / "sample_topic.txt"
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(
                "Active recall and spaced repetition are highly effective techniques "
                "for cognitive consolidation. Presenting information via visual diagrams, "
                "auditory signals, and structured text layouts supports multi-channel processing."
            )
            
        # Run orchestrator simulation
        # User answer key: 1 (Index of cream bg), 1 (Index of False) -> 100% correct
        results = orchestrator.run_full_workflow(
            user_id="alex",
            file_path=str(sample_file),
            topic_query="spaced repetition",
            user_answers=[1, 1],
            preferred_channel="mixed"
        )
        
        print("\n--- SIMULATION RESULTS ---")
        print(f"Learner Name: {results['profile'].name}")
        print(f"Preferred Font: {DEFAULT_FONT}")
        print(f"Theme Colors: {ACCESSIBILITY_COLORS[results['profile'].color_theme]}")
        print(f"Adapted Text: {results['lesson'].adapted_text}")
        print(f"Visual File Path: {results['lesson'].visual_content_path}")
        print(f"Audio File Path: {results['lesson'].audio_content_path}")
        print(f"Comic File Path: {results['lesson'].comic_content_path}")
        print(f"Quiz Score: {results['grade_results']['score']} ({results['grade_results']['overall_comment']})")
        print(f"Spaced Repetition Schedule: Next review in {results['schedule_item']['interval_days']} day(s) on {results['schedule_item']['next_review_date']}")
        print(f"Learner Progress Completed Lessons: {results['progress'].completed_lessons}")
        print("------------------------------------------\n")

if __name__ == "__main__":
    main()
