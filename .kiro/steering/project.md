---
inclusion: always
---

# Project steering (always loaded)

Read and obey the repo instruction file:

#[[file:AGENTS.md]]

Hard rules that apply in every session:
- The only acceptance gate is `python scripts/verify.py` printing `VERIFY PASS`.
- Never make network calls from this repo. There is no reason for one.
- Never write secrets, tokens, or keys into any file.
- Do not touch files outside the task you were given. If you think you must, stop and say why.
- When you finish a task, report: files changed, tests added, verify result.
