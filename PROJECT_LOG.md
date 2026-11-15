# Markr

Markr is a small tool for students. You give it an assignment brief and it makes a checklist of what the brief asks for. Then you give it your draft, and for each item on the list it says whether the draft meets it, misses it, or whether it can't tell.

It only checks. It doesn't write anything for you.

I made it for the Digital Transformation course (BPINFOR-131) at the University of Luxembourg, winter 2026-27.

## 1. What it does

1. Upload or paste a brief (PDF or text).
2. Markr lists the requirements. Under each one it shows the sentence of the brief it came from.
3. Upload or paste your draft.
4. Each requirement is marked met, missing or uncertain. For "met" it shows the part of your draft that backs it up.

The AI suggests the requirements and the verdicts, but plain code checks them. A requirement is dropped if its quote isn't really in the brief. A "met" becomes "uncertain" if its evidence isn't really in the draft. Word and page counts are done by code, never by the AI.

## 2. Users

Students who have several assignments at once and are afraid of missing a rule in one of the briefs. The interviews are in `PROJECT_LOG.md`.

## 3. How to run it

You need Python 3.11 or newer and a Gemini API key.

1. `git clone https://github.com/Guerrassc/Markr.git` and then `cd Markr`
2. `python -m venv .venv`, then activate it (Windows: `.venv\Scripts\activate`, Mac/Linux: `source .venv/bin/activate`)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and paste your key after `GEMINI_API_KEY=`
5. `streamlit run app.py`

The app opens in your browser at `localhost:8501`.

## 4. Architecture

See `docs/architecture.md`.

## 5. AI components

- Model: `gemini-3.5-flash-lite`, set in `.env`.
- Prompts: `prompts/extract_requirements_v2.txt` and `prompts/check_draft_v1.txt`.
- If a call fails, Markr waits and tries again up to 3 times (45 second timeout each). If it still fails, you get a message on screen.

## 6. Evaluation

I only have the small M2 experiment so far: `results/m2_results.md`. It used 10 made-up briefs, and only 3 of the 10 model calls finished. A proper test comes in M4.

## 7. Limitations

- The AI can skip requirements. On the essay test brief it first missed the late penalty, and I only found out by comparing with the brief myself.
- The answers can change a little between runs.
- Scanned PDFs have no text to read, so they don't work. Paste the text instead.
- The free Gemini tier can be slow or fail. Markr retries, but it can still fail.
- Your brief and draft are sent to Google. Only use text you are allowed to share.

## 8. Business case

Not written yet.

## 9. AI tools I used

I used Claude for the M1 and M2 write-ups, the test briefs and the first experiment script. For M3 it suggested the code for the Gemini client, the quote checks and the app, and helped me set up VS Code, git and Python. I typed and ran the code, tested it, and decided what to keep.

## 10. Who did what

I'm working alone, so I did everything else: the interviews, the repository, the experiments, and the tests.