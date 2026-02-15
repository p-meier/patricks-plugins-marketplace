---
name: research:export
description: Export research findings to Excel, Word, PDF, or PowerPoint
arguments:
  - name: project
    description: Project slug
    required: true
  - name: format
    description: "Export format: xlsx, docx, pdf, pptx (default: docx)"
    required: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

Export research findings to a document format.

## Process

### Step 1: Load Research

Read from `research/$ARGUMENTS/`:
- RESEARCH.md (question, scope)
- THESES.md (validated theses)
- SOURCES.md (source registry)
- synthesis/meta-principles.md
- synthesis/findings.md
- synthesis/categories.md (if exists)
- synthesis/decision-guide.md (if exists)

### Step 2: Determine Format

From $ARGUMENTS or default to docx:
- **xlsx** — Use xlsx skill for data tables and comparison matrices
- **docx** — Use docx skill for formatted report document
- **pdf** — Use pdf skill for final PDF deliverable
- **pptx** — Use pptx skill for presentation deck

### Step 3: Generate

Use the report-generation skill to structure the content, then the appropriate document skill to create the file.

Save to `research/{project}/exports/{filename}.{ext}`

### Step 4: Confirm

Show: "Report exported to research/{project}/exports/{filename}. Open it?"
