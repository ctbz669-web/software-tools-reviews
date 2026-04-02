#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path

STATE = Path('/Users/kevin/.openclaw/workspace/.runtime/active-task.json')


def load_json(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('usage: set_active_task.py <name> <status> <progress> <nextStep> [blocked:true|false]')
        sys.exit(1)
    name, status, progress, next_step = sys.argv[1:5]
    blocked = False
    if len(sys.argv) >= 6:
        blocked = sys.argv[5].lower() == 'true'

    state = load_json(STATE)
    state.update({
        'name': name,
        'status': status,
        'updatedAt': int(time.time()),
        'progress': progress,
        'nextStep': next_step,
        'blocked': blocked
    })
    save_json(STATE, state)
    print(json.dumps(state, ensure_ascii=False, indent=2))
