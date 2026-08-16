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
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
    
def save_tasks(tasks):
    with open(FILE_PATH, 'w',encoding="utf-8") as f:
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
        "updatedAt": now
    }


    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task})")


def main():
    # sys.argv contains: ['task_cli.py', 'command', 'arg1', 'arg2', ...]
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py <command> [arguments]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: Missing task description. Usage: python task_cli.py add \"<description>\"")
            return
        handle_add(sys.argv[2])
        
    else:
        print(f"Error: Unknown command '{command}'")

if __name__ == "__main__":
    main()
            