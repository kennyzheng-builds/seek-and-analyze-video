# Social Media Content Research Workflow

Research content trends, influencers, and viral patterns across TikTok, YouTube, and Instagram.

## When to Use

- User says "research what's trending on TikTok about X"
- User wants to analyze competitor or influencer content strategy
- User asks "why does this type of content go viral"
- User wants to discover content around a topic or hashtag
- User asks to "find videos about X on YouTube/TikTok/Instagram"

## Workflow: Topic Research

**Step 1: Search public platforms**
```bash
python scripts/memories_api.py search_public "<TOPIC>" --platform TIKTOK --top-k 10
```
Supported platforms: `TIKTOK`, `YOUTUBE`, `INSTAGRAM`. Returns matching videos with metadata (titles, URLs, thumbnails, engagement).

Present a summary of results to the user before importing.

**Step 2: Import top results for deep analysis**
```bash
python scripts/memories_api.py import_url "<VIDEO_URL_1>" --tags "research,<topic>"
python scripts/memories_api.py import_url "<VIDEO_URL_2>" --tags "research,<topic>"
python scripts/memories_api.py import_url "<VIDEO_URL_3>" --tags "research,<topic>"
```
Import 3-5 most relevant results. Each returns a `videoNo`. Collect all video numbers.

**Step 3: Wait for processing**
```bash
python scripts/memories_api.py wait "<VIDEO_NO_1>" --timeout 300
python scripts/memories_api.py wait "<VIDEO_NO_2>" --timeout 300
```

**Step 4: Cross-video analysis**
Use `chat_personal` to query across all imported videos:
```bash
python scripts/memories_api.py chat_personal "Based on the videos in my library tagged 'research', what are the common themes and patterns?"
```

For specific video questions:
```bash
python scripts/memories_api.py chat_video "<VIDEO_NO>" "What hook does this video use in the first 3 seconds?"
```

**Step 5: Store findings**
```bash
python scripts/memories_api.py memory_add "Research on <topic>: Key finding 1... Key finding 2..." --tags "research,<topic>"
```

## Workflow: Influencer/Creator Analysis

**Step 1: Import creator content**
```bash
python scripts/memories_api.py import_creator "<CREATOR_PROFILE_URL>" --count 10
```

**Step 2: Wait and analyze**
After processing completes, use `chat_personal` to analyze patterns:
```bash
python scripts/memories_api.py chat_personal "Analyze the content style, topics, and engagement patterns of the recently imported creator videos"
```

## Workflow: Hashtag Research

**Step 1: Import by hashtag**
```bash
python scripts/memories_api.py import_hashtag "<HASHTAG>" --platform TIKTOK --count 15
```

**Step 2: Analyze trends**
```bash
python scripts/memories_api.py chat_personal "What are the common visual elements, hooks, and themes in the videos tagged with <hashtag>?"
```

## Output Format

When presenting research results, structure as:
1. **Overview**: What was searched, how many results found
2. **Key Patterns**: Common themes, visual styles, hooks, audio patterns
3. **Top Performers**: Which videos stood out and why
4. **Actionable Insights**: What the user can learn or replicate
5. **Stored Memories**: What was saved for future reference

## Tips

- Always present search results to user before importing (importing costs credits)
- Use tags consistently to organize research by topic
- `chat_personal` is better than `chat_video` for cross-video patterns
- Import 3-5 videos per research session for good coverage without excessive credit usage
