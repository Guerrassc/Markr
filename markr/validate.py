import re

REPLACEMENTS = {
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-",
    "\u00a0": " ", "\u00ad": "",
}

STATUSES = {"met", "missing", "uncertain"}


def norm(text):
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip().lower()


def quote_in(quote, text):
    q = norm(quote)
    return len(q) >= 8 and q in norm(text)


def word_count(text):
    return len(text.split())


def validate_requirements(items, brief):
    kept, rejected = [], []
    for item in items:
        ok = (
            isinstance(item, dict)
            and isinstance(item.get("requirement"), str)
            and isinstance(item.get("source_quote"), str)
            and quote_in(item["source_quote"], brief)
        )
        (kept if ok else rejected).append(item)
    return kept, rejected


def validate_verdicts(verdicts, draft):
    checked = []
    for v in verdicts:
        if not isinstance(v, dict):
            continue
        status = v.get("status")
        evidence = v.get("evidence") or ""
        note = ""
        if status not in STATUSES:
            status, note = "uncertain", "The AI gave an invalid status"
        elif status == "met" and not quote_in(evidence, draft):
            status, note = "uncertain", "No matching quote found in the draft"
        checked.append({**v, "status": status, "evidence": evidence, "note": note})
    return checked