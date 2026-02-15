---
name: research:resume
description: Resume an existing research project from its saved state
arguments:
  - name: project
    description: Project slug (folder name under research/)
    required: false
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

Resume an existing research project from its saved state.

## Process

### Step 0: Environment Validation

Run the validation script before anything else. Stop if it returns errors.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh
```

If validation fails with errors (missing PERPLEXITY_API_KEY, broken SDK), tell the user what to fix and stop. Warnings are non-blocking — inform the user but continue.

### Step 1: Find Project

If project slug given via $ARGUMENTS:
- Read `research/$ARGUMENTS/STATE.md`

If no project specified:
- List available projects: `ls research/`
- Show each project's status (read Quick Reference from each STATE.md)
- Ask user which project to resume

### Step 2: Load State

Read and display:

```bash
# Read state files
cat research/$PROJEKT/STATE.md
cat research/$PROJEKT/RESEARCH.md
```

Show the user:
- Current phase and status
- Last activity
- Key findings so far
- Next steps from Resume Instructions

### Step 3: Confirm and Launch

Ask: "Resume from {phase}? Or would you like to adjust the direction?"

If confirmed, launch the orchestrator:

```
Task(
  subagent_type: "deep-researcher:research-orchestrator",
  description: "Resume research project",
  prompt: """
    Resume the research project.
    Project: research/{slug}/

    Read STATE.md for current state and Resume Instructions.
    Continue from where we left off.
    Max 5 concurrent external API calls.

    API Keys are loaded in the environment:
    - PERPLEXITY_API_KEY (for web search via Perplexity)
    {include FIRECRAWL_API_KEY line only if set}
    {include APIFY_API_KEY line only if set}
  """
)
```
