# Video Q&A Workflow

Ask questions about any video from a URL. The most common use case -- users paste a link and want to understand, analyze, or interrogate the video content.

## When to Use

- User shares a video URL and asks a question about it
- User says "what's in this video", "summarize this video", "analyze this"
- User wants to understand a specific moment, scene, or topic in a video
- User asks about emotions, objects, people, or events in a video

## Workflow

### Quick Analysis (no upload, instant results)

Use `caption_video` for fast, one-shot analysis when the user needs a quick answer without persistent indexing.

```bash
python scripts/memories_api.py caption_video "<VIDEO_URL>" "<USER_QUESTION>"
```

This returns an immediate AI analysis. Good for:
- "What's happening in this video?"
- "Describe the emotions shown"
- "What products appear in this clip?"

For complex reasoning tasks, add `--think`:
```bash
python scripts/memories_api.py caption_video "<URL>" "Count the number of people" --think
```

### Deep Analysis (upload + persistent chat)

Use when the user needs multi-turn Q&A, transcript access, or plans to revisit the video later.

**Step 1: Upload for indexing**
```bash
python scripts/memories_api.py upload_video "<VIDEO_URL>" --tags "user-upload"
```
Returns a response containing `taskId` and `videoNo` in the `data` field. Extract both.

**Step 2: Wait for processing**
```bash
python scripts/memories_api.py wait "<VIDEO_NO>" --timeout 600
```
Blocks until the video is fully indexed. Short clips (~1 min) finish in under a minute; longer videos may take several minutes.

**Step 3: Chat with the video**
```bash
python scripts/memories_api.py chat_video "<VIDEO_NO>" "<USER_QUESTION>"
```
This leverages the full indexed content for accurate, context-aware answers.

**Step 4 (optional): Get transcript**
```bash
python scripts/memories_api.py transcript "<VIDEO_NO>"
python scripts/memories_api.py transcript "<VIDEO_NO>" --audio
```
- Without `--audio`: visual scene descriptions (what's happening visually)
- With `--audio`: spoken words transcription

**Step 5 (optional): Store key insights**
```bash
python scripts/memories_api.py memory_add "Key insight from video <VIDEO_NO>: ..."
```

### Finding Specific Moments (search within a video)

After uploading a video, use `search_audio` to find specific quotes, topics, or moments in the spoken content:

```bash
python scripts/memories_api.py search_audio "<VIDEO_NO>" "acquisition deal"
```

Returns matching segments with timestamps. Use this when:
- User asks "find where they discuss X"
- User wants exact quotes or timestamps
- User needs to locate a specific topic in a long video

Combine with `chat_video` for context around the found moment:
```bash
python scripts/memories_api.py chat_video "<VIDEO_NO>" "Give me the exact quotes and context around the acquisition deal discussion"
```

**When to use which:**
- `search_audio`: Find specific moments/quotes by keyword (fast, targeted)
- `transcript --audio`: Get full spoken transcript (comprehensive, for notes)
- `chat_video`: Ask questions with AI interpretation (flexible, conversational)

## Decision: Quick vs Deep

| Signal | Use Quick (caption_video) | Use Deep (upload + chat) |
|---|---|---|
| One-off question | Yes | No |
| Multi-turn conversation | No | Yes |
| Need transcript | No | Yes |
| Will revisit later | No | Yes |
| Video already in library | N/A | Just use chat_video directly |

## Image Analysis

For images instead of video:
```bash
python scripts/memories_api.py caption_image "<IMAGE_URL>" "<QUESTION>"
```

## Error Recovery

| Error | Action |
|---|---|
| Video stuck in UNPARSE | Wait longer; use `video_info` to check. Long videos need more time |
| Empty chat response | Credits may be depleted. Check at memories.ai/app/service/key |
| API Error 0402 | Insufficient credits -- inform the user |
| API Error 0429 | Rate limited -- wait a few seconds and retry |
