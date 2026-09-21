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
