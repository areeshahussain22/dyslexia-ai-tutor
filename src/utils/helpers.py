import json
from pathlib import Path
from typing import Any, Dict

def load_json_db(file_path: Path) -> Dict[str, Any]:
    """Helper to safely load json data from local JSON database files."""
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_json_db(file_path: Path, data: Dict[str, Any]) -> None:
    """Helper to save dictionary data to local JSON database files."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
