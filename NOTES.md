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



