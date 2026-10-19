| approach | model | completed cases | mean recall | items/brief | total input tokens | total output tokens | median latency (s) | worst latency (s) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| rules | regex | 10/10 | 50.3% | 3.7 | 0 | 0 | 0.0 | 0.0 |
| small | gemini-3.5-flash-lite | 3/10 | 100.0% | 10.7 | 591 | 430 | 31.49 | 186.34 |
| large | gemini-3.8-flash | 0/10 (not run/completed) | not measured | not measured | 0 | 0 | not measured | not measured |

## Interpretation

The small model completed the essay, lab and Haskell briefs. It found all 20 labelled requirements in those three cases. On the same three cases, regex recall was 29%, 57% and 50%, respectively (45.3% mean). Across all ten cases, regex mean recall was 50.3%. Seven small-model requests did not complete, so 100% is conditional on the three successful calls and must not be presented as a 10-case result. The larger model has no measured result.

The metric is keyword-based: every annotated key string for a requirement must occur in one extracted line. It can penalise correct paraphrases and may not detect semantic errors. All ten briefs are synthetic. The LLM latency is high (31.49 s median; 186.34 s worst) and availability limited during this run.

Example baseline misses in the essay case: PDF format, Harvard referencing, at least six academic sources, title page/student ID, and late-work penalty. These are specific constraints the regex rules did not extract.

## Three completed LLM sample outputs

These are actual excerpts from the three successful small-model calls in `m2_results.json`, not manually invented outputs. Each case had 100% keyword-scored recall in this run.

### Essay brief

- Write an essay on one cause of the First World War.
- The essay length must be 1500-word (+/-10%).
- Submit the essay as a PDF file.
- Submit via Moodle.
- Submit by Friday 14 November, 23:59.
- … (4 further extracted items are preserved in the JSON result)

**Commentary:** The model returned a multi-item checklist rather than only dates and numeric constraints, and all labelled requirements in this case were matched by the experiment scorer. This is encouraging but not conclusive: there are only three successful calls, and keyword matching is not a human quality review.

### Lab brief

- Complete the assignment as a group of 2 students.
- Write a lab report on the topic of Titration.
- Keep the report length to a maximum of 6 pages excluding the appendix.
- Include an Aim section in the report.
- Include a Method section in the report.
- … (8 further extracted items are preserved in the JSON result)

**Commentary:** The model returned a multi-item checklist rather than only dates and numeric constraints, and all labelled requirements in this case were matched by the experiment scorer. This is encouraging but not conclusive: there are only three successful calls, and keyword matching is not a human quality review.

### Haskell brief

- Implement the functions in Assignment2.hs.
- Do not change the function signatures.
- Use no external packages besides base.
- Submit Assignment2.hs only.
- Do not submit a zip file.
- … (5 further extracted items are preserved in the JSON result)

**Commentary:** The model returned a multi-item checklist rather than only dates and numeric constraints, and all labelled requirements in this case were matched by the experiment scorer. This is encouraging but not conclusive: there are only three successful calls, and keyword matching is not a human quality review.
