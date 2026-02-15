# Perplexity Python CLI Reference

Wrapper script: `${CLAUDE_PLUGIN_ROOT}/scripts/ppxl` (handles venv internally)

Uses the official `perplexityai` Python SDK (`pip install perplexityai`).

## Cost Tiers

| Command | Model | Cost | Use Case |
|---------|-------|------|----------|
| `ask --pro` | sonar-pro | ~$0.05/req | **DEFAULT.** Best quality with citations. Use for all queries. |
| `search` | Search API | ~$0.005/req | Bulk URL discovery only (when raw links are enough). |
| `ask` | sonar | ~$0.01/req | Rarely. Only if budget is very tight. |
| `reason` | sonar-reasoning-pro | ~$0.10/req | Contradiction analysis, thesis validation. |
| `deep-research` | sonar-deep-research | ~$0.50-2+/req | CHECKPOINT ONLY. Never automated. |

## Global Options

| Option | Description |
|--------|-------------|
| `--output json` / `-o json` | JSON output (default: markdown) |
| `--output markdown` / `-o markdown` | Markdown output |

## Commands

### search

Raw search results from the Perplexity Search API. Cheapest option — use freely.

```bash
PPXL="$CLAUDE_PLUGIN_ROOT/scripts/ppxl"

$PPXL search "query" [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--max-results N` | Number of results (1-20) | 10 |
| `--domains "d1,d2"` | Domain allowlist (comma-separated, max 20) | — |
| `--exclude-domains "d1,d2"` | Domain denylist (comma-separated) | — |
| `--recency PERIOD` | Time filter: `day`, `week`, `month` | — |
| `--language "en,de"` | Language filter ISO 639-1 (comma-separated) | — |
| `--country CODE` | ISO 3166-1 alpha-2 code (US, DE, GB) | — |

#### Domain Filtering

Supports root domains, subdomains, and TLD filtering:

```bash
# Trusted enterprise sources
$PPXL search "AI report" --domains "mckinsey.com,gartner.com,forrester.com,bcg.com"

# Academic only
$PPXL search "machine learning survey" --domains "arxiv.org,nature.com,.edu"

# Government + educational
$PPXL search "AI policy" --domains ".gov,.edu"

# Exclude low-quality
$PPXL search "AI trends" --exclude-domains "pinterest.com,reddit.com,quora.com"
```

**Rules:**
- Domains without protocol: `nature.com` not `https://nature.com`
- Root domain matches all subdomains: `wikipedia.org` matches `en.wikipedia.org`
- TLD filter: `.gov` matches all .gov domains
- Max 20 domains per request
- Allowlist OR denylist, not both in same request

### ask

AI-synthesized answer with web search grounding.

```bash
# Basic (sonar model — cheap)
$PPXL ask "What are the main AI agent frameworks?"

# Pro quality (sonar-pro — moderate cost, better citations)
$PPXL ask --pro "Compare LangChain vs CrewAI for enterprise use"

# With domain filtering
$PPXL ask "Latest AI developments" --recency week --domains "techcrunch.com,theverge.com"
```

| Option | Description |
|--------|-------------|
| `--pro` | Use sonar-pro model (higher quality, more expensive) |
| `--domains` | Domain allowlist |
| `--exclude-domains` | Domain denylist |
| `--recency` | Time filter: `day`, `week`, `month` |

### reason

Complex reasoning and analysis using sonar-reasoning-pro.

```bash
$PPXL reason "Source A claims X while Source B claims Y. Analyze the contradiction."
```

No additional options. Use for:
- Contradiction resolution between sources
- Thesis validation against evidence
- Complex analytical questions requiring step-by-step reasoning

### deep-research

Multi-step deep research using sonar-deep-research. **Very expensive.**

```bash
# Requires --confirm flag (safety guard)
$PPXL deep-research "Comprehensive analysis of topic" --confirm
```

**Safeguards:**
- Without `--confirm`, prints cost warning and exits
- Should NEVER be used in automated loops
- Only the orchestrator should trigger this at explicit checkpoints
- Always get user approval before calling

## Output Formats

### Markdown (default)

```bash
$PPXL search "AI frameworks"
# Output: Human-readable markdown with headers, URLs, snippets

$PPXL ask "What is LangChain?"
# Output: Prose answer with citations section
```

### JSON

```bash
$PPXL -o json search "AI frameworks"
# Output: {"query": "...", "result_count": 10, "results": [{...}]}

$PPXL -o json ask "What is LangChain?"
# Output: {"model": "sonar", "content": "...", "citations": [...]}
```

## Examples by Use Case

### Source Discovery (Phase 1)

```bash
# Broad search
$PPXL search "AI agent frameworks enterprise deployment" --max-results 20

# Domain-specific
$PPXL search "AI report 2025" --domains "mckinsey.com,gartner.com" --recency month

# YouTube content
$PPXL search "site:youtube.com AI agents talk conference" --max-results 10

# LinkedIn profiles
$PPXL search "site:linkedin.com CTO AI startup" --max-results 10
```

### Context Gathering (Phase 2-3)

```bash
# Quick context on a tool
$PPXL ask "What is CrewAI and who are its main competitors?"

# Detailed comparison
$PPXL ask --pro "Compare the architecture approaches of LangChain, CrewAI, and AutoGen"
```

### Synthesis Support (Phase 4)

```bash
# Contradiction resolution
$PPXL reason "McKinsey says AI agent adoption is 40% in enterprise by 2025. Gartner says 15%. Analyze which is more credible."

# Thesis validation
$PPXL reason "Evaluate: Multi-agent systems consistently outperform single-agent approaches for complex enterprise tasks"
```

### Deep Dive (Checkpoint Only)

```bash
# Only after orchestrator checkpoint with user approval
$PPXL deep-research "Complete landscape analysis of AI agent frameworks for enterprise deployment in 2025" --confirm
```
