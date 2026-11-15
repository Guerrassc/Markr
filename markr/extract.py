import json
from pathlib import Path

from markr.llm import ask_gemini
from markr.validate import validate_requirements

PROMPT = Path(__file__).parent.parent / "prompts" / "extract_requirements_v2.txt"


def parse_json_list(text):
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("The AI answer was not a list")
    return json.loads(text[start:end + 1])


def extract_requirements(brief):
    system = PROMPT.read_text(encoding="utf-8")
    text = ask_gemini(system, brief)
    items = parse_json_list(text)
    return validate_requirements(items, brief)