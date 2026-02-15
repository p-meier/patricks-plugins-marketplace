# Deep Researcher

A comprehensive research automation system for Claude Code with specialist agents, iterative analysis, and meta-principle extraction.

## Features

- **Multi-agent research** — 8 specialist agents coordinated by an orchestrator
- **Iterative flow** — Scout → Fetch → Summarize → Synthesize → Repeat until complete
- **Markdown state system** — Visible `research/` folder with STATE.md, THESES.md, SOURCES.md
- **Cost-tiered Perplexity** — Python SDK with 5 cost tiers (search → ask → pro → reason → deep-research)
- **Skills as abstraction** — Agents use skills (web-research, youtube, linkedin), not raw API tools
- **Rate limiting** — Max 5 concurrent external API calls enforced by hooks
- **Auto-setup** — Python venv with perplexityai SDK installed on SessionStart
- **Document export** — Excel, Word, PDF, PowerPoint via document processing skills
- **Resumable sessions** — Full state preservation across sessions

## Quick Start

```bash
# Install plugin
claude --plugin-dir /path/to/deep-research-plugin

# Configure API keys
cp .env.example .env
# Edit .env with your keys

# Start a new research project
/research:new "State of AI Agent Frameworks"

# Resume an existing project
/research:resume enterprise-agent-frameworks

# Check status
/research:status

# Export findings
/research:export enterprise-agent-frameworks docx
```

## Prerequisites

- **Python 3.9+** — For Perplexity SDK (auto-installed in plugin venv on first run)
- **Perplexity API key** — Primary web search (via `perplexityai` Python SDK)
- **Firecrawl API key** + CLI (`npm install -g firecrawl-cli`) — Web scraping, search, crawling
- **Apify API key** — YouTube transcripts, LinkedIn scraping
- **LibreOffice** — For Excel formula recalculation (xlsx skill)

## Architecture

```
User → Commands → Research Orchestrator → Specialist Agents
                                              ↓
                                          Skills Layer
                                    (web-research, youtube, linkedin)
                                              ↓
                                      SDK / MCP / CLI Layer
                          (Perplexity Python SDK, Firecrawl CLI, Apify CLI)
                                              ↓
                                    Hooks: Rate Limiting (max 5 concurrent)
                                           + SessionStart auto-setup
```

## Cost Tiers (Perplexity)

| Command | Model | Cost/Request | Use Case |
|---------|-------|-------------|----------|
| `ask --pro` | sonar-pro | ~$0.05 | **Default.** All research queries. Best quality with citations. |
| `search` | Search API | ~$0.005 | Bulk URL discovery only (raw links without synthesis) |
| `reason` | sonar-reasoning-pro | ~$0.10 | Contradiction analysis, thesis validation |
| `deep-research` | sonar-deep-research | ~$0.50-2+ | Checkpoint only, never automated |

## Agents

| Agent | Expertise | Color |
|-------|-----------|-------|
| **research-orchestrator** | Coordination, state management | Blue |
| **source-scout** | Source discovery and evaluation | Green |
| **company-analyst** | Company due diligence | Yellow |
| **data-analyst** | Quantitative analysis | Cyan |
| **academic-researcher** | Academic papers | Magenta |
| **trend-analyzer** | Pattern identification | Yellow |
| **technical-specialist** | Technical documentation | Red |
| **synthesizer** | Meta-principles, thesis validation | Magenta |

## Research Flow

```
Phase 1: SCOUT → source-scout finds sources → SOURCES.md
    ↓ CHECKPOINT
Phase 2: FETCH → agents download to data/ folder
    ↓
Phase 3: SUMMARIZE → specialists create summaries/ and initial THESES.md
    ↓ CHECKPOINT
Phase 4: SYNTHESIZE → synthesizer creates meta-principles, cross-verifies
    ↓ (loop back to Phase 1 if gaps found)
    ↓ CHECKPOINT
Phase 5: REPORT → generate and export final deliverable
```

## Project Structure

Each research project creates:

```
research/{project-slug}/
├── STATE.md              # Living Memory
├── RESEARCH.md           # Plan, questions, scope
├── THESES.md             # Hypothesis tracking
├── SOURCES.md            # Source registry
├── data/                 # Downloaded raw material
│   ├── articles/
│   ├── transcripts/
│   └── reports/
├── summaries/            # Source summaries
└── synthesis/            # Meta-level insights
    ├── meta-principles.md
    ├── findings.md
    ├── categories.md
    └── decision-guide.md
```

## Configuration

Run `/research:configure` to set:
- Trusted sources per domain (enterprise, small project, personal)
- API rate limits
- Apify actor IDs for YouTube and LinkedIn
- Default research domain
