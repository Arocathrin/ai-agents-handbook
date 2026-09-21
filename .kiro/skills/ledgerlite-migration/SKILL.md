---
name: ledgerlite-migration
description: How to change the on-disk ledger schema in this repo. Use whenever a change adds, removes, or renames a field on Entry or alters the JSON file layout.
---

# Ledger schema migration

Invariant: a ledger file written by any earlier version of ledgerlite must load without data loss after the change.

## Steps, in order
1. Bump `SCHEMA_VERSION` in `src/ledgerlite/store.py` by exactly one.
2. Register `MIGRATIONS[<old version>] = <function>` in the same file. The function takes the raw file dict and returns the dict in the new layout. It must be pure and must not read the filesystem.
3. Update `Entry.to_dict` and `Entry.from_dict` in `src/ledgerlite/models.py`. `from_dict` reads required keys directly. Do not paper over a missing key with `.get(..., default)`, that hides a missing migration.
4. Add `fixtures/ledger_v<old>.json`, a real file in the previous layout with at least two entries.
5. Add a test in `tests/test_store.py` that loads the fixture, asserts the migrated values, saves to a temp path, and asserts `schema_version` equals the new value in the written file.
6. Run `python scripts/verify.py`. Do not report done until it prints `VERIFY PASS`.

## Do not
- Change the meaning of an existing key in place. Add a new key and migrate.
- Touch the CLI in the same change unless the task says so.
