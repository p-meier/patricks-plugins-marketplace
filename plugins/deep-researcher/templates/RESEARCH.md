# Research: {Project Title}

## Meta

| Field | Value |
|-------|-------|
| **Project ID** | {project-slug} |
| **Created** | {date} |
| **Mode** | {Deep Project\|Quick Session} |
| **Domain** | {enterprise\|small-project\|personal} |
| **Status** | Active |

---

## Research Question

**Central:** {Main research question}

**Sub-Questions:**
1. {Sub-question 1}
2. {Sub-question 2}
3. {Sub-question 3}

---

## Research Lens

**Type:** {Landscape | Comparative | Deep-Dive | Trend/Forecast}

**Angle:** {One sentence describing the specific perspective — e.g., "Compare frameworks by the architectural trade-offs that determine fitness for different task types" or "Map the current ecosystem of tools and their market positions"}

**This lens means agents should:**
- {Lens-specific instruction 1 — e.g., "Evaluate every item against the same dimensions for apples-to-apples comparison"}
- {Lens-specific instruction 2 — e.g., "Produce decision matrices, not just descriptions"}
- {Lens-specific instruction 3 — e.g., "Always state when/why to use and when/why NOT to use"}

---

## Goal & Deliverable

### Primary Goal
{What decision or understanding should result from this research}

### Deliverables
1. {Deliverable 1}
2. {Deliverable 2}
3. {Deliverable 3}

---

## Scope

### In-Scope
{What will be examined}

### Out-of-Scope
{What is explicitly excluded}

### Evaluation Criteria
{How sources and findings will be evaluated}

---

## Trusted Sources (Domain-specific)

{List of trusted sources for this domain, e.g.:}
- McKinsey, Gartner, Forrester (enterprise)
- TechCrunch, Medium, HN (small project)
- WebMD, Mayo Clinic (personal/health)

---

## Known Starting Points

### Sources
- {Known source 1}
- {Known source 2}

### People/Experts
- {Known expert 1}

### Existing Documents
- {Any existing docs to process}

---

## Hypotheses (to validate)

{Generated from the research question + lens during interview. Must be specific and testable.}

### H1: {Title}
> {Hypothesis statement}
> **Lens alignment:** {How this hypothesis connects to the research lens}

### H2: {Title}
> {Hypothesis statement}
> **Lens alignment:** {How this hypothesis connects to the research lens}

---

## Project Structure

```
research/{project-slug}/
├── STATE.md          # Living Memory
├── RESEARCH.md       # This file
├── SOURCES.md        # Source registry
├── THESES.md         # Thesis tracking
├── data/             # Raw downloaded data
│   ├── articles/     # Scraped articles
│   ├── transcripts/  # YouTube transcripts
│   └── reports/      # PDFs and documents
├── summaries/        # Source summaries
└── synthesis/        # Meta-level insights
    ├── meta-principles.md
    ├── findings.md
    ├── categories.md
    └── decision-guide.md
```
