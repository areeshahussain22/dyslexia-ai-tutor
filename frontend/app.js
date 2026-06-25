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

let currentPdfText = '';
let currentMode = null;

const sampleOutputs = {
  summary: `\nSummary:\n\n- The document explains how to make learning easier with pictures, sound, and shorter text blocks.\n- It encourages reading using comfortable fonts and color themes.\n- It also suggests using visual tools such as mind maps and comics for better memory.\n`,
  flashcards: `\nFlash cards:\n\n1. What helps dyslexic learners focus?\n   - Clear fonts, bigger text, and calm colors.\n2. Why use comics?\n   - Comics add meaning with images and simple captions.\n3. What does audio support?\n   - It helps learners hear the material while reading along.\n`,
  flowchart: `flowchart TD\n  A[PDF upload] --> B[Choose a mode]\n  B --> C{Pick one}\n  C --> D[Summary]\n  C --> E[Comics]\n  C --> F[Mindmap]\n  C --> G[Audio]\n  C --> H[Flash cards]\n  C --> I[Flowchart]\n  D --> J[Read easy text]\n  E --> K[See fun images]\n  F --> L[Review main ideas]\n  G --> M[Listen while reading]\n  H --> N[Practice key facts]\n  I --> O[Follow a path]`,
  mindmap: `mindmap\n  root((PDF study))\n    Summary\n      Comfortable text\n      Short points\n    Comics\n      Friendly panels\n      Speech bubbles\n    Audio\n      Listen along\n      Calm pace\n    Flash cards\n      Quick reviews\n    Flowchart\n      Step-by-step`,
  comics: `\nComics idea:\n\nPanel 1: A smiling student sits at a desk with a PDF on screen. Caption: "I can upload a PDF and pick how I want to learn."\nPanel 2: The same student chooses a flowchart and a comic. Caption: "Big text, clear colors, and fun visuals help me focus."\nPanel 3: The student listens to audio while reading. Caption: "Audio makes it easy to follow along."\n`,
  audio: `Audio mode:\n\nListen to the content with simple narration, steady pace, and short sentences.\n\n[Audio playback will be generated here after upload in a real app.]\n`,
};

function setContentStyle() {
  const root = document.documentElement;
  root.style.setProperty('--content-bg', bgColor.value);
  root.style.setProperty('--content-text', textColor.value);
  root.style.setProperty('--content-accent', accentColor.value);
  contentArea.style.fontSize = `${fontSizeRange.value}px`;
  contentArea.style.background = bgColor.value;
  contentArea.style.color = textColor.value;
  fontSizeValue.textContent = `${fontSizeRange.value}px`;
}

function updateButtonStates(enabled) {
  modeButtons.forEach(button => { button.disabled = !enabled; });
  clearButton.disabled = !enabled;
}

function setActiveButton(mode) {
  modeButtons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === mode);
  });
}

function renderTextOutput(title, text) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>${title}</h3>
      <pre>${text}</pre>
    </div>
  `;
}

function renderDiagram(type, code) {
  contentArea.innerHTML = `
    <div class="content-output">
      <h3>${type}</h3>
      <pre>${code}</pre>
      <p class="hint">This is a sample diagram text format. In a full app, it would render as a visual chart.</p>
    </div>
  `;
}

function handleMode(mode) {
  currentMode = mode;
  statusText.textContent = `Showing ${mode} content.`;
  setActiveButton(mode);

  if (mode === 'audio') {
    contentArea.innerHTML = `
      <div class="content-output">
        <h3>Audio</h3>
        <p>Audio narration is ready. Press play to listen.</p>
        <audio controls>
          <source src="data:audio/mpeg;base64,${generateSilenceAudioBase64()}" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      </div>
    `;
    return;
  }

  if (mode === 'flowchart' || mode === 'mindmap') {
    renderDiagram(mode === 'flowchart' ? 'Flowchart' : 'Mindmap', sampleOutputs[mode]);
    return;
  }

  renderTextOutput(mode.charAt(0).toUpperCase() + mode.slice(1), sampleOutputs[mode]);
}

function generateSilenceAudioBase64() {
  return 'SUQzAwAAAAAAF1RTU0UAAAAAAwAAGhvbWUAAAACAAABAABPAAAAAEAAAAAAAAAAAAAAAAAAAAAAFAAAACABAAEAAQAAEAAQABFAAAAAAA=';
}

function parsePdfText(arrayBuffer) {
  return pdfjsLib.getDocument({ data: arrayBuffer }).promise.then(pdf => {
    const pagePromises = [];
    for (let pageIndex = 1; pageIndex <= pdf.numPages; pageIndex += 1) {
      pagePromises.push(pdf.getPage(pageIndex).then(page => page.getTextContent().then(content => {
        return content.items.map(item => item.str).join(' ');
      })));
    }
    return Promise.all(pagePromises).then(pageTexts => pageTexts.join('\n\n'));
  });
}

pdfInput.addEventListener('change', event => {
  const file = event.target.files[0];
  if (!file) return;
  statusText.textContent = 'Reading PDF…';

  const fileReader = new FileReader();
  fileReader.onload = () => {
    parsePdfText(fileReader.result).then(text => {
      currentPdfText = text || 'No text found in this PDF.';
      statusText.textContent = `PDF loaded — "${file.name}". Pick a mode to explore it.`;
      updateButtonStates(true);
      setActiveButton(null);
      contentArea.innerHTML = `
        <div class="content-output">
          <h3>PDF text preview</h3>
          <pre>${currentPdfText.substring(0, 1200)}${currentPdfText.length > 1200 ? '…' : ''}</pre>
        </div>
      `;
    }).catch(error => {
      statusText.textContent = 'Unable to read the PDF. Try another file.';
      contentArea.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><p>${error.message}</p></div>`;
      updateButtonStates(false);
    });
  };
  fileReader.readAsArrayBuffer(file);
});

modeButtons.forEach(button => {
  button.addEventListener('click', () => handleMode(button.dataset.mode));
});

clearButton.addEventListener('click', () => {
  currentPdfText = '';
  currentMode = null;
  pdfInput.value = '';
  statusText.textContent = 'Upload a PDF to begin.';
  setActiveButton(null);
  contentArea.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">📄</div>
      <p>Upload a PDF above, then pick a mode — summary, flashcards, audio, comics, flowchart, or mindmap.</p>
    </div>
  `;
  updateButtonStates(false);
});

fontSizeRange.addEventListener('input', () => setContentStyle());
bgColor.addEventListener('input', () => setContentStyle());
textColor.addEventListener('input', () => setContentStyle());
accentColor.addEventListener('input', () => setContentStyle());

setContentStyle();
