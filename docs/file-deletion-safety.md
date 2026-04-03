# File Deletion Safety

Deletion should be rare, deliberate, and verified.

## Required workflow

### 1. Read before delete
Before deleting any file or directory:
- read the file, or inspect the directory contents
- identify whether it is canonical, duplicate, temporary, or legacy
- check whether the important content has already been merged elsewhere

### 2. Confirm source of truth
Ask:
- Is this the active/canonical version?
- Is there another file that now replaces it?
- Is the replacement already verified?

### 3. Prefer reversible actions
Prefer:
- archive / move
- rename to `*-legacy`
- move to `archived/`

Only hard-delete when:
- content has been read
- content is confirmed obsolete / duplicated
- replacement has been verified

### 4. Verify after change
After deletion / move / rename:
- re-read the surviving canonical file
- verify expected paths still exist
- verify no rule or workflow now points at the removed path

## Red flags
Stop and re-check if:
- the file is a root markdown config (`AGENTS.md`, `MEMORY.md`, `SOUL.md`, etc.)
- the file is referenced by SOPs or workspace-map
- the file is under a Git-tracked project
- the file contains secrets, auth, runtime metadata, or historical memory

## Rule of thumb
**Read before delete. Verify after delete.**
