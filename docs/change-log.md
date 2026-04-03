# Change Log

Tracks major workspace / OpenClaw configuration changes and the reason behind them.

## 2026-04-03

### Workspace and memory cleanup
- Changed `~/.openclaw/workspace` symlink to point to `/Volumes/WorkData/ctbzai`
- Merged old and new `MEMORY.md`
- Removed duplicate bootstrap markdown files from the old workspace
- Renamed `openclaw-workspace/` to `openclaw-workspace-legacy/`
- Added `docs/workspace-map.md` and `docs/openclaw-healthcheck.md`
- Cleaned and re-homed legacy memory, projects, outputs, runtime/cache metadata, and review artifacts into `archived/legacy-openclaw-workspace/`
- Migrated non-duplicate legacy local skills into `~/.agents/skills/`
- Removed the root-level `openclaw-workspace-legacy/` directory after preserving recovery materials and a git bundle snapshot

**Reason:** reduce ambiguity and make the canonical workspace/files explicit.

### Secrets standardization
- Moved API key handling to `~/.openclaw/.env`
- Updated config to use `${VAR}` references where applicable

**Reason:** align with official OpenClaw guidance and reduce upgrade risk.

### Model policy
- Switched all agent primary models to `minimax/MiniMax-M2.7`
- Removed Kimi from fallback lists
- Restored Kimi provider/model availability for manual use only

**Reason:** Kimi tool-calling instability, but keep manual access available.

### Daily publishing workflow hardening
- Enforced: Obsidian internal diary first, website public diary second
- Added explicit logo/brand-hero checks before deploy
- Standardized website deploy via Wrangler

**Reason:** prevent drift and avoid repeating diary / asset mistakes.
