# Workspace Map

Canonical workspace root: `/Volumes/WorkData/ctbzai/`

## Path discipline
- `read` / `write` / `edit` / `exec` should use **absolute paths by default**
- message / media sending should use **workspace-relative paths by default**
- For tools with strict path rules, follow the tool-specific rule
- Avoid mixing path styles inside one task unless required

## Top-level directories

### `.git`
Git metadata for the main workspace repo.

### `.openclaw`
Workspace-local OpenClaw state if present. Not the main global OpenClaw config location; the canonical global config is `~/.openclaw/`.

### `archived/`
Archived files, old outputs, and historical materials that are no longer active but should be kept for reference.

### `audio-outputs/`
Generated audio outputs such as TTS tests, voice samples, and final audio renders.

### `content-download/`
Downloaded external source material and raw reference inputs.

### `docs/`
Long-form documents, reference docs, healthcheck docs, SOPs, and document-based projects.

### `memory/`
Canonical daily memory files (`YYYY-MM-DD.md`). Raw chronological memory log.

### `archived/legacy-openclaw-workspace/`
Archived legacy OpenClaw workspace materials, outputs, metadata, and recovery history. Not active.
- This replaced the old root-level `openclaw-workspace-legacy/` shell after full archival cleanup.

### `outputs/`
General generated outputs that do not belong to a more specific project directory.
- Use this for broad/generated outputs that are not tied to one dedicated project repo.

### `projects/`
Active project repositories and project-specific working directories.
- Root of `projects/` should avoid loose assets when they belong to a single project.
- Prefer putting legacy one-off assets into a project subdirectory such as `legacy-root-assets/`.

#### GitHub repo directory rules (important)
For Git-tracked project repos, especially `projects/caotaibanzi-media/`:
- `content/daily/` = source diary content (markdown/source layer)
- `site/daily/` = public generated diary pages (published HTML layer)
- `site/assets/` = canonical website assets that Wrangler deploy will publish
- If a path is part of the public website, keep the canonical version in Git before deploy

### `reports/`
Structured reports, summaries, and analysis outputs.

### `review-deliveries/`
Files prepared for review / approval workflows.
- Use for handoff packages waiting for Kevin review/approval.

### `scripts/`
Reusable scripts that belong to the canonical workspace.

### `tmp/`
Temporary working files. Safe to regenerate.
- Should stay small and disposable.
- If a temp file becomes worth keeping, move it to `archived/`, `outputs/`, or a project directory.

### `v13-images/`
Image assets / generated image batches for the v13 workflow.

### `video-projects/`
Video-specific working directories and outputs.
- Use for final or multi-version video deliverables that are not already neatly contained in a dedicated repo/project subdirectory.

## External but canonical paths

### Obsidian daily diary vault
- Path: `/Users/kevin/Library/Mobile Documents/iCloud~md~obsidian/Documents/ctbz-daily/`
- Purpose: internal full-version daily diary archive
- Rule: write Obsidian version first, then derive the public website version

### Website project repo
- Path: `/Volumes/WorkData/ctbzai/projects/caotaibanzi-media/`
- Purpose: Git-tracked public website project
- Key directories:
  - `content/daily/` = source markdown/log layer
  - `site/daily/` = public HTML diary layer
  - `site/assets/` = deployable website assets

## Canonical source-of-truth files
These should be treated as the main versions:
- `AGENTS.md`
- `MEMORY.md`
- `SOUL.md`
- `USER.md`
- `HEARTBEAT.md`
- `TOOLS.md`
- `IDENTITY.md`

## Rules
1. Prefer storing active work in the canonical workspace root or under `projects/`.
2. Do not use `openclaw-workspace-legacy/` as an active workspace.
3. Before deleting any directory or file, read it first and confirm its purpose.
4. If a directory’s purpose changes, update this file.
