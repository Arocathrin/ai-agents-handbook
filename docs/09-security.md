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
