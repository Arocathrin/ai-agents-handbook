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
