# Markr

Markr turns an assignment brief into a checklist, then checks your draft against it so you don't lose marks to something you missed.
Semester project for Digital Transformation (BPINFOR-131), University of Luxembourg, WS2026-27.

## 1. What it does
You give Markr an assignment brief (PDF or text). It pulls out every requirement (deadlines, word limits, format, referencing, marking weights) as a checklist and checks your draft against it. It only checks your work, it never writes it. *(Status at M2: just the extraction experiment, no product yet.)*

## 2. Users and value proposition
For university students juggling several assignments who lose marks to missed requirements, Markr is an assignment-checklist assistant that turns a brief or rubric into a list of every requirement and checks your draft against it in minutes, unlike rereading the brief by hand or pasting it into a general chatbot and hoping. See `PROJECT_LOG.md` (M1).

## 3. How to run it
Experiment only for now: see `experiments/m2_extraction/README.md` (4 steps).

## 4. Architecture
M2 proposal: see [`docs/architecture.md`](docs/architecture.md) for the initial Mermaid data-flow sketch. It is a proposal, not yet the final architecture of a running product; update it for M3.*

## 5. AI components
- Prompt: `prompts/extract_requirements.txt`
- M2 candidate models: `gemini-3.5-flash-lite` (small; 3/10 calls completed) and `gemini-3.8-flash` (larger; not run). See `results/m2_results.md` and `.env.example`.
- Data: 10 synthetic briefs in `experiments/m2_extraction/cases.json` (written for this project)

## 6. Evaluation
M2 preliminary extraction experiment: `results/m2_results.md`. M4 evaluation is still TODO and must include at least 20 cases or 5 test users, before/after results and three verbatim failure cases.

## 7. Limitations, risks, privacy and ethics
*TODO for final package (at most 250 words). Starting points: briefs and drafts are student work (do not send to third-party AI without consent; check providers' training terms); the tool must check, not write, assignments; extraction can miss implied rules.

## 8. Business case
*TODO (see course brief section 6).*

## 9. AI tools the team used
- Claude: helped draft the M1/M2 write-ups, the 10 test briefs and the first version of the experiment script. *TODO (Samy): add what you changed or checked yourself, and any other tools (Copilot, ChatGPT...) used later.*

## 10. Who did what
| Member | Contribution |
|---|---|
| Samy Cherif Guerras | M1 write-up, M2 repo, experiment and cost estimate *(update as the team contributes)* |
