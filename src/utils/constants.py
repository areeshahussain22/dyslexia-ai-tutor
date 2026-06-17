# Accessibility Defaults for Dyslexic Learners

DEFAULT_FONT = "OpenDyslexic"
DEFAULT_FONT_SIZE = "18px"
DEFAULT_LINE_HEIGHT = "1.8"  # 1.5x - 2x spacing
DEFAULT_WORD_SPACING = "0.27em"

# Color Palettes (High Contrast, avoiding red/green-only indicators for colorblindness/visual comfort)
ACCESSIBILITY_COLORS = {
    "default": {
        "background": "#FDFBF7",  # Off-white / warm cream (reduces glare)
        "text": "#1A1A1A",
        "primary": "#0D5C75",     # Deep blue-green
        "secondary": "#A84C00",   # Muted orange
        "success": "#0B6623",     # Safe green (with checkmarks/double cues)
        "error": "#B22222"        # Safe red (with cross/double cues)
    },
    "high_contrast": {
        "background": "#FFFFFF",
        "text": "#000000",
        "primary": "#0000EE",
        "secondary": "#551A8B",
        "success": "#008000",
        "error": "#FF0000"
    },
    "inverse_mode": {
        "background": "#121212",  # Dark mode
        "text": "#F5F5F5",
        "primary": "#3399FF",
        "secondary": "#FF9933",
        "success": "#33CC66",
        "error": "#FF3333"
    }
}

# Instructional preferences
SHORT_INSTRUCTIONS_ONLY = True
NO_RED_GREEN_ONLY_FEEDBACK = True  # Always use text, symbols, or double cues (e.g. checkmark/cross + text)
SUPPORTED_DIAGRAM_FORMATS = ["svg", "mermaid", "ascii"]
SUPPORTED_ADAPTATION_MODES = ["text", "audio", "visual", "comic", "mixed"]
