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
