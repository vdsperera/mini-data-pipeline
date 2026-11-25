# Exam prep pack (2 hours to go)

## Your 2-hour prep plan (do it in this order)
| Time | Do this |
|---|---|
| 0:00-0:10 | Unzip. Open `starter/` in Antigravity or VS Code. Copy `.agents/`, `AGENTS.md` and `.github/` into it (see ANTIGRAVITY_VSCODE_SETUP.md). Run `pip install -r requirements.txt` and `pytest -q`. Run `python -m src.main api` and `python -m src.main web`. If both work, your environment is ready. |
| 0:10-0:25 | Read `EXAM_PLAYBOOK.md` once. Read the "Prompts to paste" section twice. |
| 0:25-1:10 | **Drill 1** from `PRACTICE_PROJECTS.md` (API). Timed 45 min. Use Cursor, follow the playbook exactly. |
| 1:10-1:15 | Break. Water. |
| 1:15-1:45 | **Drill 2** (Selenium), timed 30 min. Focus only on waits, locators, page objects. |
| 1:45-1:55 | Skim `CHEATSHEET.md`. |
| 1:55-2:00 | Re-read the "First 10 minutes" and "Last 15 minutes" in the playbook. Stop studying. |

If you only have time for one drill, do Drill 1 and skip to the cheat sheet.

## Files
- `.agents/`, `AGENTS.md`, `.github/`: rules, slash-command workflows and skill for Antigravity and VS Code (`.cursor/` is the Cursor version)
- `starter/`: tested skeleton (retry client, state file, page objects, CLI, tests). Copy it into the exam project if allowed.
- `EXAM_PLAYBOOK.md`: minute-by-minute plan, prompts, what to do if AI is restricted, how to defend your code
- `CHEATSHEET.md`: syntax you don't have to memorise
- `PRACTICE_PROJECTS.md`: 4 timed drills with acceptance criteria
