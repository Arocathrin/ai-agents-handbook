\# Chapter 2 Notes — Thinking About an Agent



\## 1. Task I Would Delegate



\### Task



Add input validation to the Python expense CLI so that negative amounts are rejected and an empty category is not accepted.



\### Four Questions



\*\*Bounded:\*\* \[Fact] The task can be limited to the expense CLI files and their corresponding tests. The agent should not modify unrelated project files.



\*\*Verifiable:\*\* \[Fact] The change can be verified by running the project's verification command and the relevant tests.



\*\*Reversible:\*\* \[Fact] The changes can be reviewed with `git diff` and reverted using Git if the implementation is incorrect.



\*\*Understood:\*\* \[Fact] I can explain the expected solution: validate the amount before saving the expense and reject invalid or empty input with a clear error message.



\### Files to Touch



\* `src/ledgerlite/cli.py`

\* Relevant test file under `tests/`



\### Verification Command



```powershell

python scripts/verify.py

```



\---



\## 2. Task I Would Not Delegate



\### Task



Decide the security architecture for an AI application that handles sensitive user data.



\### Four Questions



\*\*Bounded:\*\* \[Inference] The implementation could be limited to specific architecture and configuration files, but the decision itself affects the overall system.



\*\*Verifiable:\*\* \[Inference] Individual security tests can verify implementation details, but they cannot by themselves prove that the overall security architecture is appropriate.



\*\*Reversible:\*\* \[Fact] Git can revert implementation changes, but reversing an incorrect security decision does not necessarily undo its consequences.



\*\*Understood:\*\* \[Fact] The final security and architecture decision should remain with me because it requires human judgment about risks, requirements, and trade-offs.



\### Question That Fails



\*\*Understood\*\* — this is a decision I should make myself rather than delegate to the agent.



\### Files to Touch



\* Architecture/security documentation and configuration files only after the design decision is made.



\### Verification Command



```powershell

python scripts/verify.py

```

Chapter 3 Reflection

The naive run added validation/tests for cases I did not explicitly request, including invalid dates and non-numeric amounts, and it chose exit code 1.

The directed brief's exact Rules, named tests, scope fence ("Do not change any other file"), and Definition of Done prevented those guesses in Round 2.

## Chapter 4 Reflection

I would merge the with-skill run because the `ledgerlite-migration` skill gives a precise, repeatable procedure for schema changes.

Both the no-skill and with-skill runs produced a migration that passed verification, but the skill explicitly requires:
- bumping the schema version by exactly one,
- registering a pure migration function,
- using required keys in `Entry.from_dict`,
- adding a real previous-version fixture,
- testing migration and the written schema version,
- and avoiding CLI changes.

If the no-skill approach were merged, a future schema change in 6 months could be implemented inconsistently. An agent might silently use `.get(..., default)` instead of requiring the migration, skip the previous-version fixture/test, or modify unrelated files. The skill preserves the migration procedure as a reusable repository rule.
## Chapter 8 Reflection

I reviewed the remote-sync agent PR and compared my findings with the reviewer agent.

Human review findings:

1. `src/ledgerlite/sync.py:11` — An API token is hardcoded in source code. Credentials should not be committed to the repository.
2. `src/ledgerlite/store.py:43` — `except Exception` hides corrupt or invalid ledger errors by returning an empty ledger.
3. `requirements.txt:3` — `requests` is unpinned, making dependency resolution less reproducible.
4. `src/ledgerlite/cli.py:46` — The `--last` behavior was changed outside the remote-sync scope and now returns one fewer entry than requested.
5. `tests/test_cli.py:21` — The existing test was weakened so the `--last` regression could pass.
6. `src/ledgerlite/sync.py:19-23` — The complete ledger is sent to an external service without explicit user agreement or documented opt-in behavior.
7. `src/ledgerlite/sync.py:19-25` — The new network behavior has no tests covering successful sync, failed responses, or network errors.

The reviewer agent found the hardcoded token, external data transmission, dependency problem, missing sync tests, `--last` regression, and broad exception handling. It also identified the secret remaining in Git history and the missing `requests` declaration in `pyproject.toml`.

The reviewer did not explicitly identify the weakened `test_cli.py` assertion as a separate finding. I updated the reviewer prompt to explicitly compare changed test assertions with their previous behavior and flag tests weakened to accommodate an implementation.

Chapter 8 also exposed the difference between automated verification and human review: `python scripts/verify.py` passed, but the review identified security, privacy, scope, dependency, error-handling, and test-quality problems that the green test suite did not catch.

The remote-sync PR was accidentally merged during the exercise instead of being closed without merging. I did not fabricate a review or pretend that the PR was closed unmerged.
