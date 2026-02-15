# Apify Actors — YouTube

Prerequisite: `npm install -g apify-cli` then `apify login --token $APIFY_API_KEY`

## YouTube Transcript Scraper

**Actor:** `topaz_sharingan/Youtube-Transcript-Scraper-1`

### Download transcript (single video)

```bash
echo '{
  "includeTimestamps": "No",
  "startUrls": ["https://www.youtube.com/watch?v=VIDEO_ID"]
}' | apify call topaz_sharingan/Youtube-Transcript-Scraper-1 --silent --output-dataset
```

### Download transcripts (batch)

```bash
echo '{
  "includeTimestamps": "No",
  "startUrls": [
    "https://www.youtube.com/watch?v=ID_1",
    "https://www.youtube.com/watch?v=ID_2",
    "https://www.youtube.com/watch?v=ID_3"
  ]
}' | apify call topaz_sharingan/Youtube-Transcript-Scraper-1 --silent --output-dataset
```

### With timestamps

```bash
echo '{
  "includeTimestamps": "Yes",
  "startUrls": ["https://www.youtube.com/watch?v=VIDEO_ID"]
}' | apify call topaz_sharingan/Youtube-Transcript-Scraper-1 --silent --output-dataset
```

### Key options

| Option | Description |
|--------|-------------|
| `--silent` | Suppress progress output, only print result |
| `--output-dataset` | Print the dataset items to stdout |
| `-i '{"key":"val"}'` | Pass input inline instead of via stdin |

### Output format

**Without timestamps** (`includeTimestamps: "No"`):
```json
{ "transcript": "Full transcript text..." }
```

**With timestamps** (`includeTimestamps: "Yes"`):
```json
{
  "transcript": [
    { "timestamp": "0:01", "text": "First sentence." },
    { "timestamp": "0:04", "text": "Second sentence." }
  ]
}
```

If a video has no transcript available, the result will be `null`.
