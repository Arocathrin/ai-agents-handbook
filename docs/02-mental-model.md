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
