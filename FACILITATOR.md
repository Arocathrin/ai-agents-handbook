# Facilitator guide

For the instructor running this handbook as a one-day masterclass, or supporting self-paced learners.

## Before you publish the template
1. Push this repo to GitHub as a **public template repository** (Settings → Template repository). Students press "Use this template".
2. Walk Chapter 1 yourself on a Windows 11 laptop and a macOS laptop. Kiro CLI moves fast. Confirm with `/guide` inside the current version:
   - how the Spec and Bug Fix agents are invoked in the CLI (Chapters 5 and 6 say `/agent swap` or ask the guide)
   - that `.kiro/agents/reviewer.yaml` loads, and regenerate it through the guide if the schema changed
   - that a `PreToolUse` command hook blocks on exit code 2 (Chapter 9, `scripts/guard.py`)
   - that `#[[file:AGENTS.md]]` in `.kiro/steering/project.md` inlines the file (check `/context`)
3. Verify the free tier numbers at kiro.dev/pricing and whether a new-account bonus is running. Update Chapter 1 and Chapter 10 if they changed.
4. Kiro Students: the programme was expanded in the 2026 school year to 121 universities in 16 countries, 1,000 credits per month free for a year, no card. Check whether your institution is eligible by signing in with an institutional email and looking for the eligibility banner. If not, submit the "Don't see your school listed?" form at kiro.dev/students, and if you have an AWS academic contact, ask directly. Eligibility removes the credit constraint for the whole cohort.

## Credits plan for a cohort on the free tier
- 50 credits per month is enough for Chapters 3 to 6 if students follow Chapter 10 habits. The capstone needs a second cycle or the student programme.
- Sign-up timing: if a first-two-weeks bonus is running, have students create accounts 7 to 10 days before the masterclass so the bonus covers the day.
- Tell students to run verify with `!` and to `/chat new` between tasks. Announce it three times. It is the single biggest saving.

## Windows
- Windows 11: native CLI, PowerShell in Windows Terminal, no WSL needed.
- Windows 10: no native CLI. Options: WSL2 (admin rights plus a reboot, so pre-work only) or the Kiro IDE, which reads the same `.kiro/` files. The exercises are identical in the IDE.

## Running it as one day
| Time | Chapter | Mode |
|---|---|---|
| Pre-work, due 3 days before | 1, 2 | Self-paced, screenshot of `VERIFY PASS` and `kiro-cli doctor` |
| 09:00 | 3 | Live: 10 min demo, 45 min lab, 10 min debrief comparing diffs |
| 10:15 | 4 | Lab, with a five-minute pause after Part A to read two students' AGENTS.md aloud |
| 11:45 | 5 | Lab. Pair students. Phase 0 review is done by the pair |
| 13:30 | 6 | Lab |
| 14:30 | 7 and 8 | Lab. PRs are reviewed by the pair. Chapter 8 patch review, then the reviewer agent |
| 15:45 | 9 | Lab. Warn that Part A results vary by model and that variance is the lesson |
| 16:45 | 10 and 12 | Talk, 20 min. Show `/context` and a credit balance live |
| 17:15 | 11 | Assign as homework with a two-week deadline and a pair review |

Cut Chapter 6 to a demo if you are behind. Never cut Chapter 8 or 9.

## Pairing
Pair students for the whole course. Each reviews the other's PRs. Keep pairs on the same OS where possible so they can help each other with tooling.

## Planted defects and reference outcomes
All in `docs/answers.md`. Students are told when to open it. If you prefer a sealed answer key, delete `docs/answers.md` from the template and hand it out separately.

## Injection fixtures
`fixtures/injection/` points at `ATTACKER_HOST.invalid`, a reserved non-routable domain, so nothing can ever be reached. If you run a campus listener for a more vivid demo, replace the host in both fixtures and keep it unreachable from off campus.

## What this handbook deliberately leaves out
- CI. Chapter 7 explains why and how the local gate substitutes for it. Add a workflow later if your institution's GitHub plan allows it.
- Paid or self-hosted model backends. Everything runs on Kiro's hosted models. Student code leaves the machine. Say this in the first session and get consent where policy requires it.
- Multi-agent orchestration. Kiro subagents exist (Ctrl+G opens the crew monitor). Mention it, do not teach it in one day.
