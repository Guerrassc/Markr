# M2 notes (turn into the one-page PDF)

## 1. Approaches compared
| | A: regex rules (baseline) | B: small LLM | C: large LLM |
|---|---|---|---|
| Output quality (recall, `results/m2_results.md`) | | | |
| Cost per brief (tokens x price) | 0 | | |
| Latency (median / worst) | | | |
| Data needed | none | none (prompt only) | none (prompt only) |
| Failure modes | misses rules without numbers/dates; no wording flexibility | | |
| Switching difficulty / vendor lock-in | none | low (prompt in `prompts/`, plain HTTP client) | low |

## 2. Experiment
`experiments/m2_extraction/` - command and metric in its README. Result: see `results/m2_results.md`. Commentary: *TODO (3 sample outputs or the table plus what surprised you).*

## 3. Chosen approach
*TODO.* Three limitations: *TODO.* What would make us switch: *TODO.*

## 4. Architecture sketch
*TODO: photo of a hand-drawn sketch in this folder.*

## 5. Cost estimate
Provider price list: *TODO link and date.* One action = one brief (about *N* input tokens + *M* output tokens, from `results/m2_results.json`): (N x price_in + M x price_out) / 1,000,000 = *TODO*.

## 6. Plan to MVP (due 2026-11-16)
| Task | Owner | Date |
|---|---|---|
| Accept PDF/text upload and extract text | | |
| Checklist extraction end to end (chosen model) | | |
| Draft-vs-checklist check | | |
| Simple web UI | | |
| 3-minute demo video, bug list | | |
