# OpenClaw Healthcheck

Quick post-upgrade / post-maintenance checklist.

## 1. Workspace
- `~/.openclaw/workspace` should point to `/Volumes/WorkData/ctbzai`
- `~/.openclaw/openclaw.json` workspace should also point to `/Volumes/WorkData/ctbzai/`

## 2. Secrets
- `~/.openclaw/.env` exists
- `~/.openclaw/.env` is a real file (not symlink)
- `~/.openclaw/.env` permissions should be `600`

## 3. Memory bootstrap files
These should exist only in the main workspace root:
- `AGENTS.md`
- `MEMORY.md`
- `SOUL.md`
- `USER.md`
- `HEARTBEAT.md`
- `TOOLS.md`

## 4. Memory freshness
- `memory/YYYY-MM-DD.md` exists for today
- `MEMORY.md` contains durable rules only
- project-specific details are stored in project memory files when possible

## 5. Model config
- Main/default primary model is `minimax/MiniMax-M2.7`
- Kimi is available but not in fallback lists unless explicitly desired

## 6. Exec approvals
- `~/.openclaw/exec-approvals.json` should be valid JSON
- expected relaxed config:
  - `defaults.security = "full"`
  - `defaults.ask = "off"`
  - `agents.main.security = "full"`
  - `agents.main.ask = "off"`

## 7. Logs
Check:
```bash
tail -50 ~/.openclaw/logs/gateway.err.log
```
Watch for:
- repeated `token_mismatch`
- repeated `tools.allow allowlist contains unknown entries`
- repeated `Provide a command to start. raw_params={"command":""}`

## 8. Website deployment sanity
If touching `caotaibanzi-media`:
- logo is PNG
- hero image is compressed
- homepage latest entries are intact
- deploy with Wrangler, then verify public URL
