#!/usr/bin/env python3
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

STATE_DIR = Path('/Users/kevin/.openclaw/workspace/.runtime')
STATE_DIR.mkdir(parents=True, exist_ok=True)
PENDING_FILE = STATE_DIR / 'pending-review.json'
NOTIFY_STATE = STATE_DIR / 'pending-work-check.json'
OPENCLAW_CONFIG = Path('/Users/kevin/.openclaw/openclaw.json')
CHAT_ID = '605187761'
MIN_NOTIFY_INTERVAL = 30 * 60


def load_json(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def save_json(path: Path, data):
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

    pending = load_json(PENDING_FILE)
    items = pending.get('pending_items', [])
    sprint = pending.get('sprint', 'unknown')
    state = load_json(NOTIFY_STATE)
    now = int(time.time())
    sig = {'sprint': sprint, 'pending_count': len(items), 'pending_items': items}
    last_sig = state.get('signature')
    last_notify_at = int(state.get('last_notify_at', 0) or 0)

    if not items:
        if last_sig != sig:
            state['signature'] = sig
            state['last_notify_at'] = 0
            save_json(NOTIFY_STATE, state)
        return

    changed = sig != last_sig
    cooldown_ok = now - last_notify_at >= MIN_NOTIFY_INTERVAL

    if changed or cooldown_ok:
        preview = '\n'.join(f'- {x}' for x in items[:5])
        text = f'⏳ 還有工作未完成\nSprint: {sprint}\nPending: {len(items)}\n{preview}'
        send_telegram(token, text)
        state['signature'] = sig
        state['last_notify_at'] = now
        save_json(NOTIFY_STATE, state)


if __name__ == '__main__':
    main()
