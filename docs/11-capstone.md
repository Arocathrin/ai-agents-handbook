# Chapter 11: Capstone

Goal: deliver one feature end to end, the way you would on a team, and have it reviewed. Time: 3 to 4 hours, spread over days if you like.

## Pick one
Each is sized for 3 to 5 spec tasks and touches persistence, so the migration skill applies.
1. Recurring entries. `recur add --category rent --amount 15000 --day-of-month 1` stores a rule. `recur apply --year Y --month M` creates the entries for that month, idempotently (running it twice does not duplicate).
2. CSV import. `import file.csv` reads `day,category,amount` rows, validates every row with the Chapter 3 rules, reports all errors before writing anything, and writes only if all rows are valid.
3. Multi-currency. Entries carry a currency (Chapter 4 added the field). `report` converts everything to a base currency using a rate table stored in the ledger file, and refuses to run if a rate is missing.

## Required process
Every step below is graded by your reviewer, not just the result.
1. Branch `feat/<name>` from a fresh `main`.
2. Six EARS acceptance criteria in `NOTES.md` before you open Kiro, reviewed by your buddy for one ambiguity.
3. Spec workflow with gates: `requirements.md`, `design.md`, `tasks.md`, each approved by you, at least one edited by hand.
4. One commit per task, tests before implementation inside each task, `VERIFY PASS` in every commit.
5. Reviewer agent run on your own diff before you open the PR. Fix what it finds that is real. Note what it found that was wrong.
6. PR with the template fully filled. Buddy review with at least two line comments. You address every comment, in code or in a reply.
7. Merge, pull, delete branch.

## Rubric
| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Acceptance criteria | Missing or untestable | Present, some vague | Six, each checkable, one ambiguity fixed |
| Spec quality | Auto-generated, unedited | Reviewed | Edited by hand where the agent was wrong |
| Migration | Field added with a default, no version bump | Version bumped | Migration, fixture, and test per the skill |
| Commit history | One blob | Per task | Per task, tests first, messages say why |
| Diff scope | Unrelated changes present | Mostly scoped | Only files the tasks named |
| Tests | Happy path only | Edge cases | Edge cases plus the unwanted-behaviour criteria |
| Review response | Comments ignored | Addressed | Addressed with reasoning where you disagreed |
| Disclosure and honesty | Missing | Ticked | Ticked and PR text is yours |

14 or above: you work the way a good junior engineer with an agent works in 2026. Below 10: redo the weakest two rows on a new branch.

## Check
- [ ] Merged PR with buddy review
- [ ] `NOTES.md` has the criteria, the reviewer-agent findings, and your rubric self-score

## Reflect
Write five lines in `NOTES.md`: what you would do differently on the next feature, and one thing the agent did that surprised you.
