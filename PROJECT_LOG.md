# Project log

## M1 - Problem and customer validation (due 2026-10-12; written 2026-10-19)

**Problem.** Every assignment comes with a brief mixing deliverables, deadlines, word limits, formatting rules and marking criteria. Students juggling several courses read it once and sometimes discover at the end that a requirement was missed, which can mean lost marks or extra work. One interviewee said missing a small instruction can cost marks; both said checking takes extra time when several assignments overlap. *[TODO: minutes per assignment, lost marks or redone work, from the follow-up question]*

**Users and customers.** Users: university students, mostly bachelor level. Payers: students (free tier plus a small monthly fee); later universities or student services. Segment: University of Luxembourg 7,200+ students (uni.lu Facts & Figures); 35,615 Luxembourg students received state aid in 2024/25 (Paperjam).

**Interviews (2026-10-19, ~25 min each, consent to note-taking given).**
- Interview A, law student in Montreal (graduation expected 2028): gets instructions via online platforms and PDFs; hard to keep track of all deadlines and requirements; missing a small instruction can cost marks; uses personal notes and calendars; checking takes extra time when several assignments are due. *[TODO: follow-up on time spent, lost marks, paid help]*
- Interview B, law student in Luxembourg (graduation expected 2028): instructions come with different rules and deadlines; easy to forget small details; sometimes rereads instructions to check everything is included; uses notes and reminders; checking takes time and an automatic checklist could help. *[TODO: follow-up on time spent, lost marks, paid help]*

**Alternatives.** Do nothing (reread the brief); own checklist or calendar app (deadlines only, no checking); general chatbot (inconsistent, nothing saved, work goes to a third party).

**Value proposition.** For university students juggling several assignments who lose marks to missed requirements, Markr is an assignment-checklist assistant that turns a brief or rubric into a list of every requirement and checks your draft against it in minutes, unlike rereading the brief by hand.

**Why AI.** Briefs have no standard format and many rules are only implied; extracting them and checking a draft needs language understanding that fixed rules cannot provide across layouts.

## M2 - Technology exploration and proposal (due 2026-10-19)

- [x] Repository created; README skeleton in place; public repository
- [x] Two candidate approaches described (regex baseline and LLM; larger LLM listed as an untested candidate)
- [x] Experiment script, instructions and result committed in `experiments/m2_extraction/` and `results/`
- [x] Regex baseline: 50.3% mean recall over 10 synthetic cases
- [x] Small LLM: 100% recall on the 3 completed cases (20 labelled requirements); 7/10 calls did not complete. On the same three cases, regex recall averaged 45.3%
- [x] Chosen provisional approach, three limitations and switch triggers documented in `docs/M2_filled.tex`
- [x] Initial architecture sketch in `docs/architecture.md`
- [x] Cost estimate documented, separating measured extraction tokens from assumed end-to-end tokens
- [x] MVP tasks, owner and dates documented in `docs/M2_filled.tex`

**M2 evidence limitation.** The small-model results are partial because only 3 of 10 API requests completed. The larger candidate was not run. The PDF states these limitations explicitly; do not describe the experiment as a completed 10-case LLM comparison. Cost figures use the price assumptions recorded in the M2 write-up and a planning estimate for the draft-checking stage; verify live provider prices before deployment.
