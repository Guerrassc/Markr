from pathlib import Path

from markr.extract import parse_json_list
from markr.llm import ask_gemini
from markr.validate import validate_verdicts, word_count

PROMPT = Path(__file__).parent.parent / "prompts" / "check_draft_v1.txt"


def check_draft(requirements, draft, pages=None):
    system = PROMPT.read_text(encoding="utf-8")
    numbered = "\n".join(f"{i}. {r['requirement']}" for i, r in enumerate(requirements, 1))
    facts = f"Word count (computed by code, do not recount): {word_count(draft)}"
    if pages:
        facts += f"\nPage count (computed by code): {pages}"
    user = f"REQUIREMENTS:\n{numbered}\n\nFACTS:\n{facts}\n\nDRAFT:\n{draft}"

    verdicts = validate_verdicts(parse_json_list(ask_gemini(system, user)), draft)
    by_id = {str(v.get("id")): v for v in verdicts}

    results = []
    for i, req in enumerate(requirements, 1):
        v = by_id.get(str(i)) or {
            "status": "uncertain", "evidence": "",
            "note": "The AI gave no answer for this requirement",
        }
        results.append({**req, "status": v["status"],
                        "evidence": v.get("evidence", ""), "note": v.get("note", "")})
    return results