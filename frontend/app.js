const pdfInput = document.getElementById('pdfInput');
const statusText = document.getElementById('statusText');
const contentArea = document.getElementById('contentArea');
const modeButtons = Array.from(document.querySelectorAll('.mode-btn'));
const clearButton = document.getElementById('clearButton');
const fontSizeRange = document.getElementById('fontSizeRange');
const fontSizeValue = document.getElementById('fontSizeValue');
const bgColor = document.getElementById('bgColor');
const textColor = document.getElementById('textColor');
const accentColor = document.getElementById('accentColor');
const statusLight = document.getElementById('statusLight');
const connectionStatusText = document.getElementById('connectionStatusText');

let currentPdfText = '';
let currentMode = null;
let currentLessonId = 'lesson_ui';
let backendConnected = false;
// const BACKEND_URL = (window.location.protocol === 'file:' || !window.location.origin || window.location.origin === 'null')
//   ? 'http://127.0.0.1:8000'
//   : window.location.origin;
const BACKEND_URL = 'https://dyslexia-ai-tutor-production.up.railway.app';

// Check backend connection on page load
async function checkBackendConnection() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/health`, { method: 'GET' });
    if (response.ok) {
      backendConnected = true;
      statusLight.className = 'status-light connected';
      connectionStatusText.textContent = '✓ Backend Connected';
      connectionStatusText.style.color = '#0B6623';
    }
  } catch (error) {
    backendConnected = false;
    statusLight.className = 'status-light disconnected';
    connectionStatusText.textContent = '✗ Backend Disconnected';
    connectionStatusText.style.color = '#B22222';
  }
}

// Check connection on page load
document.addEventListener('DOMContentLoaded', () => {
  if (window.location.protocol === 'file:') {
    statusText.textContent = 'Open http://127.0.0.1:8000 in your browser (do not open index.html directly).';
  }
  checkBackendConnection();
  setInterval(checkBackendConnection, 10000); // Check every 10 seconds
});

function setContentStyle() {
  const root = document.documentElement;
  root.style.setProperty('--bg', bgColor.value);
  root.style.setProperty('--text', textColor.value);
  root.style.setProperty('--accent', accentColor.value);
  contentArea.style.fontSize = `${fontSizeRange.value}px`;
  fontSizeValue.textContent = `${fontSizeRange.value}px`;
}

function updateButtonStates(enabled) {
  modeButtons.forEach(button => {
    button.disabled = !enabled;
  });
  clearButton.disabled = !enabled;
}

function renderTextOutput(title, text) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>${title}</h3>
      <pre>${text}</pre>
    </div>
  `;
}

function renderFlashcards(cards) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>Flash Cards</h3>
      ${cards.map(card => `
        <div class="flashcard">
          <strong>Q:</strong> ${card.question}
          <p><strong>A:</strong> ${card.answer}</p>
          ${card.tip ? `<p class="hint">Tip: ${card.tip}</p>` : ''}
        </div>
      `).join('')}
    </div>
  `;
}

function renderDiagram(type, code) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>${type}</h3>
      <pre>${code}</pre>
      <p class="hint">This is a Mermaid diagram text format. In a full app it can render visually.</p>
    </div>
  `;
}

function renderSvg(title, svg) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>${title}</h3>
      <div class="svg-wrapper">${svg}</div>
    </div>
  `;
}

function renderAudio(url) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>🔊 Intelligent Audio Narration</h3>
      <p class="hint" style="margin-bottom: 15px;">This is AI-generated explanatory audio that intelligently explains the content with examples and clarity.</p>
      <div style="background-color: var(--accent); padding: 20px; border-radius: 8px; margin: 15px 0;">
        <audio controls style="width: 100%; height: 40px;">
          <source src="${url}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
      </div>
      <div style="background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent);">
        <p style="margin: 0; font-size: 14px; color: #333;">
          <strong>💡 Tip:</strong> Use the playback controls to play, pause, and adjust volume. The audio adapts to your learning style and dyslexia level for optimal comprehension.
        </p>
      </div>
    </div>
  `;
}

