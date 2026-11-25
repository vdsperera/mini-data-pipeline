# Setup: Antigravity and VS Code

## What goes where
| File/folder | Used by | Purpose |
|---|---|---|
| `.agents/rules/` | Antigravity | Always-on and context rules |
| `.agents/workflows/` | Antigravity | Slash commands: /plan-task, /build-step, /debug, /reliability-pass, /write-tests, /final-check, /explain-code |
| `.agents/skills/automation-exam/` | Antigravity | Skill the agent loads when the task matches |
| `AGENTS.md` | Antigravity and other agent tools | One-file version of all rules |
| `.github/copilot-instructions.md` | VS Code with GitHub Copilot | Same rules for Copilot Chat |
| `starter/` | You | Tested skeleton project |

Antigravity now uses `.agents/` (older versions used `.agent/`; if your version doesn't see the rules, rename the folder to `.agent`). Do not put `.agents/` in `.gitignore`, or Antigravity won't index it.

## Setup (10 minutes)
1. Unzip. Create a practice folder, e.g. `my-practice`.
2. Copy into it: everything inside `starter/`, the `.agents/` folder, `AGENTS.md`, and `.github/`. (Hidden folders: show hidden files in your file explorer.)
3. Open `my-practice` in Antigravity (File > Open Folder).
4. Terminal: create a venv, `pip install -r requirements.txt`, `pytest -q` (expect 5 passed).
5. Check the rules loaded: open the agent panel, "..." menu > Customizations > Rules. You should see 5 workspace rules. Open Workflows: you should see the 7 workflows.
6. If a rule's activation shows wrong, click it and set it in the UI: `00-exam-mode` = Always On, `10-python-style` = Glob `**/*.py`, others = Model Decision.

## VS Code with Copilot
Copy `.github/copilot-instructions.md` into the project. Copilot Chat reads it automatically (check Settings > search "instruction files" if it doesn't). For workflows, copy the text of a workflow file and paste it as a prompt.

## How to use in a drill
1. In the agent panel type `/plan-task` and paste the task text in the same message. Read the plan.
2. `/build-step`. Run what it tells you. Check the output yourself.
3. Repeat `/build-step` until the requirements are done.
4. `/debug` + paste the error whenever something breaks.
5. `/reliability-pass`, then `/write-tests`.
6. `/final-check` in the last 15 minutes.
7. `/explain-code` to practise defending your work out loud.

## Antigravity tips
- Planning mode vs Fast mode: use Planning for `/plan-task`, Fast for small steps.
- Review each change before accepting. Never accept code you can't explain.
- Keep terminal command approvals on "ask" so you see what runs.
- If the exam allows a different tool, paste the contents of `AGENTS.md` as your first message.
