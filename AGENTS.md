# AGENTS.md

This is the portable instruction file for any coding agent that opens this repo. Kiro loads it through `.kiro/steering/project.md`. Chapter 4 of the handbook asks you to complete the TODO sections. Every line must be true and checkable.

## What this is
`ledgerlite` is a tiny personal expense ledger: a Python library in `src/ledgerlite/` and a CLI (`ledgerlite add | list | report`). Entries live in a JSON file with a schema version. Amounts are `Decimal`, never `float`.

## Commands
- Install: `python -m pip install -e ".[dev]"`
- Verify (lint plus tests, the only gate that matters): `python scripts/verify.py`
- Run: `python -m ledgerlite.cli --ledger demo.json add --category food --amount 120.50`

## Conventions
<!-- TODO (Chapter 4): code layout, naming, where tests go, formatting, commit message style -->

## Definition of done
<!-- TODO (Chapter 4): what must be true before a task is finished. Hint: verify passes, tests added for new behaviour, no unrelated files touched -->

## Never do
<!-- TODO (Chapter 4): actions the agent must refuse or ask about first. Hint: network calls, schema edits without a migration, deleting tests, force pushes -->

## Schema changes
Any change to `Entry` fields or the JSON layout must follow the `ledgerlite-migration` skill in `.kiro/skills/`.
