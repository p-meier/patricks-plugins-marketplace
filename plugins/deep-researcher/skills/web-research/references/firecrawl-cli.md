# Firecrawl CLI Reference

Prerequisite: `npm install -g firecrawl-cli`

Authenticate: `firecrawl login --api-key fc-YOUR-API-KEY` or `export FIRECRAWL_API_KEY=fc-...`

Check status: `firecrawl --status` (shows auth, concurrency, credits remaining)

## Scrape — Single Page

Extract content from a single URL. Use `--only-main-content` for clean output.

```bash
# Markdown output (default), main content only (recommended)
firecrawl https://example.com --only-main-content

# Save to file
firecrawl https://example.com --only-main-content -o output.md

# Wait for JavaScript rendering (SPAs, dynamic content)
firecrawl https://example.com --only-main-content --wait-for 3000

# HTML output
firecrawl https://example.com --html

# Multiple formats (returns JSON)
firecrawl https://example.com --format markdown,links

# Get images from a page
firecrawl https://example.com --format images

# Get a summary
firecrawl https://example.com --format summary

# Screenshot
firecrawl https://example.com --screenshot

# Include/exclude specific HTML tags
firecrawl https://example.com --include-tags article,main
firecrawl https://example.com --exclude-tags nav,footer
```

**Key options:**

| Option | Description |
|--------|-------------|
| `--only-main-content` | Strip nav, footer, ads (recommended for research) |
| `--format <formats>` | markdown, html, rawHtml, links, screenshot, json, images, summary, changeTracking, attributes, branding |
| `--wait-for <ms>` | Wait time for JS rendering |
| `--include-tags <tags>` | Only specific HTML tags (comma-separated) |
| `--exclude-tags <tags>` | Exclude HTML tags (comma-separated) |
| `-o <path>` | Save to file |
| `--json` | Force JSON output even with single format |
| `--pretty` | Pretty print JSON output |
| `--timing` | Show request timing information |

## Search — Web Search

Search the web and optionally scrape the results.

```bash
# Basic search
firecrawl search "machine learning tutorials"

# With limit and time filter
firecrawl search "AI news" --limit 10 --tbs qdr:w

# Search and scrape results in one step
firecrawl search "documentation" --scrape --scrape-formats markdown

# Filter by source type
firecrawl search "react hooks" --categories github
firecrawl search "AI paper" --categories research,pdf

# Location-based search
firecrawl search "restaurants" --location "Berlin,Germany" --country DE

# Save results
firecrawl search "firecrawl" --pretty -o results.json
```

**Time filters (--tbs):**

| Value | Period |
|-------|--------|
| `qdr:h` | Last hour |
| `qdr:d` | Last day |
| `qdr:w` | Last week |
| `qdr:m` | Last month |
| `qdr:y` | Last year |

**Options:**

| Option | Description |
|--------|-------------|
| `--limit <number>` | Max results (default: 5, max: 100) |
| `--sources <sources>` | Sources: `web`, `images`, `news` (comma-separated) |
| `--categories <categories>` | Filter: `github`, `research`, `pdf` (comma-separated) |
| `--tbs <value>` | Time filter (see table above) |
| `--location <location>` | Geo-targeting (e.g., "Berlin,Germany") |
| `--country <code>` | ISO country code (default: US) |
| `--scrape` | Also scrape search results |
| `--scrape-formats <formats>` | Formats for scraped content (default: markdown) |
| `--only-main-content` | Main content only when scraping (default: true) |

## Map — URL Discovery

Quickly discover all URLs on a website.

```bash
# Find all URLs on a site
firecrawl map https://example.com --limit 500

# Search for specific pages
firecrawl map https://example.com --search "blog"

# Include subdomains
firecrawl map https://example.com --include-subdomains

# Sitemap controls
firecrawl map https://example.com --sitemap include
firecrawl map https://example.com --sitemap only
```

## Crawl — Entire Website

Crawl a full website starting from a URL.

```bash
# Crawl with progress
firecrawl crawl https://example.com --wait --progress --limit 100

# Specific paths only
firecrawl crawl https://example.com --include-paths /blog,/docs --wait

# Depth-limited crawl
firecrawl crawl https://example.com --limit 50 --max-depth 2 --wait

# Rate-limited crawl
firecrawl crawl https://example.com --delay 1000 --max-concurrency 2 --wait

# Check status of existing crawl
firecrawl crawl <job-id>
```

## Agent — Natural Language Web Research

Search and gather data using natural language prompts. Powerful for structured extraction.

```bash
# Basic agent query (URLs are optional)
firecrawl agent "Find the top 5 AI startups and their funding amounts" --wait

# Focus on specific URLs
firecrawl agent "Compare pricing plans" --urls https://slack.com/pricing,https://teams.microsoft.com/pricing --wait

# Structured output with schema
firecrawl agent "Get company information" --urls https://example.com --schema '{"name": "string", "founded": "number"}' --wait

# Use schema from a file
firecrawl agent "Get product details" --urls https://example.com --schema-file schema.json --wait

# Higher accuracy model
firecrawl agent "Competitive analysis" --model spark-1-pro --wait

# Limit costs
firecrawl agent "Gather contact information" --max-credits 100 --wait
```

**Agent options:**

| Option | Description |
|--------|-------------|
| `--urls <urls>` | URLs to focus on (comma-separated, optional) |
| `--model <model>` | `spark-1-mini` (default, 60% cheaper) or `spark-1-pro` (higher accuracy) |
| `--schema <json>` | JSON schema for structured output |
| `--schema-file <path>` | Path to JSON schema file |
| `--max-credits <number>` | Maximum credits to spend |
| `--wait` | Wait for completion |

## Error Handling

### JavaScript-Heavy / SPAs
```bash
firecrawl https://spa-app.com --wait-for 5000
```

### Paywall/Login Wall
Firecrawl often handles paywalls better than standard fetching. If still blocked:
```bash
firecrawl search "article title site:archive.org"
```

### Rate Limiting
For crawls, set delay:
```bash
firecrawl crawl https://example.com --delay 2000 --max-concurrency 1 --wait
```

### Credit Usage
```bash
firecrawl credit-usage
firecrawl --status  # Auth, credits, concurrency
```
