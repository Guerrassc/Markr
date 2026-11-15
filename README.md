# Markr

Markr turns an assignment brief into a checklist, then checks your draft against it so you don't lose marks to something you missed.
Semester project for Digital Transformation (BPINFOR-131), University of Luxembourg, WS2026-27.
Status: **M3 MVP**, tag `m3`. It only checks your work, it never writes it.

## 1. What it does

1. Upload or paste a brief (PDF or text).
2. Markr lists the requirements. Under each one it shows the sentence of the brief it came from.
3. Upload or paste your draft.
4. Each requirement is marked met, missing or uncertain. For "met" it shows the part of your draft that backs it up.

The AI suggests the requirements and the verdicts, but plain code checks them. A requirement is dropped if its quote isn't really in the brief. A "met" becomes "uncertain" if its evidence isn't really in the draft. Word and page counts are done by code, never by the AI.

## 2. Users and value proposition

Students who have several assignments at once and are afraid of missing a rule in one of the briefs. Unlike rereading the brief by hand, or pasting it into a general chatbot and hoping, Markr gives a saved checklist and a check against the draft. The interviews are in `PROJECT_LOG.md` (M1).

## 3. How to run it

You need Python 3.11 or newer and a Gemini API key (free from Google AI Studio).

1. `git clone https://github.com/Guerrassc/Markr.git` and then `cd Markr`
2. `python -m venv .venv`, then activate it (Windows: `.venv\Scripts\activate`, Mac/Linux: `source .venv/bin/activate`)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and paste your key after `GEMINI_API_KEY=`
5. `streamlit run app.py`

The app opens in your browser at `localhost:8501`. To check the code without an API key: `python test_validate.py`.

## 4. Architecture

See `docs/architecture.md`.

## 5. AI components

- Model: `gemini-3.5-flash-lite`, set in `.env` (`MARKR_MODEL_SMALL`), called over plain HTTP in `markr/llm.py`.
- Prompts: `prompts/extract_requirements_v2.txt` and `prompts/check_draft_v1.txt`.
- If a call fails (429, 5xx, timeout), Markr waits and tries again up to 3 times (45 second timeout each). If it still fails, you get a message on screen.

## 6. Evaluation

Only the small M2 experiment exists so far: `results/m2_results.md`. It used 10 made-up briefs, and only 3 of the 10 model calls finished, so the end-to-end product has not been evaluated yet. A proper test (at least 20 cases or 5 test users) comes in M4.

## 7. Limitations, risks, privacy and ethics

- The AI can skip requirements. The quote check catches invented requirements, not missing ones.
- A "met" only proves that the quoted text exists in the draft, not that it really satisfies the rule.
- File format, submission method and deadlines can't be seen in the draft text, so they stay "uncertain".
- Scanned PDFs have no text to read. Paste the text instead.
- The free Gemini tier can be slow or fail (429, 503). Earlier tests had a 31 s median and a 186 s worst latency, longer than the 45 s timeout.
- Your brief and draft are sent to Google. Only use text you are allowed to share, and check Google's free-tier data terms.
- Nothing is saved: results disappear when you reload the page.

## 8. Business case

Not written yet.

## 9. AI tools I used

I used Claude for the M1 and M2 write-ups, the test briefs and the first experiment script. For M3 it suggested the code for the Gemini client, the quote checks and the app, and helped me set up VS Code, git and Python. I typed and ran the code, tested it, and decided what to keep.

## 10. Who did what

Guerras Samy: everything since M2, which means the Streamlit app, the Gemini client with retries, the quote and evidence checks, the two prompts, PDF reading, the tests and the documentation.