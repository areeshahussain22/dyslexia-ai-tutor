import json
import sys
import os
from pathlib import Path

# Ensure the project root is on sys.path when launching via python src/backend.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

from src.main import initialize_tutor
from src.config.settings import UPLOADS_DIR, GENERATED_CONTENT_DIR

ALLOWED_EXTENSIONS = {"pdf"}

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(__name__, static_folder=str(frontend_dir), static_url_path="")
app.config["UPLOAD_FOLDER"] = str(UPLOADS_DIR)
app.config["GENERATED_FOLDER"] = str(GENERATED_CONTENT_DIR)

# Enable CORS for all routes
CORS(app, 
     resources={r"/*": {
         "origins": "*",
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"]
     }})

orchestrator = initialize_tutor()


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for frontend to verify backend connectivity."""
    return jsonify({"status": "ok", "message": "Backend is running"}), 200


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_profile_dyslexia_level(user_id: str = "guest") -> str:
    profile = orchestrator.user_profile_agent.get_profile(user_id)
    if profile and profile.dyslexia_level:
        return profile.dyslexia_level
    return "moderate"


@app.route("/api/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF part in the request."}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed."}), 400

    filename = secure_filename(file.filename)
    upload_path = Path(app.config["UPLOAD_FOLDER"]) / filename
    file.save(upload_path)

    try:
        # Ingest document into vector database (chunks + embeddings)
        chunks = orchestrator.content_ingestion_agent.ingest_document(str(upload_path))
        chunk_count = len(chunks)
        
        raw_text = orchestrator.content_ingestion_agent.document_loader.load_pdf(str(upload_path))
        lesson_id = f"lesson_{abs(hash(raw_text)) % 10000}"
        preview_text = raw_text[:2500]

        return jsonify({
            "fileName": filename,
            "previewText": preview_text,
            "fullText": raw_text,
            "lessonId": lesson_id,
            "backend": True,
            "vectorDbStatus": "SUCCESS",
            "chunkCount": chunk_count,
            "message": f"✓ PDF uploaded and stored in database ({chunk_count} chunks)"
        })
    except Exception as e:
        return jsonify({
            "error": f"Upload failed: {str(e)}",
            "vectorDbStatus": "FAILED"
        }), 500


@app.route("/api/mode", methods=["POST"])
def mode_content():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode")
    text = data.get("text", "")
    lesson_id = data.get("lessonId", "lesson_ui")

    if not mode or not text:
        return jsonify({"error": "Mode and text are required."}), 400

    try:
        if mode == "summary":
            dyslexia_level = get_profile_dyslexia_level()
            adapted = orchestrator.adaptation_agent._adapt_text(text, dyslexia_level)
            return jsonify({"type": "text", "title": "Summary", "content": adapted})

        if mode == "flashcards":
            flashcards = orchestrator.practice_agent.generate_practice_material(text)
            return jsonify({"type": "flashcards", "title": "Flash Cards", "content": flashcards})

        if mode in {"flowchart", "mindmap"}:
            diagram_type = "mindmap" if mode == "mindmap" else "flowchart"
            diagram_path = orchestrator.visual_learning_agent.generate_diagram(
                topic="PDF Topic",
                context=text,
                lesson_id=lesson_id,
                diagram_type=diagram_type
            )
            content = Path(diagram_path).read_text(encoding="utf-8")
            return jsonify({"type": "diagram", "title": mode.title(), "content": content})

        if mode == "comics":
            comic_path = orchestrator.visual_learning_agent.generate_comic(
                topic="PDF Topic",
                context=text,
                lesson_id=lesson_id
            )
            svg_content = Path(comic_path).read_text(encoding="utf-8")
            return jsonify({"type": "svg", "title": "Comic", "content": svg_content})

        if mode == "audio":
            try:
                # Generate intelligent audio narration
                audio_path = orchestrator.audio_learning_agent.generate_audio_narration(text, lesson_id)
                audio_file = Path(audio_path).name
                audio_url = f"/generated_content/audio/{audio_file}"
                return jsonify({
                    "type": "audio", 
                    "title": "Audio",
                    "content": audio_url,
                    "metadata": {
                        "type": "intelligent_narration",
                        "description": "AI-generated explanatory audio adapted to your learning style"
                    }
                })
            except Exception as audio_err:
                # Fallback: Return error with helpful message
                return jsonify({
                    "error": f"Audio generation failed: {str(audio_err)}",
                    "hint": "Make sure your OpenAI API key is configured in settings for intelligent audio generation"
                }), 500

        if mode == "quiz":
            try:
                # Generate quiz from content
                quiz = orchestrator.assessment_agent.generate_quiz(text, lesson_id)
                # Convert quiz to JSON-serializable format
                questions = []
                for q in quiz.questions:
                    questions.append({
                        "question_id": q.question_id,
                        "prompt": q.prompt,
                        "choices": q.choices,
                        "correct_choice_index": q.correct_choice_index,
                        "positive_reinforcement": q.positive_reinforcement,
                        "dyslexia_tips": q.dyslexia_tips
                    })
                return jsonify({
                    "type": "quiz",
                    "title": "Assessment Quiz",
                    "quiz_id": quiz.quiz_id,
                    "lesson_id": lesson_id,
                    "questions": questions,
                    "total_questions": len(questions)
                })
            except Exception as quiz_err:
                return jsonify({
                    "error": f"Quiz generation failed: {str(quiz_err)}"
                }), 500

        return jsonify({"error": "Unknown mode."}), 400
    except Exception as exc:
        error_message = str(exc)
        return jsonify({"error": "Backend processing failed.", "details": error_message}), 500


@app.route("/generated_content/audio/<path:filename>")
def serve_audio(filename: str):
    return send_from_directory(Path(app.config["GENERATED_FOLDER"]) / "audio", filename)


@app.route("/api/quiz-submit", methods=["POST"])
def submit_quiz():
    """Handle quiz submission, evaluate answers, and track progress."""
    data = request.get_json(silent=True) or {}
    quiz_id = data.get("quiz_id", "quiz_unknown")
    lesson_id = data.get("lesson_id", "lesson_unknown")
    user_answers = data.get("user_answers", [])
    context = data.get("context", "")
    user_id = data.get("user_id", "guest")

    try:
        # Generate the quiz to get correct answers
        quiz = orchestrator.assessment_agent.generate_quiz(context, lesson_id)
        
        # Evaluate answers
        results = orchestrator.assessment_agent.evaluate_answers(quiz, user_answers, context)
        
        # Record progress
        score = results.get("score", 0)
        orchestrator.progress_analytics_agent.record_activity(
            user_id=user_id,
            lesson_id=lesson_id,
            channel="quiz",
            quiz_score=score,
            total_questions=len(quiz.questions)
        )
        
        return jsonify({
            "quiz_id": quiz_id,
            "lesson_id": lesson_id,
            "score": score,
            "correct": results.get("correct", 0),
            "total": results.get("total", len(quiz.questions)),
            "overall_comment": results.get("overall_comment", "Good effort!"),
            "feedback": results.get("feedback_list", [])
        })
    except Exception as e:
        return jsonify({
            "error": f"Quiz evaluation failed: {str(e)}"
        }), 500


@app.route("/frontend/<path:path>")
def serve_frontend(path: str):
    return send_from_directory(app.static_folder, path)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    #app.run(host="127.0.0.1", port=8000, debug=True)
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
