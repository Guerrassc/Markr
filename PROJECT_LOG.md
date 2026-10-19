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

- [x] Repository created, README skeleton in place (public)
- [x] Regex baseline measured: 50% mean recall, 3.7 items per brief (`experiments/m2_extraction`)
- [ ] LLM approaches run, results in `results/m2_results.md`
- [ ] Chosen approach, 3 limitations, switch trigger (in the M2 PDF)
- [x] First architecture sketch: `docs/architecture.md`
- [ ] Cost estimate with measured tokens (Groq price list checked 2026-10-19)
- [ ] Plan to MVP (in the M2 PDF)
