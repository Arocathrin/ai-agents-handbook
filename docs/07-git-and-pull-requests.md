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
