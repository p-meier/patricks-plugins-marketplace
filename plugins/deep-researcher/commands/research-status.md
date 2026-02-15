---
name: research:status
description: View the current status of a research project
arguments:
  - name: project
    description: Project slug (folder name under research/)
    required: false
allowed-tools:
  - Read
  - Glob
  - Bash
---

Display the current status of a research project.

## Process

### Step 1: Find Project

If project slug given via $ARGUMENTS:
- Use `research/$ARGUMENTS/`

If no project specified:
- List all projects under `research/`
- Show summary status for each

### Step 2: Display Status

Read and present:

1. **Quick Reference** from STATE.md (project, phase, status, last activity)
2. **Progress Tracker** from STATE.md (checklist with completion)
3. **Source Overview** (counts from SOURCES.md)
4. **Thesis Status** (counts from THESES.md)
5. **API Usage** (from STATE.md)

Format as a clear dashboard:

```markdown
## Research Status: {project}

**Phase:** {current phase}
**Status:** {status}
**Last Activity:** {date and description}

### Progress
- Phase 1: Scout Sources {status}
- Phase 2: Fetch & Download {status}
- Phase 3: Summarize & Extract {status}
- Phase 4: Synthesize & Cross-Verify {status}
- Phase 5: Report {status}

### Sources: {found} found, {analyzed} analyzed
### Theses: {total} total ({validated} validated, {open} open, {refuted} refuted)
```
