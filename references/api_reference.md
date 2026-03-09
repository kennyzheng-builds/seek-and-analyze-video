# Memories.ai API Reference

Quick reference for all available commands via `scripts/memories_api.py`.

## Setup

**API Key**: Set `MEMORIES_API_KEY` environment variable, or pass `--api-key KEY` to every command.
**Namespace**: Set `MEMORIES_UNIQUE_ID` for multi-project isolation, or pass `--unique-id ID`. Default: `"default"`.

All commands output JSON to stdout. Errors exit with non-zero code and JSON error message.

## Commands

### Video Management

| Command | Description |
|---|---|
| `upload_video <url> [--tags T] [--callback URL]` | Upload video from URL. Returns `taskId` and `videoNo` |
| `upload_file <path> [--tags T]` | Upload local video file |
| `list_videos [--status S] [--page N] [--size N]` | List videos. Status: PARSE (ready), UNPARSE (processing), FAIL |
| `video_status <task_id>` | Check processing status by task ID |
| `video_info <video_no>` | Get single video details |
| `delete_videos <vn1> [vn2...]` | Delete videos by number |
| `transcript <video_no> [--audio]` | Get transcription. Default: visual. `--audio`: spoken words |
| `wait <video_no> [--timeout N]` | Block until video is ready (default 600s) |

### Search

| Command | Description |
|---|---|
| `search <query> [--top-k N] [--tag T] [--video-nos V1,V2]` | Semantic search across private library |
| `search_public <query> [--platform P] [--top-k N]` | Search TikTok/YouTube/Instagram |
| `search_audio <video_no> <query>` | Search within audio transcripts of a specific video |

### Chat

| Command | Description |
|---|---|
| `chat_video <video_no> <prompt> [--session-id N]` | Chat about a specific video |
| `chat_personal <prompt> [--session-id N]` | Chat across entire library + memories (MAG) |

### Text Memory

| Command | Description |
|---|---|
| `memory_add <content> [--tags T]` | Store text with semantic indexing |
| `memory_search <query> [--page N] [--page-size N]` | Semantic search across memories |
| `memory_list [--page N] [--page-size N]` | List all stored memories |

### AI Vision

| Command | Description |
|---|---|
| `caption_video <url> <prompt> [--think]` | Analyze video without uploading. `--think` for reasoning mode |
| `caption_image <url> <prompt>` | Analyze image from URL |

### Social Media Import

| Command | Description |
|---|---|
| `import_url <url> [--tags T]` | Import from social media URL |
| `import_hashtag <hashtag> [--platform P] [--count N]` | Import by hashtag |
| `import_creator <creator_url> [--count N]` | Import from creator profile |

## Response Format

All successful responses follow:
```json
{
  "code": "0000",
  "msg": "success",
  "data": { ... }
}
```

## Common Error Codes

| Code | Meaning | Recovery |
|---|---|---|
| 0402 | Insufficient credits | User needs to top up at memories.ai/app/service/key |
| 0429 | Rate limited | Wait a few seconds, retry |
| 401 | Invalid API key | Check key at memories.ai/app/service/key |

## Video Number Format

Video numbers look like `VI685903399832780800` (prefix `VI` + numeric ID). Task IDs are returned from upload operations. Use `video_status` to convert task ID -> video number.

## Processing Times

- Short clips (<1 min): ~30 seconds
- Medium videos (1-10 min): 1-3 minutes
- Long videos (10-60 min): 5-10 minutes
- Very long (>60 min): 10+ minutes
