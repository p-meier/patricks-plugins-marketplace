---
name: youtube
description: "This skill should be used when an agent needs to \"find YouTube videos\", \"download a transcript\", \"get video subtitles\", \"process YouTube content\", \"extract video information\", or work with any YouTube-related research material. Covers searching for videos and downloading transcripts via Apify CLI."
---

# YouTube Skill

Search for relevant YouTube videos and download their transcripts for local research processing.

## Finding Videos

### Search via Perplexity

Use the web-research skill's Perplexity CLI to find relevant videos:

```bash
# Use ask --pro for best results with context about each video
$CLAUDE_PLUGIN_ROOT/scripts/ppxl ask --pro "Find the best YouTube videos about {topic}: conference talks, tutorials, expert presentations. List URLs, channel names, and why each is relevant."

# Or search for bulk URL discovery when you just need a list of links
$CLAUDE_PLUGIN_ROOT/scripts/ppxl search "site:youtube.com {topic} tutorial OR talk OR presentation" --max-results 10
```

### Search via Firecrawl

For broader video discovery:

```bash
firecrawl search "site:youtube.com {topic}" --limit 20 --pretty
```

## Downloading Transcripts

### Via Apify CLI

Download transcripts using the Apify CLI with the YouTube Transcript Scraper actor:

```bash
# Single video
echo '{
  "includeTimestamps": "No",
  "startUrls": ["https://www.youtube.com/watch?v=VIDEO_ID"]
}' | apify call topaz_sharingan/Youtube-Transcript-Scraper-1 --silent --output-dataset

# Multiple videos (batch)
echo '{
  "includeTimestamps": "No",
  "startUrls": [
    "https://www.youtube.com/watch?v=ID_1",
    "https://www.youtube.com/watch?v=ID_2"
  ]
}' | apify call topaz_sharingan/Youtube-Transcript-Scraper-1 --silent --output-dataset
```

### Transcript Processing Workflow

1. **Identify relevant videos** using web-research skill (Perplexity search)
2. **Download transcripts** via `apify call`
3. **Save to data folder:**
   ```
   research/{project}/data/transcripts/youtube-{channel}-{title-slug}.md
   ```
4. **Format the transcript file:**
   ```markdown
   # YouTube Transcript: {Title}

   - **Channel:** {channel name}
   - **URL:** {youtube url}
   - **Duration:** {duration}
   - **Published:** {date}
   - **Downloaded:** {today}

   ---

   {transcript content}
   ```
5. **Create summary** in `summaries/` using the standard summary format

## Batch Processing

When processing multiple videos:

1. Collect all YouTube URLs from source scouting
2. Group into batches of 5 (respecting rate limits)
3. Download transcripts for each batch via `apify call` with multiple startUrls
4. Process and summarize each transcript
5. Update SOURCES.md with video entries

## Quality Assessment

Not all YouTube content is equal. Apply source evaluation criteria:

| Indicator | High Quality | Low Quality |
|-----------|-------------|-------------|
| Channel | Established expert, company channel | Unknown creator |
| Views | >10K views | <1K views |
| Length | 15-60 min (substantive) | <5 min (shallow) |
| Type | Conference talk, interview, tutorial | Listicle, reaction |
| Comments | Technical discussion | Spam or superficial |

## Additional Resources

### Reference Files

- **`references/apify-actors.md`** - Actor IDs, CLI examples, and output format details
