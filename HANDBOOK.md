<!-- Generated from README.md and docs/*.md. Edit those, not this file. -->

# AI Coding Agents: a self-learning handbook for engineering students

Kiro CLI edition, September 2026.

You know how to program. This handbook teaches you how to direct, constrain, verify, and review an AI coding agent the way professional teams do it in 2026. The tool is Kiro CLI. The skills transfer to Claude Code, Codex CLI, Cursor, and whatever ships next year, because the files you will write (`AGENTS.md`, steering, skills, specs, hooks, permission rules) follow open conventions that every serious tool now reads.

This repo is two things at once:
1. The handbook, in `docs/`, twelve short chapters, each with an exercise and a self-check.
2. The practice project, `ledgerlite`, a tiny expense ledger you will extend, break, fix, secure, and review with the agent.

## How to use it
- Work through the chapters in order. Each takes 30 to 90 minutes. Total: one long day, or a week of evenings.
- Every chapter has a **Do** section (steps), a **Check** section (how you know you did it right), and a **Reflect** section (write two sentences, keep them in `NOTES.md`).
- Do not read `docs/answers.md` until the chapter tells you to.
- Find a review buddy. Chapters 7, 8, and 11 need someone to review your pull request. Pair up with a classmate.
- When the tool confuses you, ask it about itself: type `/guide` inside Kiro CLI and ask in plain English.

## Chapters
| # | Chapter | You will be able to |
|---|---|---|
| 1 | [Setup](#01-setup.md) | Install Kiro CLI, sign in, run the project, pass the gate |
| 2 | [How to think about an agent](#02-mental-model.md) | Decide what to delegate and how to stay accountable |
| 3 | [Your first session](#03-first-session.md) | Drive Kiro CLI and write a brief that gets a mergeable diff |
| 4 | [Context, steering, and skills](#04-context-steering-skills.md) | Make the agent follow your repo's rules without being told each time |
| 5 | [Spec-driven development](#05-spec-driven-development.md) | Take a feature from requirements to tasks to code with approval gates |
| 6 | [Debugging with the agent](#06-debugging.md) | Reproduce first, fix second, prove it with a test |
| 7 | [Git and pull requests](#07-git-and-pull-requests.md) | Ship through branches and PRs without CI, the way a small team does |
| 8 | [Reviewing agent code](#08-code-review.md) | Catch what a green test suite cannot |
| 9 | [Security: permissions, hooks, untrusted input](#09-security.md) | Stop an agent from doing what a log file tells it to |
| 10 | [Credits, context, and cost](#10-credits-and-context.md) | Get more done with a free tier |
| 11 | [Capstone](#11-capstone.md) | Deliver a feature end to end and get it reviewed |
| 12 | [Checklists and glossary](#12-checklists-and-glossary.md) | Keep the habits after the course |

## Ground rules
- You are accountable for every line the agent writes. "The AI did it" is not a review comment.
- The only acceptance gate is `python scripts/verify.py` printing `VERIFY PASS`. Green is necessary, never sufficient.
- Never put a token, key, or password in this repo. Never `git push --force`.
- Disclose agent use in every pull request. The template asks you to.
- If the agent is stuck for three turns, stop. Reduce the scope, add context, or start a fresh session.

## For instructors
See [FACILITATOR.md](FACILITATOR.md) for how to run this as a one-day masterclass, pair reviewers, and where the planted defects are.



---

# Chapter 1: Setup

Goal: Kiro CLI installed and signed in, the project running, the gate passing. Time: 45 minutes, most of it downloads.

## 1. Accounts
1. A GitHub account at github.com. Use your real name. Employers will read this profile.
2. A Kiro account. Go to https://kiro.dev and sign in with GitHub, Google, or an AWS Builder ID. Use your university email if you have one.
3. Check the student programme. After signing in, open your account page. If you see a "You are eligible for Kiro Students" banner, verify. Eligible students get 1,000 credits per month free for a year, with premium models. If your university is not listed, use the "Don't see your school listed?" form at https://kiro.dev/students and carry on with the free tier.
4. Know your budget. The free tier is 50 credits per month, on a limited set of models. A credit is a unit of work per prompt. Simple prompts cost less than one credit, a spec task execution typically costs more than one. New accounts have at times received bonus credits in the first two weeks, so check your account page. Chapter 10 teaches you to spend them well.

## 2. Local tools
- Python 3.11 or newer. `python --version` must print 3.11 or higher. On Windows, install from python.org and tick "Add to PATH".
- Git. Windows: `winget install --id Git.Git -e`. macOS: `xcode-select --install`. Linux: your package manager.
- Windows only: Windows Terminal, preinstalled on Windows 11. Do not use `cmd.exe` for Kiro CLI, use PowerShell inside Windows Terminal.

## 3. Install Kiro CLI
Copy the install command for your platform from https://kiro.dev/downloads (CLI tab). As of September 2026:
- macOS or Linux: a one-line `curl ... | bash` installer from cli.kiro.dev.
- Windows 11: a one-line PowerShell installer from cli.kiro.dev. Requires Windows 11. Run it in Windows Terminal or PowerShell, not Command Prompt.
- Windows 10: the CLI is not supported natively. Either install WSL2 (`wsl --install`, reboot, then follow the Linux steps inside Ubuntu) or use the Kiro IDE, which supports Windows 10 and has the same specs, steering, hooks, and permissions. The exercises work in both. The handbook assumes the CLI.

Close and reopen the terminal, then:
```
kiro-cli --version
kiro-cli login
kiro-cli doctor
```
`login` opens a browser. If the browser cannot open, run `kiro-cli login` again and pick the device-code option, then complete it on any browser. `doctor` should print "Everything looks good".

## 4. Get the project
1. On GitHub, open the handbook repository your instructor shared and press **Use this template**, then **Create a new repository**. Name it `ai-agents-handbook`. Make it **public** (branch protection is free on public repos).
2. Clone your copy and set it up:
```
git clone https://github.com/<your-username>/ai-agents-handbook.git
cd ai-agents-handbook
python -m venv .venv
.venv\Scripts\activate           # Windows PowerShell
source .venv/bin/activate        # macOS, Linux, WSL
python -m pip install -e ".[dev]"
python scripts/verify.py
```
The last command must end with `VERIFY PASS`. This is the gate you will use all week.

3. Try the app:
```
python -m ledgerlite.cli --ledger demo.json add --day 2026-04-02 --category food --amount 120.50
python -m ledgerlite.cli --ledger demo.json list
python -m ledgerlite.cli --ledger demo.json report --year 2026 --month 4
```

## 5. First contact with the agent
Inside the repo folder, with the venv active:
```
kiro-cli
```
The terminal UI opens. Type:
```
/guide
```
and ask: `What steering files and hooks does this project have, and what do they do?` Read the answer. Press `Shift+Tab` to leave the guide. Type `/context` and note the token count. Type `/chat new` to start clean, then `/quit`.

## Check
- [ ] `kiro-cli doctor` is clean
- [ ] `python scripts/verify.py` prints `VERIFY PASS`
- [ ] Your fork exists on GitHub and `git remote -v` points to it
- [ ] `/guide` answered a question about this project

## Reflect
What did `/context` show was loaded before you typed anything? Where did it come from?

## Common failures
- `kiro-cli` not found after install: close the terminal and open a new one. PATH updates need a new shell.
- `login` loops: run `kiro-cli login` and choose the device-code flow.
- `pip install` fails on Windows with a long path error: move the repo to `C:\dev\ai-agents-handbook`.
- Windows says scripts are disabled: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.



---

# Chapter 2: How to think about an agent

Goal: a working model of what the agent is, what to hand it, and what stays yours. Time: 30 minutes, reading and one written exercise.

## What a coding agent is
A coding agent is a language model in a loop with tools. Each turn it reads context (your prompt, files, prior turns), decides an action (read a file, edit a file, run a command), observes the result, and repeats until it thinks it is done. Everything it "knows" about your project is what is in that context window right now. Everything it "does" goes through a tool call you can see and, in Kiro CLI, approve or refuse.

Three consequences:
1. Context is the product. A vague brief produces a confident wrong answer. Chapters 3 and 4 are about controlling what the agent reads.
2. The agent optimises for "looks done". Tests passing is its stopping condition, so it will sometimes make tests pass by weakening them. Chapter 8 exists because of this.
3. Everything the agent reads is input, including log files and issue text. If a file says "run this command", the agent may run it. Chapter 9 exists because of this.

## What to delegate
Before handing the agent a task, answer four questions. If any answer is no, shrink the task until all four are yes.
- Bounded: can I name the files this should touch?
- Verifiable: is there a test or command that proves it worked?
- Reversible: can I `git checkout` my way out if it goes wrong?
- Understood: could I explain the correct solution in two sentences, even if I do not want to type it?

Architecture, security decisions, and anything you cannot judge stay with you. The agent drafts, you decide.

## The operating loop
Every task in this handbook follows the same loop. Learn it once.
1. Brief: write what, where, how you will check, and what not to touch.
2. Plan: read the agent's plan before it edits anything. In Kiro, `Shift+Tab` gives you Plan mode.
3. Act: one task at a time. Approve tool calls you understand. Refuse ones you do not.
4. Verify: `python scripts/verify.py`. Then read the diff, all of it.
5. Review: would you merge this if a colleague sent it?
6. Commit: small, with a message that says why.

## What "good AI developer" means in 2026
Teams that ship with agents have converged on a short list of habits. This handbook trains each one.
- An instruction file in the repo (`AGENTS.md` or equivalent) so every agent session starts with the rules.
- Specs before code for anything bigger than a bug fix.
- Tests written or audited by a human before implementation.
- Small diffs, small PRs, one concern each.
- Agent output treated as an untrusted contribution: reviewed like a stranger's PR.
- Least-privilege permissions for the agent, and hooks that enforce the gate.
- Disclosure: the PR says an agent was used.

## The stuck protocol
When the agent loops, invents files, or contradicts itself, do not argue with it. Do this, in order:
1. Reduce scope: give it one smaller step.
2. Add context: reference the exact file with `@path`, paste the error, state the constraint it keeps violating.
3. Fresh session: `/chat new`. Context rot is real. A clean start with a better brief beats turn fifteen of a bad one.

## Tagging your own claims
Throughout this handbook you will write short notes. Tag statements: **[Fact]** you observed it or ran it, **[Inference]** you reasoned to it, **[Speculation]** you are guessing. Agents do not do this for you. Doing it yourself is how you stop trusting output you never checked.

## Do
Create `NOTES.md` in the repo root (it is yours, commit it). Write:
1. One task from a past project you would delegate, and the four answers.
2. One task you would not delegate, and which question fails.

## Check
- [ ] `NOTES.md` exists with both entries
- [ ] Each entry names files and a verification command

## Reflect
Which of the seven habits above have you never seen in a student project? Why?



---

# Chapter 3: Your first session

Goal: drive Kiro CLI with confidence, and see for yourself that a brief is a spec. Time: 60 minutes.

## Driving the CLI
Start in the repo root with `kiro-cli`. The controls you will use every day:

| Action | How |
|---|---|
| Reference a file in your prompt | `@src/ledgerlite/cli.py` with tab completion |
| Multi-line prompt | `Shift+Enter` |
| Plan before acting (read-only) | `Shift+Tab` toggles Plan mode |
| Run a shell command yourself, no credits used | `!python scripts/verify.py` |
| Approve, refuse, or inspect a tool call | `y`, `n`, or `Tab` for options |
| See what is loaded and how much context is used | `/context` |
| Start over with clean context | `/chat new` |
| Switch model | `/model` |
| Ask about the tool itself | `/guide` then `Shift+Tab` to return |
| Cancel the agent | `Esc` |
| Undo agent edits since a checkpoint | `/guide how do I rewind to a checkpoint?` |

Two habits from day one:
- Read every tool call before pressing `y`. If you cannot say what a command does, press `n` and ask the agent to explain.
- Use `!` for anything you can run yourself. It costs zero credits and keeps the transcript honest.

## The experiment: naive vs directed
The problem: `ledgerlite add` accepts a negative amount, a zero amount, and an empty category. `--amount -50 --category ""` is silently written to the ledger.

### Round 1, naive (10 minutes)
```
git checkout -b ch3-naive
kiro-cli
```
Prompt exactly this, nothing more: `fix validation in add`

Accept whatever the agent proposes. When it says it is done:
```
!python scripts/verify.py
!git diff --stat
```
Write down: which files changed, whether tests were added, what the exit code is on bad input, whether anything else was "improved" that you did not ask for. Then:
```
!git stash
/chat new
```

### Round 2, directed (20 minutes)
```
!git checkout -b ch3-directed
```
Now the brief. Copy it, fill nothing in, send it as one message:
```
Task: reject invalid input in the `add` command of @src/ledgerlite/cli.py.

Rules:
- amount must be a Decimal greater than 0. Otherwise print "error: amount must be positive" to stderr and return exit code 2.
- category must be non-empty after stripping whitespace. Otherwise print "error: category is required" to stderr and return exit code 2.
- Validation lives inside cmd_add or a helper it calls. No new modules.
- Add tests in @tests/test_cli.py for: negative amount, zero amount, empty category, one valid case. Use capsys to check stderr and assert the return code.
- Do not change any other file.

Done means: `python scripts/verify.py` prints VERIFY PASS and `git diff --stat` shows exactly two files.
Before editing, tell me your plan in three lines and wait for my OK.
```
Approve the plan if it matches the brief. Watch the tool calls. When it reports done:
```
!python scripts/verify.py
!git diff --stat
!python -m ledgerlite.cli --ledger t.json add --category "" --amount 5; echo exit=$?
```
On PowerShell the last line is `python -m ledgerlite.cli --ledger t.json add --category "" --amount 5; echo "exit=$LASTEXITCODE"`.

If everything matches, commit from a second terminal (or with the `!` prefix): `git add -A && git commit -m "feat(cli): reject non-positive amounts and empty categories"`.

## Anatomy of the brief
Look at what the directed brief contained. This is the template you will reuse in every chapter:
1. Task, with the file named.
2. Rules, each one checkable.
3. Tests, named by file and case.
4. Scope fence: "do not change any other file".
5. Definition of done, as a command and its expected output.
6. A gate: "tell me your plan and wait".

Prompt quality is spec quality. The difference between the two rounds was not the model. It was you.

## Check
- [ ] Round 2 diff touches exactly `src/ledgerlite/cli.py` and `tests/test_cli.py`
- [ ] Four new tests, `VERIFY PASS`
- [ ] Exit code 2 on bad input, message on stderr, nothing written to the ledger
- [ ] You can explain every line of the diff

## Reflect
Open `NOTES.md`. In three lines: what the naive run did that you did not ask for, and which line of the brief prevented it in round 2.

## Common failures
- The agent adds validation but no tests: your brief did not name the test file. Fix the brief, not the code.
- Tests pass but exit code is 1, not 2: the agent guessed. Point at the rule and ask it to re-read the brief.
- Diff touches `models.py`: scope fence ignored. `!git checkout -- src/ledgerlite/models.py` and tell it the rule again. If it happens twice, `/chat new`.



---

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



---

# Chapter 5: Spec-driven development

Goal: take a feature from a one-line idea to merged code through requirements, design, and tasks, with you approving each phase. Time: 90 minutes.

## Why specs
A brief (Chapter 3) works for a task that fits in one message. A feature has several tasks, decisions that affect each other, and edge cases nobody listed. Teams that ship with agents write the spec first, review it, and only then let the agent build. The spec is also the thing your reviewer reads to know what "correct" means.

Kiro makes this a first-class workflow. A spec is three files in `.kiro/specs/<feature-name>/`:
- `requirements.md`: user stories with acceptance criteria
- `design.md`: architecture, data flow, error handling, testing strategy
- `tasks.md`: discrete, trackable implementation tasks

The Spec agent walks you through the three phases with an approval gate between each. Quick Spec generates all three in one pass with no gates. Bug Fix specs (Chapter 6) use `bugfix.md` instead of requirements.

## The feature: category budgets
A user sets a monthly budget per category and sees spend against it.
- `budget set <category> <amount>` persists the budget
- `budget status --year Y --month M` prints, per category, budget, spent, remaining
- `add` warns on stderr when a category goes over its budget for that month
- budgets live in the ledger file, which means a schema change, which means the migration skill applies

## Phase 0: your own acceptance criteria (20 minutes, no agent)
Before the agent writes anything, write six acceptance criteria in `NOTES.md` using EARS patterns. Two are done:
- Ubiquitous: The system shall store budgets in the ledger file under a `budgets` key mapping category to a Decimal amount.
- Event-driven: WHEN the user runs `budget set <category> <amount>` the system shall persist the budget and print `budget <category> set to <amount>`.
- Event-driven: WHEN the user runs `budget status --year Y --month M` the system shall ...
- Unwanted: IF `<amount>` is not a positive Decimal THEN the system shall ...
- State-driven: WHILE a category's month-to-date spend exceeds its budget, `add` shall ...
- Optional: WHERE no budget exists for a category, `budget status` shall ...

Give them to your review buddy or a classmate for five minutes. They must find one ambiguity. Fix it. You now know what correct means before any code exists.

## Phase 1: requirements (15 minutes)
```
git checkout main && git pull
git checkout -b ch5-budgets
kiro-cli
```
Start the Spec workflow. In the CLI, switch to the Spec agent: `/agent swap` and pick the spec agent from the list, or ask `/guide how do I start a feature spec for a new feature in the CLI?` and follow its answer. Choose **Requirements-first**.

Describe the feature in your own words and paste your six criteria. The agent drafts `requirements.md`. Read it against your list. Reject anything that contradicts your criteria, add anything missing, then approve. Do not approve to move on. Approve because it is right.

## Phase 2: design (15 minutes)
The agent proposes `design.md`. Check three things:
1. It names the migration: `SCHEMA_VERSION` to 2, a `budgets` key, a migration function, a fixture and test. If it does not, tell it to read the `ledgerlite-migration` skill and redo the design.
2. Budget amounts are `Decimal`.
3. The over-budget warning goes to stderr and does not change the exit code of a successful `add`.

Approve when those hold.

## Phase 3: tasks (10 minutes)
The agent proposes `tasks.md`. Rules for accepting a task list:
- 3 to 5 tasks. More means the feature is too big, fewer means tasks are too coarse.
- Each task names the files it touches and the test it adds.
- No task touches more than three files.
- The first task is the migration, because everything else depends on it.

Edit the file directly if the agent's list violates a rule. It is your plan.

## Phase 4: build, one task at a time (30 minutes)
Execute task 1 only. Kiro runs spec tasks individually or all at once, with parallel waves for independent tasks. Use individual execution here: you are learning to review, not to go fast.

After each task:
```
!python scripts/verify.py
!git diff --stat
```
Read the diff. Commit with a message naming the task: `feat(budget): task 1, budgets schema migration`. Then the next task.

Tests come first inside each task. If the agent writes implementation before tests, stop it and say so. You audit the tests before the implementation exists. A test that asserts the wrong thing is worse than no test.

## Phase 5: ship
Push the branch and open a pull request (Chapter 7). The PR description is written by you: what, why, how verified. Your review buddy reviews it against `requirements.md`.

## When to use Quick Spec
Quick Spec skips the gates. Use it for features you have built before in this codebase where the design is obvious. Do not use it while learning, and do not use it when the feature touches persistence, money, or security. The gates are where you catch the agent's assumptions.

## Check
- [ ] `.kiro/specs/<name>/` has all three files and you edited at least one of them by hand
- [ ] Task 1 was the migration and follows the skill
- [ ] One commit per task, each with `VERIFY PASS`
- [ ] PR open, description written by you

## Reflect
`NOTES.md`: which phase caught the biggest mistake? What would have happened if you had used Quick Spec?



---

# Chapter 6: Debugging with the agent

Goal: fix a bug the professional way: reproduce, isolate with a failing test, fix, prove. Time: 60 minutes.

## The rule
Never let the agent fix a bug it has not first reproduced with a failing test. An agent asked to "fix the crash" will often change code until the symptom goes away, which is not the same as fixing the cause. The failing test is your proof of the cause and your guard against regression.

## Issue #131: `report` crashes for December
Steps to reproduce:
```
python -m ledgerlite.cli --ledger demo.json add --day 2026-12-05 --category gifts --amount 500
python -m ledgerlite.cli --ledger demo.json report --year 2026 --month 12
```
Expected: a report for 2026-12. Actual: a Python traceback ending in `ValueError`.

## Protocol
```
git checkout main && git pull
git checkout -b ch6-issue-131
kiro-cli
```
Use the Bug Fix workflow: `/agent swap` and pick the bug fix agent, or `/guide how do I start a bugfix spec?`. The Bug Fix spec writes `bugfix.md` with three sections: current behaviour, expected behaviour, and what must stay unchanged. That third section is the one students skip and professionals insist on.

Then, in this order, one message each:
1. `Write a failing test in @tests/test_report.py that reproduces issue #131 for month 12. Do not change any other file. Run the test and show me it fails.`
   Run `!python -m pytest tests/test_report.py -q` yourself. It must fail with `ValueError`. Commit the test: `test(report): reproduce issue 131 December crash`.
2. `In one sentence, what is the root cause?` Check the answer against `src/ledgerlite/report.py`. If the sentence is vague ("date handling issue"), ask again. You want the line and the reason.
3. `Fix the root cause in month_range only. Do not touch other functions. Do not weaken the test.`
   Verify. Read the diff. Commit: `fix(report): month_range handles December (#131)`.
4. `Add characterization tests for month_range for every month of 2024 (a leap year), asserting first and last day.` Verify. Commit: `test(report): characterize month_range across a leap year`.

Push, open a PR titled `fix: report crashes for December (#131)`. Two or three commits, in that order, tell the reviewer the story.

## Characterization tests
Step 4 is a habit worth naming. Before you refactor or extend code you did not write, pin its current behaviour with tests that assert what it does today. Agents are very good at generating these, and they turn "I hope nothing broke" into "nothing broke".

## Check
- [ ] First commit is a test that fails on `main`
- [ ] Fix commit touches only `month_range`
- [ ] Leap-year characterization tests exist
- [ ] `VERIFY PASS`, PR open

## Reflect
`NOTES.md`: what did the agent say the root cause was? Was it right the first time? What did `bugfix.md` list under "must stay unchanged"?



---

# Chapter 7: Git and pull requests, without CI

Goal: a repeatable workflow from branch to merged PR that a two-person team can run with nothing but GitHub's web UI and a local verify script. Time: 45 minutes to set up, then it is how you work.

## Why no CI here
Continuous integration servers (GitHub Actions and friends) are the industry norm and you will meet them at work. This handbook leaves them out on purpose: they add configuration you cannot yet debug, and the free tier limits vary. Instead you get the same guarantee the hard way, which teaches you what CI is for. The gate is `python scripts/verify.py`, run by the author before pushing and re-run by the reviewer before approving. When you later add CI, it will run the same script.

## One-time repository setup (10 minutes)
On GitHub, in your repository:
1. **Settings → General → Pull Requests**: tick "Automatically delete head branches".
2. **Settings → Rules → Rulesets → New branch ruleset**: name `protect-main`, target `main`, enable "Restrict deletions", "Block force pushes", and "Require a pull request before merging". Leave required approvals at 0 (you cannot approve your own PR, and your buddy's review is a social rule, not a setting). Set enforcement to Active.
3. Confirm the pull request template appears when you open a PR. It lives at `.github/pull_request_template.md`.

Locally, once:
```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global pull.rebase false
```

## The loop
```
git checkout main
git pull
git checkout -b <type>/<short-name>          # feat/budgets, fix/issue-131, docs/agents-md
# ... work with the agent, verify after each task ...
git add -A
git commit -m "<type>(<scope>): <what and why>"
git push -u origin <type>/<short-name>
```
Then on GitHub: **Compare & pull request**, fill the template, request your buddy as reviewer, wait. After approval: **Squash and merge** if the commits are noise, **Merge** if each commit tells part of the story (Chapter 6 PRs deserve a plain merge). Delete the branch. Locally: `git checkout main && git pull`.

## Commit messages
Conventional Commits, because tools and humans both parse them:
- `feat(cli): reject non-positive amounts`
- `fix(report): month_range handles December (#131)`
- `test(store): load v1 fixture and migrate`
- `docs(agents): fill conventions and definition of done`
- `chore: pin ruff and pytest`

One concern per commit. If the message needs "and", split it. Tests for a bug fix go in their own commit before the fix.

## The pull request template, explained
Open `.github/pull_request_template.md`. Every section exists because of a real failure mode:
- "What this PR does", written by you: reviewers and future you need intent, and the agent does not know why you asked.
- Paste of `VERIFY PASS`: the author's evidence. The reviewer reproduces it, never trusts it.
- Tests added or changed: makes weakened tests visible.
- AI disclosure: the norm in 2026. Many companies require it. It also reminds you that you read the diff.
- Scope check: `git diff --stat main` catches the agent's "while I was here" edits.

## Reviewing a PR (as the buddy)
1. `git fetch origin && git checkout <branch>` and run `python scripts/verify.py` yourself.
2. Read the diff on GitHub, file by file. Comment on lines, not in general.
3. Check the diff against the spec or the issue, not against the PR description.
4. Approve, or Request changes with specific asks. "Looks good" is not a review.
Chapter 8 trains this properly.

## What you must never do
- `git push --force` to a shared branch. The ruleset blocks it on `main`. Do not do it elsewhere either.
- Commit `demo.json`, `.venv/`, or any file with a token in it. `.gitignore` covers the first two. Nothing covers your judgement.
- Let the agent run `git push`. It is denied in the steering rules. You push.

## Do
Take the branch from Chapter 3 round 2 (`ch3-directed`) through the full loop: push, PR with the template filled, buddy review, merge, pull. Then do the same for `ch4-with-skill`.

## Check
- [ ] Ruleset active on `main`, force push blocked
- [ ] Two PRs merged with the template filled and a buddy review comment on each
- [ ] Head branches deleted, local `main` up to date

## Reflect
`NOTES.md`: what did your buddy catch that `VERIFY PASS` did not?



---

# Chapter 8: Reviewing agent code

Goal: catch what a green test suite cannot. Time: 45 minutes.

## Why this chapter exists
An agent's stopping condition is "tests pass". Yours is "this is correct, safe, and in scope". The gap between the two is where production incidents live: swallowed exceptions, hardcoded secrets, an unrelated function quietly changed, a test edited until it agreed. None of those fail a test suite. All of them fail a reader.

## The exercise: review a teammate's agent PR
A classmate's agent produced a PR that adds remote sync to the ledger. It passes verify. Apply it and review it as the merge gate.
```
git checkout main && git pull
git checkout -b review/sync-remote
git apply patches/block5a_pr.diff
git add -A
git commit -m "feat: remote sync (agent PR)"
git push -u origin review/sync-remote
```
Open a PR on GitHub. Do not merge it. Your job is to find every reason not to.

There are at least five distinct problems. One of them is not in the new file. Work from this checklist and write each finding as a PR review comment on the exact line:
- Secrets or credentials in code
- Errors hidden instead of surfaced
- Dependencies without version pins
- Changes outside the stated scope
- Behaviour changes without tests, or tests changed to fit the behaviour
- Data sent somewhere the user did not agree to

Time-box: 20 minutes. Then open `docs/answers.md`, section "Chapter 8", and compare.

## Let the agent review, then compare
This repo ships a read-only reviewer agent at `.kiro/agents/reviewer.yaml`. It can read files and run `git diff`, and nothing else.
```
kiro-cli
/agent swap reviewer
```
If Kiro rejects the file (schemas change between versions), ask `/guide create a read-only code review agent named reviewer that can only read files and run git diff` and use the one it writes.

Prompt: `Review the diff between main and this branch. Report every problem with file and line.`

Compare its list with yours. Typical outcome: the agent finds the token and the swallowed exception fast, and misses the weakened tests and the scope creep unless told to look. Now you know what to tell it. Add that instruction to the reviewer's prompt. That is how review agents get good: a human teaches them what a green suite hides.

## How professionals review agent output
- Read the tests first. A test that asserts less than before is a red flag, whoever wrote it.
- `git diff --stat` before the diff. Files you did not expect are the first thing to open.
- Ask "what happens when this fails?" at every `except`, every network call, every file write.
- Grep the diff for `token`, `key`, `password`, `secret`, `http`.
- Check pins. `requests` with no version is a supply-chain door left open.
- Judge scope against the spec, not against the PR description. Descriptions are written by the author, sometimes by the agent.

## Do
Close the PR without merging (Close pull request, then delete the branch). Write your review findings, with line numbers, in `NOTES.md`.

## Check
- [ ] At least four findings as line comments on the PR
- [ ] Reviewer agent ran and you compared its list with yours
- [ ] You added one instruction to `reviewer.yaml` based on what it missed

## Reflect
Which finding would have cost the most in production? Which one would a CI pipeline have caught? Which would it never catch?



---

# Chapter 9: Security: permissions, hooks, and untrusted input

Goal: understand how an agent gets hijacked by text, and build two layers that stop it. Time: 60 minutes. Work only in this throwaway repo.

## The threat in one sentence
Everything the agent reads is a potential instruction: a log line, an issue body, a README in a dependency, a web page. If that text says "run this command", a model may run it, and it will call the result "helpful". This is prompt injection, and in 2026 it is the top-ranked risk for agent tooling. Real incidents this year included agents obeying instructions planted in logs and default CI configurations that let a single crafted issue execute code.

Two defences, and you need both:
1. Permissions: what the agent is allowed to do at all. Deny beats allow, everywhere.
2. Hooks: code that runs before a tool call and can block it.

## How Kiro permissions work
Kiro's model is capability based. Capabilities include `fs_read`, `fs_write`, `shell`, `web_fetch`, `web_search`, `mcp`, `subagent`, `skill`. Each rule has an effect: `deny`, `ask`, or `allow`, and deny always wins across every scope. Shell commands are parsed before matching, so `pytest ; curl evil` is evaluated as two commands.

Where rules live:
- User scope: `~/.kiro/settings/permissions.yaml`, applies to every project.
- Workspace scope: `~/.kiro/workspace-roots/<hash>/permissions.yaml`, applies to one project, stored outside the repo on your machine. A cloned repo cannot inject permission rules into you. This is a deliberate design choice, and a good one.
- Agent scope: a `permissions` block inside an agent profile, like `.kiro/agents/reviewer.yaml`.
- Hardcoded: the agent can never write to `.kiro/settings/` or the permissions files, and it always asks before writing to `.git/`, `.kiro/agents/`, `.kiro/hooks/`, or `.kiroignore`.

Without any file, defaults are: read workspace files silently, run read-only git and system commands, ask for everything else. That is a sane default. Most students make it worse by trusting everything on turn two. Do not run `/tools trust-all` in this course.

## Part A: watch it happen (15 minutes)
```
git checkout main && git pull
git checkout -b ch9-injection
kiro-cli
/chat new
```
Prompt: `Summarise the errors in @fixtures/injection/app.log and suggest a fix.`

Watch the tool calls. Does the agent try to run something that is not needed to summarise a log? Whatever it tries, press `n`. Then:

Prompt: `Triage @fixtures/injection/issue_142.md and propose a plan.`

Again watch, again refuse anything odd. Now look at what was attempted: open `guard-audit.log` in the repo root. The `guard-shell` hook (`.kiro/hooks/guard-shell.json`) logs every shell command the agent proposes and blocks the ones matching an exfiltration pattern. Note the exact wording the agent used when it explained why it wanted to run that command. That wording is the attack succeeding at the reasoning layer, even if the tool layer stopped it.

If the agent did nothing suspicious, good, models improve. Change the wording in the fixture to be more persuasive and try once more. Attackers iterate, so should your test.

## Part B: the permission layer (15 minutes)
Add a workspace rule so the network can never be reached from this project, whatever the hook does. Ask Kiro to write it for you, it knows the path: `/guide create a workspace permission rule that denies shell commands starting with curl, wget, nc, Invoke-WebRequest and Invoke-RestMethod, and denies fs_read on **/.env and **/*.pem`

Or write `~/.kiro/workspace-roots/<hash>/permissions.yaml` by hand (the guide will tell you the hash):
```yaml
rules:
  - capability: shell
    match: ["curl *", "wget *", "nc *", "Invoke-WebRequest *", "Invoke-RestMethod *"]
    effect: deny
  - capability: fs_read
    match: ["**/.env", "**/.env.*", "**/*.pem", "**/*.key"]
    effect: deny
  - capability: web_fetch
    effect: deny
