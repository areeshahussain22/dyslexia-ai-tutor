# Intelligent Audio Narration Feature

## Overview

The Dyslexia AI Tutor now includes **intelligent audio narration** that goes beyond simple text-to-speech. Instead of just reading the PDF content word-for-word, the system uses AI to generate engaging, explanatory audio that:

- ✅ **Explains content clearly** with examples and real-world analogies
- ✅ **Breaks down complex concepts** into understandable parts
- ✅ **Adapts to learning style** based on dyslexia level
- ✅ **Maintains engaging tone** - encouraging and supportive
- ✅ **Provides natural pacing** suitable for audio learning
- ✅ **Displays directly in the interface** via HTML5 audio player

## How It Works

### 1. **Intelligent Text Generation**
When you click the **Audio** button after uploading a PDF:
1. The text is sent to the LLM (OpenAI) via `tts_service.py`
2. The LLM generates an engaging explanatory script using the prompt:
   - Opens with an engaging hook
   - Explains main concepts with examples
   - Highlights key takeaways
   - Closes with encouragement
   - Optimized for ~2-3 minutes of listening time

### 2. **Text-to-Speech Conversion**
The intelligent explanation is converted to speech using **gTTS (Google Text-to-Speech)** and saved as an MP3 file in `generated_content/audio/`

### 3. **Adaptation to Dyslexia Level**
The generated explanation can be further adapted based on the user's dyslexia level:
- **Mild**: Standard explanations with academic vocabulary
- **Moderate**: Simplified structures, clearer organization  
- **Severe**: Maximum simplification with bionic reading style

### 4. **Frontend Playback**
The audio is served via a dedicated endpoint and displayed with:
- HTML5 audio player with standard controls (play, pause, volume)
- Visual feedback and helpful tips
- Consistent styling matching the app's accessibility theme

## System Architecture

### Modified Files

#### 1. `src/services/tts_service.py`
**Key Changes:**
- Added `llm_service` parameter for AI-powered explanations
- Added `adaptation_agent` parameter for dyslexia-level customization
- New method: `_generate_intelligent_explanation()` - uses LLM to create engaging scripts
- New method: `generate_summary_audio()` - generates concise summaries
- Updated `generate_lesson_audio()` - now supports dyslexia-level adaptation

**New Methods:**
```python
def _generate_intelligent_explanation(self, text: str, topic: str = "") -> str:
    """Uses LLM to generate intelligent explanations suitable for audio."""

def generate_summary_audio(self, text: str, lesson_id: str) -> str:
    """Generates concise audio summary for quick review."""
```

#### 2. `src/agents/audio_learning_agent.py`
**Key Changes:**
- Added `adaptation_agent` support
- Added `user_profile_agent` support
- New method: `generate_summary_audio()` - for concise summaries
- Updated methods to use user dyslexia level for personalization

#### 3. `src/main.py`
**Key Changes:**
- Pass `llm_service` to `TTSService` constructor
- Pass `adaptation_agent` and `user_profile_agent` to `AudioLearningAgent`
- Proper initialization order to ensure all dependencies are available

#### 4. `frontend/app.js`
**Key Changes:**
- Enhanced `renderAudio()` function with better UI/UX
- Added helpful tips about the intelligent narration
- Better visual styling with accent color and information box
- Mobile-friendly audio player

#### 5. `src/backend.py`
**Key Changes:**
- Added error handling for audio generation
- Added metadata in response to indicate intelligent narration
- Helpful error messages if LLM API key is not configured

## Usage

### For Users

1. **Upload a PDF** using the "Upload a PDF" button
2. **Choose "Audio" mode** from the content modes
3. **Wait for intelligent audio generation** (takes 5-10 seconds depending on content)
4. **Play the audio** using the built-in player controls
5. **Adjust volume and playback** as needed

### For Developers

#### Generate Intelligent Audio Directly
```python
from src.services.tts_service import TTSService

tts = TTSService(llm_service=llm, adaptation_agent=adaptation)
audio_path = tts.generate_lesson_audio(
    topic="Photosynthesis",
    lesson_text="...",
    dyslexia_level="moderate"
)
```

#### Generate Summary Audio
```python
summary_path = tts.generate_summary_audio(
    text="...",
    lesson_id="lesson_123"
)
```

## Dependencies

### Required
- **gTTS** - Google Text-to-Speech (already in requirements.txt)
- **OpenAI API** - For intelligent explanation generation
  - Set `OPENAI_API_KEY` in environment or `.env` file
  - Uses `gpt-4o-mini` model

### Optional
- User's dyslexia level (from user profile) for adaptation

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini  # or any other OpenAI model
```

### Audio Output Location
All generated audio files are saved to: `generated_content/audio/`

### Audio Naming Convention
- Full explanatory audio: `{lesson_id}_audio.mp3`
- Lesson-specific audio: `lesson_{topic}_intelligent.mp3`
- Summary audio: `{lesson_id}_summary.mp3`

## Features

### ✅ Implemented
- [x] LLM-based intelligent explanation generation
- [x] Text-to-speech conversion using gTTS
- [x] Dyslexia-level adaptation
- [x] Frontend audio player integration
- [x] Audio file management and serving
- [x] Error handling and fallbacks
- [x] User profile-based personalization

### 🔄 Potential Enhancements
- [ ] Multiple voice options (different speakers)
- [ ] Playback speed adjustment
- [ ] Audio transcript generation
- [ ] Multiple language support
- [ ] Audio analytics (which sections are replayed most)
- [ ] Offline audio caching
- [ ] Custom audio generation (user provides topic)

## Troubleshooting

### Audio Generation Fails
**Issue**: Backend returns error about OpenAI API key
**Solution**: 
1. Set `OPENAI_API_KEY` environment variable
2. Verify API key is valid at https://platform.openai.com/account/api-keys
3. Check account has credits available

### Audio File Not Found
**Issue**: Audio player shows error or won't load
**Solution**:
1. Ensure `generated_content/audio/` directory exists
2. Check Flask backend is running: `python src/backend.py`
3. Verify CORS settings in backend

### Poor Audio Quality
**Issue**: Audio sounds robotic or unclear
**Suggestions**:
1. Try shortening the input text
2. Ensure text is well-formatted and clear
3. Test with the gTTS library directly to verify speech quality

## Performance Notes

- **Audio Generation Time**: 5-10 seconds per request (includes LLM processing + TTS)
- **File Size**: Typically 1-3 MB per audio file depending on content length
- **API Costs**: Each audio generation uses OpenAI tokens (GPT-4o-mini is cost-effective)
- **Caching**: Consider caching audio files if same content is requested multiple times

## Standards & Accessibility

The intelligent audio feature follows:
- **WCAG 2.1 Level AA** accessibility standards
- **Dyslexia-friendly principles**:
  - Clear, simple language
  - Logical structure
  - Paced for comfortable listening
  - Supporting material available (text, visuals, etc.)

## Future Integration Ideas

1. **Multimodal Learning**: Combine audio with synchronized text highlighting
2. **Interactive Audio**: Pause points for comprehension checks
3. **Audio Bookmarks**: Save important sections for later review
4. **Spaced Repetition**: Automatically generate review audio based on schedule
5. **Peer Audio**: Allow users to record their own explanatory audio

---

**Last Updated**: 2026-06-17
**Version**: 1.0
