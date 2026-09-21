# Chapter 10: Credits, context, and cost

Goal: get a full course of work out of a free tier, and understand what you are paying for. Time: 30 minutes.

## What a credit buys
Kiro meters work in credits. Simple prompts cost a fraction of a credit, a spec task execution usually costs more than one, and premium models burn faster than open-weight ones. The free tier is 50 credits per month with a limited model set. When you hit the cap, requests pause until the cycle resets. Check your balance on your account page and inside the CLI (`/guide how do I see my remaining credits?`).

Professionals treat tokens the way they treat cloud bills: visible, budgeted, and reviewed.

## Habits that cut cost without cutting quality
1. Shell yourself. `!python scripts/verify.py` costs nothing. Asking the agent to "run the tests and tell me" costs a turn plus the output it reads back.
2. One task per session. Context grows every turn and every turn re-reads it. `/chat new` after each committed task is cheaper and cleaner.
3. `/compact` when a session must continue. It summarises history to free context. Do it before the agent starts repeating itself, not after.
4. Plan first. A read-only plan (`Shift+Tab`) is cheap. A wrong implementation is expensive twice: once to write, once to undo.
5. Brief well. Chapter 3 round 1 cost more than round 2 and produced worse code, because the agent explored. Specific briefs are the cheapest optimisation there is.
6. Keep junk out of context. `.kiroignore` in this repo excludes `.venv/` and caches. Add anything large that the agent never needs.
7. Pick the model for the job. `/model` lists what your tier allows. Use the cheaper model for mechanical edits and tests, the stronger one for design and debugging. Reasoning effort, where available, is another dial: low for edits, high for root-cause analysis.
8. Do not let it read everything. `@file` references are precise. "Look at the codebase" is a credit sink.

## Reading `/context`
Run `/context` at the start of a session and after a few turns. It lists the files loaded (steering, skills, referenced files) and a usage percentage. When usage is high, quality drops before the limit is reached. Treat 60 percent as the point to compact or restart.

## Checkpoints and rewind
The CLI checkpoints the workspace as the agent edits. When a run goes wrong, rewinding is cheaper than asking the agent to undo itself. `/guide how do I rewind to a checkpoint?` Git remains the real safety net: commit after every good task.

## Estimating the course
Rough credit costs per chapter on the free tier, as a planning guide, not a promise: Chapter 3, 4 to 8. Chapter 4, 6 to 12. Chapter 5, 10 to 20. Chapter 6, 4 to 8. Chapter 8, 2 to 4. Chapter 9, 2 to 4. Capstone, 10 to 25. If you are on 50 credits, do Chapters 3 to 6 in the first two weeks of your cycle and the capstone after the reset, or verify student eligibility in Chapter 1.

## Do
Run one complete task (any small change) twice: once with a lazy brief and the agent reading "the codebase", once with a precise brief and `@file` references. Note the credit difference from your account page.

## Check
- [ ] You can state your remaining credits
- [ ] You used `!` for every verify run this chapter
- [ ] `.kiroignore` contains at least one addition of your own

## Reflect
`NOTES.md`: what was the credit ratio between the two runs?
