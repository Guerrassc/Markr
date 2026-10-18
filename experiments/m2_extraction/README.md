# M2 experiment: requirement extraction

Question: how well can each approach turn an assignment brief into a complete checklist?

- `cases.json` - 10 synthetic briefs written for this project (essay, lab, code, presentation, rubric, informal email, French, ...) with labelled requirements. They are not taken from real students' work.
- `run_experiment.py` - compares a regex baseline (`rules`), a cheaper LLM (`small`) and a stronger LLM (`large`).
- Metric: requirement recall (a labelled requirement counts when an extracted line contains all its key strings). Also items per brief, tokens and latency.

Run:
1. `pip install -r requirements.txt`
2. `cp .env.example .env` and fill in a provider, key and the two model names (skip this for the baseline only)
3. `python experiments/m2_extraction/run_experiment.py`
4. Read `results/m2_results.md` and `results/m2_results.json` (per-case misses and every extracted item).

Weak points, honestly: only 10 cases, the keyword matching can miss a correct paraphrase, and the briefs are made up. M4 needs at least 20 cases or 5 test users, so this gets replaced then.
