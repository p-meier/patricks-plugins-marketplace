---
name: web-research
description: "This skill should be used when an agent needs to \"search the web\", \"find information online\", \"fetch a webpage\", \"scrape a website\", \"download article content\", or access any online resource. Provides a unified cost-tiered strategy for web search via Perplexity Python SDK and content fetching via Firecrawl CLI."
---

# Web Research Skill

Unified skill for all web interactions: searching, fetching, and scraping. All Perplexity operations go through the Python CLI at `${CLAUDE_PLUGIN_ROOT}/scripts/ppxl.py`, which uses the official `perplexityai` SDK with full domain filtering, recency, and language support.

## Cost Tiers — Read This First

| Command | Cost | When to Use |
|---------|------|-------------|
| `ask --pro` | ~$0.05/req | **Default for everything.** Best quality, citations, domain filters. |
| `search` | ~$0.005/req | Only for bulk URL discovery when raw links are enough (no AI synthesis needed). |
| `ask` | ~$0.01/req | Rarely. Only if budget is extremely tight and quality can be lower. |
| `reason` | ~$0.10/req | Contradiction analysis, thesis validation, complex reasoning. |
| `deep-research` | ~$0.50-2+/req | **CHECKPOINT ONLY.** Never in loops. Requires `--confirm` flag. |

**Rule:** Use `ask --pro` as default for all queries. It is still cheap and yields significantly better results with proper citations. Only fall back to `search` when you need a batch of raw URLs without synthesis (e.g., 20 URLs to scrape later). Never use `deep-research` without orchestrator checkpoint approval.

## Perplexity CLI Reference

All commands use the Python script via the plugin venv:

```bash
PPXL="$CLAUDE_PLUGIN_ROOT/scripts/ppxl"
```

### ask --pro — Default for All Queries

```bash
# Standard research query (sonar-pro, best quality with citations)
$PPXL ask --pro "AI agent frameworks enterprise deployment comparison"

# Domain-filtered query
$PPXL ask --pro "Latest AI market report findings" --domains "mckinsey.com,gartner.com,forrester.com"

# Exclude low-quality domains
$PPXL ask --pro "AI trends 2025" --exclude-domains "pinterest.com,reddit.com,quora.com"

# Recent results only
$PPXL ask --pro "AI startup funding news" --recency week

# Academic focus
$PPXL ask --pro "Recent machine learning survey papers on transformer architectures" --domains "arxiv.org,nature.com,science.org,.edu"

# Regional + language
$PPXL ask --pro "KI Trends Deutschland" --recency month --domains ".de"
```

**Supports:** `--domains`, `--exclude-domains`, `--recency day|week|month`

### search — Bulk URL Discovery Only

Use `search` only when you need a list of raw URLs without AI synthesis (e.g., to scrape later):

```bash
# Get 20 URLs to scrape
$PPXL -o json search "AI agent frameworks" --max-results 20

# Find YouTube videos to download transcripts from
$PPXL search "site:youtube.com AI agents talk conference" --max-results 10

# Find LinkedIn profiles
$PPXL search "site:linkedin.com CTO AI startup" --max-results 10
```

**Additional options:** `--language`, `--country`, `--max-results 1-20`

### reason — Complex Analysis

```bash
# Contradiction resolution
$PPXL reason "Source A claims AI agent adoption is 40% in enterprise. Source B says 15%. Which is more likely correct and why?"

# Thesis validation
$PPXL reason "Is it true that multi-agent frameworks outperform single-agent approaches for complex tasks? Evaluate the evidence."
```

### deep-research — Expensive, Checkpoint Only

```bash
# Requires --confirm flag (safety guard)
$PPXL deep-research "Comprehensive analysis of the AI agent framework landscape in 2025" --confirm
```

**Never call deep-research in automated loops.** Only the orchestrator should trigger it at explicit checkpoints with user approval.

## Search Strategy

### Default Workflow

1. Use `ask --pro` for all research queries — it provides synthesized answers with citations
2. Use `search` only when you need a batch of raw URLs to scrape/download later
3. Use `reason` for contradiction resolution and thesis validation during synthesis
4. Reserve `deep-research` for checkpoint-level comprehensive queries only (requires user approval)

### Query Best Practices

- Use `--recency` filters instead of years in queries (avoids SEO spam)
- Only include year for official reports: "McKinsey AI Survey 2025"
- Be specific: "AI Agent frameworks enterprise deployment comparison" not "AI frameworks"
- Use `--domains` to target trusted sources per domain context
- Use `site:` prefix in query for platform-specific: `"site:youtube.com AI tutorial"`

### Fallback: Firecrawl Search

If Perplexity returns no results or errors, use Firecrawl search as fallback:

```bash
firecrawl search "query" --limit 10
```

Log the fallback in STATE.md under API Usage but do not interrupt the workflow.

**Do NOT use Claude's built-in WebSearch tool.** All web searches go through ppxl or Firecrawl.

## Fetch Strategy

### Primary: Firecrawl CLI

**Always use Firecrawl for fetching URLs.** Never use WebFetch — Firecrawl handles JS-heavy sites, bot protection, and paywalls better.

```bash
# Single page scrape (default for all URLs)
firecrawl https://example.com --only-main-content -o output.md

# Wait for JavaScript rendering (for SPAs and dynamic content)
firecrawl https://example.com --only-main-content --wait-for 3000

# Search and scrape results
firecrawl search "topic" --limit 10 --scrape --scrape-formats markdown
```

### Fetch Decision Tree

```
Need content from URL?
├─ firecrawl URL --only-main-content
│  ├─ Success → Use content
│  └─ Empty/failed
│     ├─ firecrawl URL --only-main-content --wait-for 3000
│     │  ├─ Success → Use content
│     │  └─ Failed → Try Perplexity search to find alternative source
```

## Batch Operations

When searching for multiple topics or fetching multiple URLs:

1. Group into batches of max 5 concurrent requests
2. Execute batch
3. Wait for all results
4. Evaluate quality
5. Execute next batch

This limit is enforced by the rate-limiting hook but should also be followed proactively.

## Saving Fetched Content

Save all fetched content to the project's `data/` folder:

```
research/{project}/data/
├── articles/     # Scraped web articles (markdown)
├── transcripts/  # Video transcripts
└── reports/      # Downloaded PDFs and documents
```

**Naming convention:** `{source-domain}-{slug}.md`
- Example: `mckinsey-state-of-ai-2025.md`
- Example: `techcrunch-langchain-funding.md`

## Additional Resources

### Reference Files

- **`references/perplexity-cli.md`** - Full Perplexity Python CLI options and examples
- **`references/firecrawl-cli.md`** - Complete Firecrawl CLI reference
