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

If everything matches, commit: `!git add -A && !git commit -m "feat(cli): reject non-positive amounts and empty categories"` (or run the git commands in a second terminal).

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
