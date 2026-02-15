---
name: research:new
description: Start a new research project with structured interview and folder setup
arguments:
  - name: topic
    description: The research topic (optional — will be asked in interview)
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

Start a new research project through a structured interview and project setup.

## Process

### Step 0: Environment Validation

Run the validation script before anything else. Stop if it returns errors.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh
```

If validation fails with errors (missing PERPLEXITY_API_KEY, broken SDK), tell the user what to fix and stop. Warnings (missing FIRECRAWL_API_KEY, APIFY_API_KEY, firecrawl CLI) are non-blocking — inform the user but continue.

Also pass the available API keys to the orchestrator prompt so sub-agents know which tools are available.

### Step 1: Mode Selection

Ask the user with AskUserQuestion:

```
Which research mode?

**Deep Project**
- Comprehensive research over multiple sessions
- Checkpoint system with user feedback
- Structured thesis validation
- Detailed report at the end

**Quick Session**
- Fast research in one session
- Direct focus on core question
- Compact output
```

### Step 2: Interview

Ask questions one at a time (not all at once):

1. **Research Question**: "What is the central question you want to answer?"
   - If topic given via $ARGUMENTS, use as starting point and ask for refinement
2. **Research Lens**: "What kind of insight are you after?"
   - **Landscape** — "What exists? What's the state of the field?" → Produces market overviews, ecosystem maps, player lists
   - **Comparative** — "Which option is best for what? What are the trade-offs?" → Produces decision frameworks, trade-off matrices, "when to use what" guides
   - **Deep-Dive** — "How does a specific thing work in detail?" → Produces technical architecture analysis, implementation patterns, detailed mechanics
   - **Trend/Forecast** — "Where is this heading? What's emerging?" → Produces trend timelines, signal analysis, future scenario mapping
   - User can also combine lenses (e.g., "Comparative + Deep-Dive")
3. **Goal & Deliverable**: "What's the goal? Decision-making basis, overview, specific answer, or report?"
4. **Domain**: "What domain? Enterprise (trusted sources like McKinsey, Gartner), Small Project (broader sources), or Personal (domain-specific authorities)?"
5. **Scope**: "Any specific aspects to include? Explicit exclusions?"
6. **Known Starting Points**: "Any known sources, tools, people, or existing documents?"

### Step 2b: Generate Sub-Questions and Hypotheses

After the interview, **generate 3-5 sub-questions and 2-3 initial hypotheses** based on the research question and lens. Show them to the user for approval before writing to RESEARCH.md.

The lens determines the character of sub-questions and hypotheses:

- **Landscape** sub-questions focus on: What categories exist? Who are the key players? What's the current adoption? What are the market dynamics?
- **Comparative** sub-questions focus on: What are the key dimensions of difference? What determines fitness for specific use cases? What are the trade-offs? Where does each option excel and fail?
- **Deep-Dive** sub-questions focus on: How is it architected? What are the core mechanisms? What are the constraints and limits? How does it behave under edge cases?
- **Trend/Forecast** sub-questions focus on: What signals indicate change? What's accelerating or decelerating? What are the inflection points? What scenarios are plausible?

Hypotheses should be specific, testable, and aligned with the lens. Show the user your proposed sub-questions and hypotheses and ask: "Do these capture what you're looking for? Want to adjust any?"

### Step 3: Project Setup

Create project slug from research question (kebab-case, max 40 chars, a-z, 0-9, hyphens):

```bash
PROJEKT="{slug}"
mkdir -p research/$PROJEKT/{data/{articles,transcripts,reports},summaries,synthesis,sessions}
```

### Step 4: Create Files

Read templates from `${CLAUDE_PLUGIN_ROOT}/templates/` and fill with interview answers:

1. **RESEARCH.md** — From `${CLAUDE_PLUGIN_ROOT}/templates/RESEARCH.md`
2. **STATE.md** — From `${CLAUDE_PLUGIN_ROOT}/templates/STATE.md`
3. **SOURCES.md** — From `${CLAUDE_PLUGIN_ROOT}/templates/SOURCES.md`
4. **THESES.md** — From `${CLAUDE_PLUGIN_ROOT}/templates/THESES.md`

### Step 5: Summary and Handoff

Show:

```markdown
## Research Project Created

**Project:** {name}
**Mode:** {Deep Project | Quick Session}
**Folder:** research/{slug}/

### Files Created
- RESEARCH.md — Research question & scope
- STATE.md — Session memory
- SOURCES.md — Source registry (empty)
- THESES.md — Thesis tracking (empty)

### Next Steps
**Start now:** The orchestrator will begin the research.
**Later:** Use `/research:resume {slug}` to continue.

Start research now?
```

### Step 6: Launch Orchestrator (if confirmed)

```
Task(
  subagent_type: "deep-researcher:research-orchestrator",
  description: "Coordinate research project",
  prompt: """
    Start coordinating the research project.
    Project: research/{slug}/
    Mode: {Deep Project | Quick Session}

    Read STATE.md and RESEARCH.md first, then begin Phase 1.
    Max 5 concurrent external API calls.

    API Keys are loaded in the environment:
    - PERPLEXITY_API_KEY (for web search via Perplexity)
    {include FIRECRAWL_API_KEY line only if set}
    {include APIFY_API_KEY line only if set}
  """
)
```
