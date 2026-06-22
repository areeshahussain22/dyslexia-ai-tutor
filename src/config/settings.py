import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"
UPLOADS_DIR = BASE_DIR / "uploads"
GENERATED_CONTENT_DIR = BASE_DIR / "generated_content"
DATABASE_DIR = SRC_DIR / "database"

# Ensure directories exist
for directory in [UPLOADS_DIR, GENERATED_CONTENT_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
    
(GENERATED_CONTENT_DIR / "visuals").mkdir(exist_ok=True)
(GENERATED_CONTENT_DIR / "audio").mkdir(exist_ok=True)
(GENERATED_CONTENT_DIR / "comics").mkdir(exist_ok=True)
(GENERATED_CONTENT_DIR / "quizzes").mkdir(exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# RAG configuration
VECTOR_DB_PATH = str(BASE_DIR / "chroma_db")
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
