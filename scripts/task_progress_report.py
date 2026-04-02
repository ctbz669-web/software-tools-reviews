#!/usr/bin/env python3
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

STATE = Path('/Users/kevin/.openclaw/workspace/.runtime/active-task.json')
OPENCLAW_CONFIG = Path('/Users/kevin/.openclaw/openclaw.json')
CHAT_ID = '605187761'
REPORT_INTERVAL = 300
STALE_INTERVAL = 300


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


def get_bot_token():
    cfg = load_json(OPENCLAW_CONFIG)
    return (((cfg.get('channels') or {}).get('telegram') or {}).get('botToken') or '')


def send_telegram(token: str, text: str):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = urlencode({'chat_id': CHAT_ID, 'text': text}).encode()
    req = Request(url, data=data, method='POST')
    with urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    token = get_bot_token()
    if not token:
        return

    task = load_json(STATE)
    if task.get('status') != 'running':
        return

    now = int(time.time())
    updated_at = int(task.get('updatedAt', 0) or 0)
    last_reported = int(task.get('lastReportedAt', 0) or 0)

    if now - last_reported < REPORT_INTERVAL:
        return

    stale = (now - updated_at) >= STALE_INTERVAL
    name = task.get('name', 'unknown-task')
    progress = task.get('progress', '').strip() or '（尚未填寫進度）'
    next_step = task.get('nextStep', '').strip() or '（尚未填寫下一步）'
    blocked = bool(task.get('blocked', False))

    prefix = '⚠️ 任務可能卡住' if stale or blocked else '⏱ 任務進度回報'
    text = (
        f'{prefix}\n'
        f'任務: {name}\n'
        f'進度: {progress}\n'
        f'下一步: {next_step}'
    )
    send_telegram(token, text)
    task['lastReportedAt'] = now
    save_json(STATE, task)


if __name__ == '__main__':
    main()
