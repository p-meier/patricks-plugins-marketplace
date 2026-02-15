# Apify Actors — LinkedIn

Prerequisite: `npm install -g apify-cli` then `apify login --token $APIFY_API_KEY`

## LinkedIn Profile Scraper

**Actor:** `apify/linkedin-profile-scraper`

### Scrape profiles

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

## LinkedIn Company Scraper

**Actor:** `apify/linkedin-company-scraper`

```bash
echo '{
  "companyUrls": [
    "https://www.linkedin.com/company/company-name/"
  ]
}' | apify call apify/linkedin-company-scraper --silent --output-dataset
```

## Key CLI Options

| Option | Description |
|--------|-------------|
| `--silent` | Suppress progress output, only print result |
| `--output-dataset` | Print the dataset items to stdout |
| `-i '{"key":"val"}'` | Pass input inline instead of via stdin |

## Configuration

Set exact actor IDs in plugin settings (.local.md) if using different actors:

```yaml
---
apify_linkedin_profile_actor: "apify/linkedin-profile-scraper"
apify_linkedin_company_actor: "apify/linkedin-company-scraper"
---
```
