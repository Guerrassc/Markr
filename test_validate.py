from markr.validate import quote_in, word_count, validate_requirements, validate_verdicts

brief = "The essay must be submitted as a PDF.\nMaximum 1,500 words, Harvard referencing."
draft = "This essay argues that remote work is here to stay."

assert quote_in("must be submitted as a pdf", brief)
assert quote_in("Maximum 1,500 words,\nHarvard referencing", brief)
assert not quote_in("Submit as a Word file", brief)
assert not quote_in("the", brief)
assert word_count("one two  three") == 3

items = [
    {"requirement": "Submit as PDF", "source_quote": "must be submitted as a PDF"},
    {"requirement": "Invented rule", "source_quote": "Include a title page"},
]
kept, rejected = validate_requirements(items, brief)
assert len(kept) == 1 and len(rejected) == 1

verdicts = [
    {"requirement": "A", "status": "met", "evidence": "remote work is here to stay"},
    {"requirement": "B", "status": "met", "evidence": "a sentence that is not in the draft"},
    {"requirement": "C", "status": "missing", "evidence": ""},
    {"requirement": "D", "status": "banana", "evidence": ""},
]
out = validate_verdicts(verdicts, draft)
assert [v["status"] for v in out] == ["met", "uncertain", "missing", "uncertain"]

print("all checks passed")