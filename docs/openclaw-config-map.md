# OpenClaw Config Map

Canonical global config directory: `~/.openclaw/`

## Files and purposes

### `~/.openclaw/.env`
Secrets only.
- API keys
- should be a real file, not a symlink
- should have `600` permissions

### `~/.openclaw/openclaw.json`
Main OpenClaw configuration.
- workspace path
- channels
- agents
- models
- tool policy
- hooks

### `~/.openclaw/exec-approvals.json`
Exec approval policy.
- approval mode
- allowlists / security levels
- should not be confused with model or channel config

### `~/.openclaw/workspace-state.json`
Workspace bootstrap / local state marker.
- runtime metadata
- not a user-authored config file

### `~/.openclaw/logs/`
Runtime logs.
- debugging only
- not canonical config

### `~/.openclaw/agents/`
Agent-specific working config and cached auth state.
- `auth-profiles.json` may contain OAuth / cached credentials managed by OpenClaw
- `models.json` may reference env vars or provider settings
- avoid editing these casually unless debugging a specific agent issue

## Canonical rule sources
- Workspace behavior → `/Volumes/WorkData/ctbzai/AGENTS.md`
- Long-term memory → `/Volumes/WorkData/ctbzai/MEMORY.md`
- Directory definitions → `/Volumes/WorkData/ctbzai/docs/workspace-map.md`
- Website deployment rules → `/Volumes/WorkData/ctbzai/projects/caotaibanzi-media/DEPLOYMENT.md`

## Rule
Do not invent parallel config files if a canonical config file already exists for the same purpose.