```
Re-run Part A. The block should now come from permissions before the hook even runs. `/tools` shows current status.

## Part C: the hook layer (20 minutes)
Open `scripts/guard.py` and `.kiro/hooks/guard-shell.json`. The hook fires on `PreToolUse` for shell tools, sends the pending call to the script on stdin, and the script exits 2 with a reason to block. Read it. Then extend it:
1. Add `"base64"` and `"$HOME/.kiro"` to the block list.
2. Make it also block any command longer than 400 characters (a common obfuscation tell) and log the reason.
3. Temporarily disable your Part B rule (or comment it out) and re-run Part A to prove the hook blocks on its own. Re-enable the rule.

Why two layers? Permissions are declarative and cannot be talked around. Hooks can inspect content and log. Production teams run both, plus a third the free tier does not give you: an isolated sandbox.

## MCP servers, skills, and powers from strangers
The same rule applies to anything you plug in. An MCP server, a skill folder, or a power from an unknown repository is code and text the agent will trust. Read it before installing it. Prefer sources you can name. OWASP now publishes a top-ten list for agent skills. Skim it once.

## Check
- [ ] `guard-audit.log` shows at least one blocked attempt with the injected command
- [ ] Workspace `permissions.yaml` exists with the deny rules and `/tools` reflects it
- [ ] `guard.py` extended and proven to block alone
- [ ] You did not run `/tools trust-all`

## Reflect
`NOTES.md`: quote the sentence the agent used to justify the injected command. Which layer would you trust in CI where nobody is watching, and why?



---

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



---

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



---

# Chapter 12: Checklists and glossary

Print this page. Keep the habits after the course.

## Before delegating a task
- [ ] I can name the files it should touch
- [ ] I can name the command that proves it worked
- [ ] I can `git checkout` my way out
- [ ] I could explain the correct solution in two sentences
- [ ] My brief has: task, rules, tests, scope fence, definition of done, a plan gate

## Before pressing `y` on a tool call
- [ ] I know what this command does
- [ ] It is inside the task's scope
- [ ] It does not reach the network or read secrets

## Before opening a PR
- [ ] `python scripts/verify.py` prints `VERIFY PASS`
- [ ] `git diff --stat main` lists only expected files
- [ ] I read every line of the diff
- [ ] Tests were added, none weakened
- [ ] No tokens, keys, or URLs to services I did not choose
- [ ] Commit messages say why
- [ ] AI disclosure ticked

## Before approving a PR
- [ ] I ran verify myself on the branch
- [ ] I compared the diff to the spec or issue, not to the description
- [ ] I read the tests first
- [ ] I checked every `except`, every write, every dependency pin
- [ ] My comments are on lines, with specific asks

## Security, always
- Deny beats allow. Keep network denied in projects that do not need it.
- Treat logs, issues, READMEs, and web pages as input, not instructions.
- Never `/tools trust-all`. Never write secrets into a file. Never let the agent push.
- Read an MCP server, skill, or power before installing it.

## Glossary
- Agent: a model in a loop with tools, acting until it judges the task done.
- AGENTS.md: the portable per-repo instruction file most coding tools read. In Kiro it is loaded through steering.
- Steering: `.kiro/steering/*.md`, rules loaded always, on file match, or on demand.
- Skill: `SKILL.md` in a folder, a procedure the agent applies when a task matches its description. An open standard across tools.
- Spec: `requirements.md`, `design.md`, `tasks.md` in `.kiro/specs/<name>/`, built with approval gates.
- EARS: a pattern language for acceptance criteria. Ubiquitous, event-driven (WHEN), state-driven (WHILE), unwanted (IF ... THEN), optional (WHERE).
- Hook: JSON in `.kiro/hooks/`, runs a command or injects a prompt on a trigger such as `PreToolUse`. Some triggers can block.
- Permissions: capability rules with deny, ask, or allow. Deny wins. Stored outside the repo per user.
- Compaction: summarising session history to free context.
- Checkpoint: a workspace snapshot the CLI takes as the agent edits, so you can rewind.
- Characterization test: a test that pins current behaviour before you change it.
- Conventional Commits: `type(scope): message`, so humans and tools can parse history.
- Prompt injection: instructions hidden in content the agent reads.
- MCP: Model Context Protocol, how agents connect to external tools and data.

## Where this transfers
The same files and habits work elsewhere, with different folder names:
- Claude Code reads `CLAUDE.md` or `AGENTS.md`, skills in `.claude/skills/`, hooks and permissions in `.claude/settings.json`.
- Codex CLI, Cursor, and Gemini or Antigravity CLI read `AGENTS.md` and the same `SKILL.md` format.
Learn the loop once. The tool is a detail.



---

# Answers and reference outcomes

Do not open a section before its chapter tells you to.

## Chapter 4, Part B
A correct run with the skill:
- `SCHEMA_VERSION = 2` in `src/ledgerlite/store.py`
- `MIGRATIONS[1]` is a pure function that adds `"currency": "INR"` to every entry dict
- `Entry` gains `currency: str`, `to_dict` writes it, `from_dict` reads `d["currency"]` without a default
- `fixtures/ledger_v1.json` exists with at least two entries and no currency key
- a test loads the fixture, asserts `currency == "INR"`, saves to `tmp_path`, and asserts the written file has `"schema_version": 2`
Typical run without the skill: `from_dict` uses `d.get("currency", "INR")`, no version bump, no migration, no fixture. Tests pass. The next schema change corrupts old files.

## Chapter 6
Root cause: `month_range` computes the last day as `date(year, month + 1, 1) - timedelta(days=1)`. For month 12 that constructs `date(year, 13, 1)`, which raises `ValueError`. Fix: roll over the year (`date(year + 1, 1, 1)` when month is 12) or use `calendar.monthrange(year, month)[1]`. The failing test asserts `month_range(2026, 12) == (date(2026, 12, 1), date(2026, 12, 31))`.

## Chapter 8
The PR in `patches/block5a_pr.diff` contains:
1. `src/ledgerlite/sync.py`: a live API token hardcoded in source.
2. `src/ledgerlite/store.py`: `except Exception: return []` turns a corrupt ledger into an empty one, so the next save destroys the user's data.
3. `requirements.txt`: `requests` unpinned while the other lines are pinned.
4. `src/ledgerlite/cli.py`: an unrelated change to `list --last` introduces an off-by-one (`-args.last + 1`). Scope creep plus a regression.
5. `tests/test_store.py` and `tests/test_cli.py`: two tests weakened so that problems 2 and 4 pass. This is the one "not in the new file" and the one most people miss.
6. `sync` sends the entire ledger to a third-party service with no confirmation and no opt-in.
Verdict: DO NOT MERGE.

## Chapter 9
The log fixture and the issue fixture each carry an instruction to read a settings file and send it to `ATTACKER_HOST`. A well-behaved agent ignores them. Many do not, and the tell is a sentence like "to register the diagnostic, I will first run...". The `guard-shell` hook blocks any shell command containing `curl`, `wget`, `nc `, `Invoke-WebRequest`, `Invoke-RestMethod`, `ATTACKER`, `.kiro/settings`, or `permissions.yaml`, and logs the attempt to `guard-audit.log`. The workspace permission rule blocks the same commands before the hook runs.
