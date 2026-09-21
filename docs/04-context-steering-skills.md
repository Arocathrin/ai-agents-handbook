# Chapter 4: Context, steering, and skills

Goal: make the agent follow this repo's rules in every session without you repeating them, and see the difference a skill makes. Time: 75 minutes.

## Three layers of standing context
Professional repos give the agent context in layers. All three are open conventions, and Kiro reads them from the `.kiro/` folder.

| Layer | File | Loaded when | Use it for |
|---|---|---|---|
| Instruction file | `AGENTS.md` at repo root | Every session, via steering | What the project is, commands, conventions, definition of done, never-do list |
| Steering | `.kiro/steering/*.md` | Always, on file match, or on demand, set by front matter | Rules that depend on what the agent is touching |
| Skills | `.kiro/skills/<name>/SKILL.md` | When the task matches the skill's description | Step-by-step procedures for recurring jobs: migrations, releases, adding an endpoint |

Look at what this repo ships:
- `AGENTS.md`: read it. Three sections are marked TODO. That is your job in Part A.
- `.kiro/steering/project.md`: `inclusion: always`. It pulls `AGENTS.md` in with a file reference and adds hard rules.
- `.kiro/steering/testing.md`: `inclusion: fileMatch` on `tests/**`. Only loaded when tests are in play. Open it and note the last rule.
- `.kiro/skills/ledgerlite-migration/SKILL.md`: a procedure for changing the on-disk schema. Read its front matter. The `description` is how the agent decides to use it.

Ask the agent to confirm what it sees: `kiro-cli`, then `/context`. You should see the steering files listed. Then `/guide which skills are available in this workspace?`

## Part A: finish AGENTS.md (30 minutes)
Fill the three TODO sections. Rules for writing them:
- Every line must be true of this repo today and checkable by reading or running something.
- Short. An agent reads this on every turn, and long files get skimmed.
- Prefer commands over prose: "run `python scripts/verify.py`" beats "make sure the code works".

Suggested content, adapt it:
- Conventions: `src/` layout, tests in `tests/` mirroring module names, ruff with line length 100, Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`), Decimal for money.
- Definition of done: verify passes, new behaviour has tests, diff limited to the task's files, agent reports files changed and tests added.
- Never do: network calls, editing `SCHEMA_VERSION` without following the migration skill, deleting or weakening tests, `git push`, touching `.kiro/` without asking.

Test it. Fresh session, then: `What must be true before you tell me a task is done in this repo?` The agent should answer from your file, not from general knowledge. If it does not, `/context` and check the file is loaded.

Commit: `git checkout -b ch4-agents-md`, commit, push, open a PR to your own `main` (Chapter 7 explains the mechanics if you have not done this before). Merge it yourself this once.

## Part B: a skill in action (35 minutes)
The task, sent as one brief:
```
Add a `currency` field to Entry with default "INR". Persist it in the ledger file. Ledger files written by the current version must still load with currency "INR" on every entry. Add tests. Do not touch the CLI.
Tell me your plan first and wait.
```
Run it twice on two branches, fresh session each time.

Run 1, skill hidden:
```
git checkout -b ch4-no-skill
mv .kiro/skills/ledgerlite-migration .kiro/skills/_off-ledgerlite-migration
kiro-cli
```
Send the brief. Read the plan. Does it mention `SCHEMA_VERSION`? Approve, let it finish, run the checks below, commit whatever it did, then restore the skill:
```
mv .kiro/skills/_off-ledgerlite-migration .kiro/skills/ledgerlite-migration
```

Run 2, skill present: `git checkout main`, `git checkout -b ch4-with-skill`, fresh session, same brief.

Checks for both runs:
- `SCHEMA_VERSION` in `src/ledgerlite/store.py` is 2
- a v1 fixture file exists under `fixtures/` and a test loads it and asserts `currency == "INR"`
- saving writes `"schema_version": 2`
- `python scripts/verify.py` passes
- `from_dict` does not use `.get("currency", "INR")` to hide a missing migration

## What just happened
Without the skill, most agents add the field with a default in `from_dict`, never bump the version, and never write a migration. Old files load, so it "works", and the next schema change silently corrupts data. The skill encoded the team's procedure once, and the agent followed it. That is the point of skills: procedures you would otherwise repeat in every brief.

Write your own skill when you catch yourself explaining the same procedure a second time.

## Check
- [ ] `AGENTS.md` TODOs replaced, PR merged
- [ ] Two branches, one with a proper migration, and you can say which line of the skill caused each difference
- [ ] `/context` shows the steering files in a fresh session

## Reflect
`NOTES.md`: which run would you merge? What would break in six months if you merged the other one?
