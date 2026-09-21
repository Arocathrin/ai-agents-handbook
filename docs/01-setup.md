# Chapter 1: Setup

Goal: Kiro CLI installed and signed in, the project running, the gate passing. Time: 45 minutes, most of it downloads.

## 1. Accounts
1. A GitHub account at github.com. Use your real name. Employers will read this profile.
2. A Kiro account. Go to https://kiro.dev and sign in with GitHub, Google, or an AWS Builder ID. Use your university email if you have one.
3. Check the student programme. After signing in, open your account page. If you see a "You are eligible for Kiro Students" banner, verify. Eligible students get 1,000 credits per month free for a year, with premium models. If your university is not listed, use the "Don't see your school listed?" form at https://kiro.dev/students and carry on with the free tier.
4. Know your budget. The free tier is 50 credits per month, on a limited set of models. A credit is a unit of work per prompt. Simple prompts cost less than one credit, a spec task execution typically costs more than one. New accounts have at times received bonus credits in the first two weeks, so check your account page. Chapter 10 teaches you to spend them well.

## 2. Local tools
- Python 3.11 or newer. `python --version` must print 3.11 or higher. On Windows, install from python.org and tick "Add to PATH".
- Git. Windows: `winget install --id Git.Git -e`. macOS: `xcode-select --install`. Linux: your package manager.
- Windows only: Windows Terminal, preinstalled on Windows 11. Do not use `cmd.exe` for Kiro CLI, use PowerShell inside Windows Terminal.

## 3. Install Kiro CLI
Copy the install command for your platform from https://kiro.dev/downloads (CLI tab). As of September 2026:
- macOS or Linux: a one-line `curl ... | bash` installer from cli.kiro.dev.
- Windows 11: a one-line PowerShell installer from cli.kiro.dev. Requires Windows 11. Run it in Windows Terminal or PowerShell, not Command Prompt.
- Windows 10: the CLI is not supported natively. Either install WSL2 (`wsl --install`, reboot, then follow the Linux steps inside Ubuntu) or use the Kiro IDE, which supports Windows 10 and has the same specs, steering, hooks, and permissions. The exercises work in both. The handbook assumes the CLI.

Close and reopen the terminal, then:
```
kiro-cli --version
kiro-cli login
kiro-cli doctor
```
`login` opens a browser. If the browser cannot open, run `kiro-cli login` again and pick the device-code option, then complete it on any browser. `doctor` should print "Everything looks good".

## 4. Get the project
1. On GitHub, open the handbook repository your instructor shared and press **Use this template**, then **Create a new repository**. Name it `ai-agents-handbook`. Make it **public** (branch protection is free on public repos).
2. Clone your copy and set it up:
```
git clone https://github.com/<your-username>/ai-agents-handbook.git
cd ai-agents-handbook
python -m venv .venv
.venv\Scripts\activate           # Windows PowerShell
source .venv/bin/activate        # macOS, Linux, WSL
python -m pip install -e ".[dev]"
python scripts/verify.py
```
The last command must end with `VERIFY PASS`. This is the gate you will use all week.

3. Try the app:
```
python -m ledgerlite.cli --ledger demo.json add --day 2026-04-02 --category food --amount 120.50
python -m ledgerlite.cli --ledger demo.json list
python -m ledgerlite.cli --ledger demo.json report --year 2026 --month 4
```

## 5. First contact with the agent
Inside the repo folder, with the venv active:
```
kiro-cli
```
The terminal UI opens. Type:
```
/guide
```
and ask: `What steering files and hooks does this project have, and what do they do?` Read the answer. Press `Shift+Tab` to leave the guide. Type `/context` and note the token count. Type `/chat new` to start clean, then `/quit`.

## Check
- [ ] `kiro-cli doctor` is clean
- [ ] `python scripts/verify.py` prints `VERIFY PASS`
- [ ] Your fork exists on GitHub and `git remote -v` points to it
- [ ] `/guide` answered a question about this project

## Reflect
What did `/context` show was loaded before you typed anything? Where did it come from?

## Common failures
- `kiro-cli` not found after install: close the terminal and open a new one. PATH updates need a new shell.
- `login` loops: run `kiro-cli login` and choose the device-code flow.
- `pip install` fails on Windows with a long path error: move the repo to `C:\dev\ai-agents-handbook`.
- Windows says scripts are disabled: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
