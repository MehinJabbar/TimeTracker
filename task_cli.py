#!/usr/bin/env python3

import sys
import os
import json
from datetime import datetime

FILE_PATH = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def handle_add(description):
    if not description.strip():
        print("Error: Task description cannot be empty.")
        return

    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    now = datetime.now().isoformat()

    new_task = {
        "id": new_id,
        "description": description.strip(),
        "status": "todo",
        "createdAt": now,
        "updatedAt": now,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")


def handle_delete(task_id_str):
    if not task_id_str.isdigit():
        print("Error: Task ID must be a valid number.")
        return

    tasks = load_tasks()
    task_id = int(task_id_str)
    filtered_tasks = [t for t in tasks if t["id"] != task_id]

    if len(filtered_tasks) == len(tasks):
        print(f"Error: Task with ID {task_id} not found.")
        return

    save_tasks(filtered_tasks)
    print(f"Task {task_id} deleted successfully.")


def handle_update(id_str, desc):
    if not id_str.isdigit():
        print("Error: Task ID must be a valid number.")
        return

    if not desc.strip():
        print("Error: Task description cannot be empty.")
        return

    task_id = int(id_str)
    tasks = load_tasks()

    for t in tasks:
        if t["id"] == task_id:
            t["description"] = desc.strip()
            t["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task updated successfully (ID: {task_id})")
            return

    print(f"Error: Task with ID {task_id} not found.")


def handle_mark_status(id_str, new_status):
    if not id_str.isdigit():
        print("Error: Task ID must be a valid number.")
        return

    task_id = int(id_str)
    tasks = load_tasks()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = new_status
            t["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task status updated to '{new_status}' successfully (ID: {task_id})")
            return

    print(f"Error: Task with ID {task_id} not found.")


def handle_list(status_filter=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    if status_filter:
        status_filter = status_filter.lower().replace(" ", "-")
        valid_statuses = ["todo", "in-progress", "done"]
        if status_filter not in valid_statuses:
            print(f"Error: Invalid status '{status_filter}'. Use: todo, in-progress, or done.")
            return

    matching_tasks = [
        t for t in tasks
        if status_filter is None or t.get("status") == status_filter
    ]

    if not matching_tasks:
        label = f" with status '{status_filter}'" if status_filter else ""
        print(f"No tasks found{label}.")
        return

    for t in matching_tasks:
        desc = t.get("description", "")
        status = t.get("status", "unknown")
        updated = t.get("updatedAt", "")
        print(f"[{t['id']}] {desc} (Status: {status}, Updated: {updated})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py <command> [arguments]")
        return

    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print('Error: Missing task description. Usage: python task_cli.py add "<description>"')
            return
        handle_add(sys.argv[2])

    elif command == "delete":
        if len(sys.argv) < 3:
            print('Error: Missing task ID. Usage: python task_cli.py delete "<id>"')
            return
        handle_delete(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 4:
            print('Error: Missing task ID or description. Usage: python task_cli.py update "<id>" "<description>"')
            return
        handle_update(sys.argv[2], sys.argv[3])

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print('Error: Missing task ID. Usage: python task_cli.py mark-in-progress "<id>"')
            return
        handle_mark_status(sys.argv[2], "in-progress")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print('Error: Missing task ID. Usage: python task_cli.py mark-done "<id>"')
            return
        handle_mark_status(sys.argv[2], "done")

    elif command == "list":
        if len(sys.argv) > 2:
            status_arg = " ".join(sys.argv[2:])
            handle_list(status_arg)
        else:
            handle_list()

    else:
        print(f"Error: Unknown command '{command}'")


if __name__ == "__main__":
    main()