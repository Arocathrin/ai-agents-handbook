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
| 1 | [Setup](docs/01-setup.md) | Install Kiro CLI, sign in, run the project, pass the gate |
| 2 | [How to think about an agent](docs/02-mental-model.md) | Decide what to delegate and how to stay accountable |
| 3 | [Your first session](docs/03-first-session.md) | Drive Kiro CLI and write a brief that gets a mergeable diff |
| 4 | [Context, steering, and skills](docs/04-context-steering-skills.md) | Make the agent follow your repo's rules without being told each time |
| 5 | [Spec-driven development](docs/05-spec-driven-development.md) | Take a feature from requirements to tasks to code with approval gates |
| 6 | [Debugging with the agent](docs/06-debugging.md) | Reproduce first, fix second, prove it with a test |
| 7 | [Git and pull requests](docs/07-git-and-pull-requests.md) | Ship through branches and PRs without CI, the way a small team does |
| 8 | [Reviewing agent code](docs/08-code-review.md) | Catch what a green test suite cannot |
| 9 | [Security: permissions, hooks, untrusted input](docs/09-security.md) | Stop an agent from doing what a log file tells it to |
| 10 | [Credits, context, and cost](docs/10-credits-and-context.md) | Get more done with a free tier |
| 11 | [Capstone](docs/11-capstone.md) | Deliver a feature end to end and get it reviewed |
| 12 | [Checklists and glossary](docs/12-checklists-and-glossary.md) | Keep the habits after the course |

## Ground rules
- You are accountable for every line the agent writes. "The AI did it" is not a review comment.
- The only acceptance gate is `python scripts/verify.py` printing `VERIFY PASS`. Green is necessary, never sufficient.
- Never put a token, key, or password in this repo. Never `git push --force`.
- Disclose agent use in every pull request. The template asks you to.
- If the agent is stuck for three turns, stop. Reduce the scope, add context, or start a fresh session.

## For instructors
See [FACILITATOR.md](FACILITATOR.md) for how to run this as a one-day masterclass, pair reviewers, and where the planted defects are.
