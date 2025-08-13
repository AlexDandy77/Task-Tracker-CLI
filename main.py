import argparse, json, sys
from pathlib import Path
from datetime import datetime

DB_FILE = Path("tasks.json")

def now_ts():
    return datetime.now().isoformat(timespec="seconds") + "Z"

def load_db():
    if DB_FILE.exists():
        try:
            with DB_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "next_id" not in data or "tasks" not in data:
                raise ValueError
            return data
        except Exception:
            print("Corrupt tasks.json. Rename or delete and try again.", file=sys.stderr)
            sys.exit(1)
    return {"next_id": 1, "tasks": []}

def save_db(db):
    with DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def find_task(db, task_id: int):
    for idx, t in enumerate(db["tasks"]):
        if t["id"] == task_id:
            return idx, t
    print(f"Task with id {task_id} not found.", file=sys.stderr)
    sys.exit(1)

def add_task(description: str):
    db = load_db()
    task = {
        "id": db["next_id"],
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(timespec="seconds") + "Z",
        "updatedAt": None
    }

    db["tasks"].append(task)
    db["next_id"] += 1
    save_db(db)
    print(f"Task added successfully (id: {task["id"]}).")

def list_tasks(status: str | None):
    db = load_db()
    tasks = db["tasks"]
    if status:
        status = status.lower()
        if status not in {"todo", "in-progress", "done"}:
            print("Status must be one of: todo, in-progress, done.", file=sys.stderr)
            sys.exit(1)
        tasks = [t for t in tasks if t["status"] == status]
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        print(f'{t["id"]:>3} | {t["status"]:<11} | {t["description"]}')

def update_task(task_id: int, description: str):
    db = load_db()
    idx, t = find_task(db, task_id)
    t["description"] = description
    t["updatedAt"] = now_ts()
    db["tasks"][idx] = t
    save_db(db)
    print("Task updated successfully.")

def delete_task(task_id: int):
    db = load_db()
    idx, _ = find_task(db, task_id)
    db["tasks"].pop(idx)
    save_db(db)
    print("Task deleted successfully.")

def set_status(task_id: int, new_status: str):
    db = load_db()
    idx, t = find_task(db, task_id)
    t["status"] = new_status
    t["updatedAt"] = now_ts()
    db["tasks"][idx] = t
    save_db(db)
    if new_status == "in-progress":
        print("Task status changed to in-progress.")
    elif new_status == "done":
        print("Task status changed to done.")
    else:
        print("Status updated")

def main():
    parser = argparse.ArgumentParser(prog="task", description="Simple Task Tracker (JSON storage in cwd).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", nargs="+", help="Task description")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=["todo", "in-progress", "done"], help="Filter by status")

    p_update = sub.add_parser("update", help="Update a task's description")
    p_update.add_argument("id", type=int)
    p_update.add_argument("description", nargs="+", help="New description")

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int)

    p_mip = sub.add_parser("mark-in-progress", help="Mark a task in-progress")
    p_mip.add_argument("id", type=int)

    p_md = sub.add_parser("mark-done", help="Mark a task as done")
    p_md.add_argument("id", type=int)

    args = parser.parse_args()

    if args.cmd == "add":
        add_task(" ".join(args.description))
    elif args.cmd == "list":
        list_tasks(args.status)
    elif args.cmd == "update":
        update_task(args.id, " ".join(args.description))
    elif args.cmd == "delete":
        delete_task(args.id)
    elif args.cmd == "mark-in-progress":
        set_status(args.id, "in-progress")
    elif args.cmd == "mark-done":
        set_status(args.id, "done")


if __name__ == '__main__':
    main()