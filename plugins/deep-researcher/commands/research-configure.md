---
name: research:configure
description: Configure trusted sources, API settings, and domain preferences
arguments:
  - name: setting
    description: "Setting to configure: sources, api, domain"
    required: false
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
---

Configure the deep-researcher plugin settings.

## Process

### If no setting specified, show current configuration:

Read `.claude/deep-researcher.local.md` (if exists) and display current settings.

### Settings Categories

#### 1. Trusted Sources (`/research:configure sources`)

Ask user to define trusted sources per domain:

```yaml
---
enterprise_trusted_sources:
  - "McKinsey"
  - "Accenture"
  - "Gartner"
  - "Forrester"
  - "BCG"
  - "Deloitte"
small_project_trusted_sources:
  - "TechCrunch"
  - "Medium"
  - "Dev.to"
  - "Hacker News"
personal_trusted_sources:
  - "WebMD"
  - "Mayo Clinic"
  - "Healthline"
---
```

#### 2. API Settings (`/research:configure api`)

Configure rate limits and API preferences:

```yaml
---
perplexity_rpm: 10
firecrawl_rpm: 20
apify_rpm: 30
max_concurrent_calls: 5
---
```

#### 3. Domain Default (`/research:configure domain`)

Set default research domain:

```yaml
---
default_domain: "enterprise"
---
```

#### 4. Apify Actor Configuration (`/research:configure apify`)

Set the exact Apify actor IDs:

```yaml
---
apify_youtube_actor: "bernardo~youtube-transcript-scraper"
apify_linkedin_profile_actor: "apify~linkedin-profile-scraper"
apify_linkedin_company_actor: "apify~linkedin-company-scraper"
---
```

### Save Settings

Write to `.claude/deep-researcher.local.md` in the project root.