function renderQuiz(quizData) {
  let quizHTML = `
    <div class="content-output">
      <h3>📝 Dyslexia-Friendly Assessment Quiz</h3>
      <p class="hint" style="margin-bottom: 20px;">Answer each question below. The quiz is designed to be clear and encouraging.</p>
      <form id="quizForm" style="max-width: 600px;">
  `;

  quizData.questions.forEach((question, idx) => {
    quizHTML += `
      <div style="margin-bottom: 25px; padding: 15px; background-color: #f9f9f9; border-radius: 8px; border-left: 4px solid var(--accent);">
        <h4 style="margin: 0 0 15px 0; color: var(--text);">Question ${idx + 1} of ${quizData.total_questions}</h4>
        <p style="margin: 0 0 15px 0; font-weight: 500; color: var(--text);">${question.prompt}</p>
        ${question.dyslexia_tips ? `<p style="margin: 0 0 10px 0; font-size: 13px; color: #666; font-style: italic;">💡 ${question.dyslexia_tips}</p>` : ''}
        <div style="margin: 10px 0;">
          ${question.choices.map((choice, choiceIdx) => `
            <label style="display: block; margin: 8px 0; padding: 10px; border-radius: 4px; background-color: white; cursor: pointer; border: 2px solid #ddd; transition: all 0.2s;">
              <input type="radio" name="question_${idx}" value="${choiceIdx}" style="margin-right: 10px;">
              <span>${choice}</span>
            </label>
          `).join('')}
        </div>
      </div>
    `;
  });

  quizHTML += `
      <button type="submit" style="background-color: var(--accent); color: white; padding: 12px 30px; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 15px;">
        Submit Quiz
      </button>
      </form>
    </div>
  `;

  contentArea.innerHTML = quizHTML;

  // Add form submission handler
  document.getElementById('quizForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const answers = [];
    quizData.questions.forEach((_, idx) => {
      const selected = document.querySelector(`input[name="question_${idx}"]:checked`);
      answers.push(selected ? parseInt(selected.value) : -1);
    });

    try {
      const response = await fetch(`${BACKEND_URL}/api/quiz-submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quiz_id: quizData.quiz_id,
          lesson_id: quizData.lesson_id,
          user_answers: answers,
          context: currentPdfText
        })
      });

      if (!response.ok) throw new Error('Failed to submit quiz');
      
      const result = await response.json();
      displayQuizResults(result);
    } catch (error) {
      statusText.textContent = 'Error submitting quiz: ' + error.message;
    }
  });
}

function displayQuizResults(results) {
  let resultsHTML = `
    <div class="content-output">
      <h3>📊 Quiz Results</h3>
      <div style="background-color: ${results.score >= 0.7 ? '#d4edda' : '#fff3cd'}; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <h4 style="margin-top: 0;">Score: ${Math.round(results.score * 100)}% (${results.correct}/${results.total})</h4>
        <p style="font-size: 16px; margin: 10px 0;">${results.overall_comment}</p>
      </div>
  `;

  if (results.feedback && results.feedback.length > 0) {
    resultsHTML += '<h4>Feedback:</h4>';
    results.feedback.forEach((fb) => {
      resultsHTML += `
        <div style="margin: 15px 0; padding: 12px; border-radius: 4px; ${fb.is_correct ? 'background-color: #e8f5e9; border-left: 4px solid #4caf50;' : 'background-color: #ffebee; border-left: 4px solid #f44336;'}">
          <p style="margin: 0; font-weight: bold;">${fb.is_correct ? '✅ Correct!' : '❌ Not quite'}</p>
          <p style="margin: 8px 0 0 0;">${fb.feedback_text}</p>
        </div>
      `;
    });
  }

  resultsHTML += '</div>';
  contentArea.innerHTML = resultsHTML;
  statusText.textContent = `Quiz completed! Score: ${Math.round(results.score * 100)}%`;
}

async function callModeApi(mode) {
  statusText.textContent = `Loading ${mode}...`;

  try {
    const response = await fetch(`${BACKEND_URL}/api/mode`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        mode,
        lessonId: currentLessonId
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      statusText.textContent = error.error || 'Unable to fetch backend content.';
      return;
    }

    const data = await response.json();
    statusText.textContent = `Showing ${mode} content.`;

    if (data.type === 'text') {
      renderTextOutput(data.title, data.content);
    } else if (data.type === 'flashcards') {
      renderFlashcards(data.content);
    } else if (data.type === 'diagram') {
      renderDiagram(data.title, data.content);
    } else if (data.type === 'svg') {
      renderSvg(data.title, data.content);
    } else if (data.type === 'audio') {
      renderAudio(data.content);
    } else if (data.type === 'quiz') {
      renderQuiz(data);
    } else {
      renderTextOutput('Notice', JSON.stringify(data, null, 2));
    }
  } catch (error) {
    statusText.textContent = 'Backend request failed. Is the Flask server running?';
    contentArea.innerHTML = `<p class="empty-state">${error.message}</p>`;
  }
}

function handleMode(mode) {
  currentMode = mode;
  callModeApi(mode);
}

function generateSilenceAudioBase64() {
  return 'SUQzAwAAAAAAF1RTU0UAAAAAAwAAGhvbWUAAAACAAABAABPAAAAAEAAAAAAAAAAAAAAAAAAAAAAFAAAACABAAEAAQAAEAAQABFAAAAAAA=';
}

async function uploadPdf(file) {
  const uploadData = new FormData();
  uploadData.append('pdf', file);

  let response;
  try {
    response = await fetch(`${BACKEND_URL}/api/upload`, {
      method: 'POST',
      body: uploadData
    });
  } catch (error) {
    if (window.location.protocol === 'file:') {
      throw new Error('Cannot upload from a local file. Start the server and open http://127.0.0.1:8000');
    }
    throw new Error(`Could not reach backend at ${BACKEND_URL}. Start it with: python src/backend.py`);
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || 'PDF upload failed.');
  }

  return response.json();
}

pdfInput.addEventListener('change', async event => {
  const file = event.target.files[0];
  if (!file) return;

  statusText.textContent = '📤 Uploading PDF...';
  updateButtonStates(false);

  try {
    // Show uploading progress
    statusText.textContent = '📤 Uploading PDF (reading file)...';
    
    const data = await uploadPdf(file);
    
    // Show processing progress
    statusText.textContent = '⚙️ Processing (chunking & storing)...';
    
    currentPdfText = data.previewText || '';
    currentLessonId = data.lessonId || 'lesson_ui';
    
    // Show vector DB storage status
    if (data.vectorDbStatus === "SUCCESS") {
      statusText.textContent = `✅ ${data.message}`;
      contentArea.innerHTML = `
        <div class="content-output success-status">
          <h3>✓ Upload Successful</h3>
          <p><strong>File:</strong> ${data.fileName}</p>
          <p><strong>Chunks stored:</strong> ${data.chunkCount}</p>
          <p><strong>Status:</strong> Ready for analysis</p>
          <p style="color: #0B6623; font-weight: bold; margin-top: 10px;">✅ ${data.message}</p>
          <hr>
          <h4>PDF Preview:</h4>
          <pre>${currentPdfText.substring(0, 1200) + (currentPdfText.length > 1200 ? '...' : '')}</pre>
        </div>
      `;
    } else {
      statusText.textContent = '✅ PDF uploaded. Choose a mode to see dyslexia-friendly content.';
      renderTextOutput('PDF text preview', currentPdfText.substring(0, 1200) + (currentPdfText.length > 1200 ? '...' : ''));
    }
    
    updateButtonStates(true);
  } catch (error) {
    statusText.textContent = '❌ ' + error.message;
    contentArea.innerHTML = `<p class="empty-state">${error.message}</p>`;
    updateButtonStates(false);
  }
});

modeButtons.forEach(button => {
  button.addEventListener('click', () => handleMode(button.dataset.mode));
});

clearButton.addEventListener('click', () => {
  currentPdfText = '';
  currentMode = null;
  currentLessonId = 'lesson_ui';
  pdfInput.value = '';
  statusText.textContent = 'Upload a PDF to begin.';
  contentArea.innerHTML = `
    <div class="empty-state">
      <p>Once your PDF is loaded, choose one of the modes to see the content, comics, diagram, flashcards, or hear it read aloud.</p>
    </div>
  `;
  updateButtonStates(false);
});

fontSizeRange.addEventListener('input', () => setContentStyle());
bgColor.addEventListener('input', () => setContentStyle());
textColor.addEventListener('input', () => setContentStyle());
accentColor.addEventListener('input', () => setContentStyle());

setContentStyle();
