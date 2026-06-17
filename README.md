# Dyslexia & Neurodivergent AI Tutor

A Multi-Agent RAG-based AI Tutor for dyslexic and neurodivergent learners.

## Design Philosophy

The core philosophy of this platform is **accessibility without dilution**. We do not dumb down or simplify the educational concepts. Instead, we present the **exact same educational rigor** through multiple complementary channels (structured text, audio narration, visual diagrams, and cartoon comic strips) tailored to the learner's cognitive processing strengths.

---

## Multi-Agent Workflow

Below is the step-by-step pipeline executed during a learning session:

| Step | Phase | Agent Involved | Service Called | Description |
|---|---|---|---|---|
| 1 | Profile Management | User Profile Agent | None | Loads the student profile, preferred font size, severe/moderate/mild dyslexia styling, and theme colors. |
| 2 | Ingestion & Index | Content Ingestion Agent | RAG Core (ChromaDB) | Reads PDF/text, splits into overlapping chunks, computes embeddings, and indexes in ChromaDB. |
| 3 | Context Retrieval | Orchestrator Agent | Retriever | Performs semantic search to retrieve content chunks relevant to the user query. |
| 4 | Content Adaptation | Adaptation Agent | LLM Service | Rewrites the raw material to apply Bionic Reading bolding, clean spacing, and bullet points. |
| 5 | Multimodal Render | Visual & Audio Agents | Comic, Diagram, TTS | Triggers diagram code generation, SVG comic strip illustration, and MP3 audio narration files. |
| 6 | Active Recall | Practice Agent | LLM Service | Creates card exercises/active flashcard reviews for self-testing. |
| 7 | Assessment | Assessment Agent | LLM Service | Generates clear multiple-choice quizzes, evaluates answers, and explains mistakes. |
| 8 | Spaced Review | Review Scheduler Agent | None | Uses SuperMemo-2 (SM-2) to compute the next optimal date for review. |
| 9 | Learner Analytics | Progress Analytics Agent | Analytics Service | logs accuracy curves, completion rates, and preferred study channels. |

---

## Services & Integrations

### 1. LLM Service (`llm_service.py`)
- Standardized wrapper using the `google-genai` Gemini SDK.
- Exposes methods for text adaptation, summarizing, quiz generation, misconception explanations, and standard completions.
- Uses `gemini-2.5-flash` as the default model.

### 2. Gemini Integration (Comic Service)
- Uses the `google-genai` SDK to call Gemini models (e.g. `gemini-2.5-flash`) to generate structured SVG code.
- Generates clean, high-contrast panels, stick figures, text speech bubbles, and descriptions using warm cream backgrounds (#FDFBF7) and dark text (#1A1A1A) to minimize visual glare.

### 3. Comic Service Notes
- The current implementation is Gemini-only and uses `GEMINI_API_KEY`.
- The legacy OpenAI image path has been removed from active code.

### 4. Mermaid Diagram Strategy (`diagram_service.py`)
- Generates raw Mermaid text definitions (flowcharts, mindmaps, timelines, concept maps) from educational content using LLM prompts.
- **No image rendering is done in python**: Diagrams are kept as text files (`.mermaid`), allowing the frontend to natively render them using `mermaid.js` in the browser (improving responsiveness and speed).

### 5. TTS Service (`tts_service.py`)
- Integrates with the lightweight `gTTS` (Google Text-to-Speech) library.
- Saves audio narration files as `.mp3` under the `generated_content/audio/` folder.

---

## Dyslexia Accessibility Design Principles

1. **Font & Sizing**: OpenDyslexic or clean sans-serif (e.g. Arial, Comic Sans) in 18px+ sizing.
2. **Spacing**: Line height at 1.5x - 2.0x, letter spacing at 0.12em+, and word spacing at 0.27em+.
3. **Contrast**: High contrast but warm color pairings to prevent reading fatigue (cream #FDFBF7 or light gray #F4F4F4). Solid black-on-white is avoided due to heavy light glare.
4. **Multi-cues**: Feedback never uses color alone (e.g., green-only correct or red-only error). Standard symbols (checkmarks/crosses) and friendly encouraging tone parameters are always present.
5. **Bionic Bolding**: Bolding the starting syllables of words to anchor the eye while tracking.

---

## Setup & Running

1. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
3. Run the CLI tool:
   ```bash
   python src/main.py
   ```
4. Run a simulated workflow demo:
   ```bash
   python src/main.py --run-demo
   ```
5. Run the test suite:
   ```bash
   python -m unittest discover -s tests
   ```
