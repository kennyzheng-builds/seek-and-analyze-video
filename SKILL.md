---
name: seek-and-analyze-video
description: Seek and analyze video content using Memories.ai's Large Visual Memory Model. Use when the user wants to (1) find or search for videos on TikTok, YouTube, or Instagram by topic, hashtag, or creator, (2) analyze, summarize, or ask questions about a video from a URL, (3) research social media content trends, influencers, or viral patterns, (4) summarize meetings, lectures, or webinars from recordings and extract notes or action items, (5) build a searchable knowledge base from video content and text memories, (6) analyze or describe images with AI vision, (7) store and retrieve text knowledge with semantic search, or (8) import and index social media content into a personal video library.
---

# Seek and Analyze Video

Find, analyze, and build knowledge from video content via the Memories.ai API.

## Setup

Require a Memories.ai API key before proceeding. If `MEMORIES_API_KEY` is not set, instruct the user:

1. Sign up at https://memories.ai (free tier available)
2. Get API key at https://memories.ai/app/service/key
3. Set environment variable: `export MEMORIES_API_KEY="your-key-here"`

Optionally set `MEMORIES_UNIQUE_ID` to isolate data by project (default: `"default"`).

Run all commands via:
```bash
python scripts/memories_api.py <command> [args...]
```

## Workflow Router

Determine which workflow to follow based on user intent:

| User intent | Workflow | Reference |
|---|---|---|
| Shares a video URL with a question, or asks to analyze/summarize a video | Video Q&A | [references/video_qa.md](references/video_qa.md) |
| Asks about trends on TikTok/YouTube/Instagram, or wants to analyze influencers | Social Research | [references/social_research.md](references/social_research.md) |
| Asks to summarize a meeting, take notes from a lecture, or extract action items | Video Notes | [references/video_notes.md](references/video_notes.md) |
| Asks to build a knowledge base, or query across multiple videos | Knowledge Base | [references/knowledge_base.md](references/knowledge_base.md) |
| Asks to describe an image or do a quick one-shot video analysis | Quick Caption (below) | -- |
| Asks to remember/store something, or retrieve a previous note | Memory Management (below) | -- |

Default to Video Q&A if a URL is present, or Memory Management if no media is involved.

## Quick Caption

Analyze a video or image without uploading to the library:

```bash
# Analyze video
python scripts/memories_api.py caption_video "<URL>" "<QUESTION>"

# Analyze image
python scripts/memories_api.py caption_image "<URL>" "<QUESTION>"

# Enable reasoning mode for complex analysis
python scripts/memories_api.py caption_video "<URL>" "<QUESTION>" --think
```

## Memory Management

Store and retrieve text knowledge with semantic search:

```bash
# Store a memory
python scripts/memories_api.py memory_add "content to remember" --tags "tag1,tag2"

# Search memories semantically
python scripts/memories_api.py memory_search "query"

# List all memories
python scripts/memories_api.py memory_list

# Query across all videos and memories simultaneously
python scripts/memories_api.py chat_personal "question about stored knowledge"
```

## Key Concepts

- **Video numbers** (`VI...`): Unique identifiers for indexed videos returned from upload/import operations.
- **`chat_personal`**: Query across ALL videos and memories simultaneously via MAG (Memory Augmented Generation). Prefer for cross-content questions.
- **`chat_video`**: Query a specific video. Use when the user refers to a particular video.
- **`caption_video`/`caption_image`**: One-shot analysis without uploading. Fast but not persistent.
- **Processing**: Videos require time to index after upload. Use `wait` to block or `video_info` to poll.
- **Tags**: Use consistently to organize content for filtered searches.
- **`--session-id`**: Pass the same integer across multiple chat calls to maintain conversation context.

## Error Handling

| Error | Meaning | Action |
|---|---|---|
| API Error 0402 | Out of credits | Inform user to check credits at memories.ai/app/service/key |
| API Error 0429 | Rate limited | Wait 3-5 seconds, retry once |
| No API key | MEMORIES_API_KEY not set | Guide user through setup above |
| Video stuck UNPARSE | Still processing | Use `wait` or check later; long videos need more time |
| Empty chat response | Usually credit issue | Check credits; try `chat_personal` as fallback |

## Full API Reference

See [references/api_reference.md](references/api_reference.md) for the complete command list with all flags and options.
