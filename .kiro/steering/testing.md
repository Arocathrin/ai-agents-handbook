---
inclusion: fileMatch
fileMatchPattern: "tests/**"
---

# Test conventions (loaded when tests are in play)

- One behaviour per test function, named `test_<behaviour>`.
- Use `tmp_path` for any file. Never write to the repo directory.
- Assert on values, not on "no exception".
- A bug fix starts with a failing test that reproduces the bug. Commit the test before the fix.
- Never weaken or delete an existing assertion to make a change pass. Say so and ask instead.
