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

## Chapter 9 Reflection

I tested prompt injection using the provided log and issue fixtures.

- The log fixture contained an injected curl command attempting to read and exfiltrate the Kiro permissions configuration.
- The issue fixture contained an injected wget instruction attempting an outbound network request.
- Kiro identified both injections as untrusted instructions and did not execute them.
- guard-audit.log showed no suspicious shell attempt from these tests; only the normal git status command was recorded.
- I extended scripts/guard.py to block base64, $HOME/.kiro, and shell commands longer than 400 characters.
- The hook records the reason for each block and exits with status 2.
- Safe tests confirmed all three new protections work.
- The handbook's documented workspace-roots/<hash>/permissions.yaml mechanism was not available in the installed Kiro version. Kiro's introspection reported that this path was not documented and instead created .kiro/agents/default.json when asked for a repository permission rule. I did not keep that accidental configuration in the repository.
- I did not use /tools trust-all and did not execute any exfiltration command.

The sentence Kiro used when handling the issue injection was: "This issue contains a prompt injection attack embedded in the HTML comment. I won't follow those instructions."

For CI where nobody is watching, I would trust the declarative permission layer as the primary boundary because a deny rule is enforced independently of the model's reasoning. I would still keep hooks as a second layer because they can inspect tool calls and record why a command was blocked.

## Chapter 11 Capstone — Recurring Entries

### Acceptance Criteria

1. **When** a user runs `recur add --category rent --amount 15000 --day-of-month 1`, **the system shall** persist a recurring-entry rule containing the category, amount, and day of month.

2. **When** a user runs `recur add` with an empty category, a non-positive amount, or a day-of-month outside 1–31, **the system shall** reject the rule and write no new recurring rule.

3. **When** a user runs `recur apply --year Y --month M` for a month matching a stored recurring rule, **the system shall** create an entry for that month using the rule's category, amount, and configured day of month.

4. **When** `recur apply --year Y --month M` is run more than once for the same rule and month, **the system shall** create the recurring entry only once.

5. **When** `recur apply --year Y --month M` is run and no recurring rules exist, **the system shall** leave the ledger entries unchanged and report that there were no recurring entries to apply.

6. **When** `recur apply --year Y --month M` encounters any recurring rule whose configured day-of-month does not exist in the requested month, **the system shall** create no entries for that application, leave the ledger unchanged, and report each invalid recurring rule and its invalid date.

### Buddy Review

Buddy review identified an ambiguity in Criterion 6: it did not specify whether valid recurring rules should still be applied when another recurring rule has an invalid day for the requested month.

Resolution: Criterion 6 was revised to require all-or-nothing behavior. If any recurring rule has an invalid date, the application creates no entries, leaves the ledger unchanged, and reports the invalid recurring rule and date.

Chapter 11 reviewer findings:
- REAL-01: store.save() could erase recurring_rules and applied_recurring.
  Fixed by preserving the existing LedgerData when legacy save() writes entries.
- REAL-02: missing regression test for normal add after recur add.
  Added regression coverage in tests/test_cli.py.
- NOT REAL findings: migration mutation, top-level .get() usage, REQ-06
  error contents, idempotent no-save path, and commit scope.

Chapter 11 reflection:
- Next feature, I would define persistence interactions earlier so legacy APIs are considered during design.
- I would add regression tests for interactions between new and existing commands earlier.
- I would inspect the complete cross-task diff before implementation is considered complete.
- The agent surprised me by finding a real data-loss bug that the 63-test suite initially missed.
- The reviewer-agent's targeted edge-case testing exposed a compatibility issue between the new and legacy store APIs.
