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
