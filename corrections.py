"""Learns word-level corrections and personal vocabulary from the user's edits. Stored locally as JSON."""
import difflib
import json
import re
from pathlib import Path

STORE = Path.home() / ".local-dictation" / "learned.json"


def load(path: Path = STORE) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"corrections": {}, "vocabulary": []}


def save(data: dict, path: Path = STORE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def apply(text: str, corrections: dict) -> str:
    # shortcut: whole-word replace in insertion order, no fuzzy matching; fine for a personal dictionary
    for wrong, right in corrections.items():
        text = re.sub(rf"\b{re.escape(wrong)}\b", right, text, flags=re.IGNORECASE)
    return text


def learn(heard: str, fixed: str, data: dict) -> dict:
    """Record word substitutions from heard -> fixed, and add corrected words to the vocabulary."""
    a, b = heard.split(), fixed.split()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if tag == "replace" and i2 - i1 == j2 - j1:
            for wrong, right in zip(a[i1:i2], b[j1:j2]):
                data["corrections"][wrong.strip(".,!?")] = right.strip(".,!?")
        if tag in ("replace", "insert"):
            for word in b[j1:j2]:
                clean = word.strip(".,!?")
                if clean and clean not in data["vocabulary"]:
                    data["vocabulary"].append(clean)
    return data


def initial_prompt(data: dict) -> str:
    # Whisper uses this as a hint, which helps it spell names and terms you use often.
    return ", ".join(data["vocabulary"][-50:])
