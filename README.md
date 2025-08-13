# Task Tracker (CLI, Python)

A tiny dependency-free command-line task tracker that stores tasks in `tasks.json` in the **current working directory**.  
Implements the Roadmap.sh (https://roadmap.sh/projects/task-tracker) spec: add, update, delete, mark in-progress/done, and list by status — using only the Python standard library.

---

## Features

- **Add** tasks with descriptions
- **List** all tasks or filter by status (`todo`, `in-progress`, `done`)
- **Update** a task’s description
- **Delete** tasks by id
- **Mark** tasks as `in-progress` or `done`
- **Human-readable JSON** storage in `tasks.json` (created on first run)
- **UTC timestamps** for creation and updates

---

## Requirements

- **Python 3.10+** (uses modern typing like `str | None`)
- Works on **Windows (PowerShell / CMD)**, macOS, and Linux

---

## Getting Started

1. Create a folder and drop in `task.py` (the CLI script you already have).
2. Open a terminal **in that folder**.
3. Run commands with:
   ```powershell
   python task.py <command> [options]
   ```

> Tip (Windows): make a quick alias in PowerShell for convenience:
> ```powershell
> Set-Alias task "python $PWD	ask.py"
> task add "Try aliases"
> ```

---

## Usage

### Commands

| Command | Syntax | What it does |
|---|---|---|
| **add** | `python task.py add "<description>"` | Adds a new task (status = `todo`) |
| **list** | `python task.py list` <br> `python task.py list todo` <br> `python task.py list --status done` | Lists all tasks, or only by a given status |
| **update** | `python task.py update <id> "<new description>"` | Changes a task’s description |
| **delete** | `python task.py delete <id>` | Removes a task |
| **mark-in-progress** | `python task.py mark-in-progress <id>` | Sets status to `in-progress` |
| **mark-done** | `python task.py mark-done <id>` | Sets status to `done` |

### Examples

```powershell
# Add a couple of tasks
python task.py add "Refactor auth flow"
python task.py add "Write docs"

# List everything
python task.py list
#   1 | todo        | Refactor auth flow
#   2 | todo        | Write docs

# Update description
python task.py update 1 "Refactor login/auth flow"

# Move through statuses
python task.py mark-in-progress 1
python task.py mark-done 1

# Filtered listing (positional or --status both work)
python task.py list done
python task.py list --status todo

# Delete by id
python task.py delete 2
```

---

## Data Model

All data lives in a single JSON file in your current directory:

`tasks.json`
```json
{
  "next_id": 3,
  "tasks": [
    {
      "id": 1,
      "description": "Refactor login/auth flow",
      "status": "done",
      "createdAt": "2025-08-13T19:12:00Z",
      "updatedAt": "2025-08-13T19:20:45Z"
    },
    {
      "id": 2,
      "description": "Write docs",
      "status": "todo",
      "createdAt": "2025-08-13T19:13:10Z",
      "updatedAt": null
    }
  ]
}
```

- `next_id` is incremented on each `add` (no scanning required).
- `status` is always one of: `todo`, `in-progress`, `done`.
- Timestamps are stored in **UTC** ISO-8601 with a trailing `Z`.

---

## Error Handling & Exit Codes

- Missing or wrong IDs → prints an error like `Task with id 7 not found.` and exits with **code 1**.
- Invalid status filter → prints `Status must be one of: todo, in-progress, done.` and exits with **code 1**.
- Corrupt `tasks.json` → friendly message and exit **code 1** (so you can script around it).
- Success paths return **code 0**.

> Resetting the store: delete or rename `tasks.json` to start fresh.

---

## Design Notes

- **No dependencies**; just `argparse`, `json`, `pathlib`, `datetime`.
- **One file** by design — ideal for learning and quick scripting.
- **Linear search** on tasks is fine for small lists; keeps code simple and readable.
- **Readable output**: `id | status | description` is easy to parse by eye or with tools.

---

## Quick Test Script (manual “smoke test”)

Run these lines in a new folder:

```powershell
python task.py add "Buy milk"
python task.py add "Write README"
python task.py list
python task.py update 1 "Buy whole milk"
python task.py mark-in-progress 1
python task.py mark-done 1
python task.py delete 2
python task.py list
python task.py list done
```

You should see confirmations after each command and filtered lists matching the current state.

---

## Making It Globally Runnable (Optional)

**Windows (PowerShell):**
1. Create a wrapper `task.ps1` somewhere on your `PATH`:
   ```powershell
   param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
   python "C:\path	o	ask.py" @Args
   ```
2. Ensure script execution is allowed: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**Cross-platform:**
- Use `pyinstaller` to build a single binary:
  ```bash
  pyinstaller --onefile task.py
  # dist/task (or task.exe on Windows)
  ```

---

## Roadmap / Nice-to-Haves

- Edit tasks interactively (`task edit <id>` opening your $EDITOR)
- Natural status toggles (`task start <id>`, `task done <id>`, `task reopen <id>`)
- Sort and formatting flags (`--sort status|created`, `--json` output)
- File locking for concurrent usage
- Unit tests with `pytest`

---

## License

MIT — do whatever you want, just don’t blame me if it breaks 😄
