---
name: linkedin
description: "This skill should be used when an agent needs to \"search LinkedIn\", \"find LinkedIn profiles\", \"scrape company page\", \"get LinkedIn data\", \"research a person on LinkedIn\", or gather professional network data for research. Covers searching and scraping LinkedIn profiles and company pages via Apify actors."
---

# LinkedIn Skill

Search for and extract data from LinkedIn profiles and company pages for research purposes.

## Profile Research

### Finding Profiles

Use the web-research skill to find relevant LinkedIn profiles:

```bash
# Use ask --pro for best results with context about each profile
$CLAUDE_PLUGIN_ROOT/scripts/ppxl ask --pro "Find LinkedIn profiles of key people at {company} in {role}. List profile URLs and their relevance."

# Or search for bulk URL discovery
$CLAUDE_PLUGIN_ROOT/scripts/ppxl search "site:linkedin.com/in {person name} {company} {role}" --max-results 10
```

Or via Firecrawl search:

```bash
firecrawl search "site:linkedin.com {person name} {role}" --limit 10
```

### Scraping Profiles via Apify CLI

Use the Apify CLI with the LinkedIn Profile Scraper actor:

```bash
# Single profile
echo '{
  "profileUrls": ["https://www.linkedin.com/in/username/"]
}' | apify call apify/linkedin-profile-scraper --silent --output-dataset

# Multiple profiles (batch)
echo '{
  "profileUrls": [
    "https://www.linkedin.com/in/username1/",
    "https://www.linkedin.com/in/username2/"
  ]
}' | apify call apify/linkedin-profile-scraper --silent --output-dataset
```

**Note:** Check `references/apify-actors.md` for configured actor IDs and CLI details.

### Profile Data Format

Save scraped profiles to the data folder:

```
research/{project}/data/profiles/linkedin-{name-slug}.md
```

Format:

```markdown
# LinkedIn Profile: {Full Name}

- **Title:** {current title}
- **Company:** {current company}
- **Location:** {location}
- **URL:** {linkedin url}
- **Scraped:** {today}

## Summary
{headline / about section}

## Experience
{list of positions}

## Education
{education history}

## Key Skills
{relevant skills}

## Relevance to Research
{how this person/profile relates to the research question}
```

## Company Page Research

### Scraping Company Pages

```bash
echo '{
  "companyUrls": ["https://www.linkedin.com/company/company-name/"]
}' | apify call apify/linkedin-company-scraper --silent --output-dataset
```

### Company Data Format

Save to:
```
research/{project}/data/companies/linkedin-{company-slug}.md
```

## Batch Processing

When researching multiple profiles or companies:

1. Collect all LinkedIn URLs from source scouting
2. Group into batches of 5 (respecting rate limits)
3. Scrape each batch
4. Process and format results
5. Update SOURCES.md

## Ethical Guidelines

- Only scrape publicly available information
- Respect LinkedIn's terms of service
- Use data for research purposes only
- Do not store sensitive personal information beyond what's needed for the research

## Additional Resources

### Reference Files

- **`references/apify-actors.md`** - Configured Apify actor details and API usage
