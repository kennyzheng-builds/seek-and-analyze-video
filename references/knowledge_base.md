# Knowledge Base Building Workflow

Build a searchable knowledge base from video content and text memories, queryable with natural language via Memory Augmented Generation (MAG).

## When to Use

- User wants to "build a knowledge base" from videos
- User says "I want to be able to search across all my videos"
- User wants to extract and organize insights from multiple videos
- User asks "what do my videos say about X" (cross-video query)
- User wants to store and retrieve knowledge/notes with semantic search

## Core Concept: MAG (Memory Augmented Generation)

Memories.ai combines two types of content:
1. **Video memories**: Indexed videos searchable by visual/audio content
2. **Text memories**: Stored text notes searchable by semantic meaning

`chat_personal` queries BOTH simultaneously, providing answers grounded in your full knowledge base. This is the key differentiator -- most platforms only do text. Memories.ai combines video understanding + text into a unified queryable layer.

## Workflow: Build from Existing Videos

**Step 1: Survey existing library**
```bash
python scripts/memories_api.py list_videos --status PARSE --size 50
```

**Step 2: Search for relevant content**
```bash
python scripts/memories_api.py search "<TOPIC>" --top-k 20
```

**Step 3: Extract insights from key videos**
For each relevant video:
```bash
python scripts/memories_api.py chat_video "<VIDEO_NO>" "Extract the key facts, insights, and claims made in this video. Be specific and include details."
```

**Step 4: Store as structured memories**
```bash
python scripts/memories_api.py memory_add "From video <VIDEO_NO> about <topic>: [extracted insights]" --tags "<topic>,video-insight"
```

Repeat for each video. Use consistent tag conventions.

**Step 5: Verify the knowledge base**
```bash
python scripts/memories_api.py chat_personal "What do I know about <topic>? Summarize based on my videos and memories."
```

## Workflow: Build from New Content

**Step 1: Upload videos**
```bash
python scripts/memories_api.py upload_video "<URL_1>" --tags "kb,<topic>"
python scripts/memories_api.py upload_video "<URL_2>" --tags "kb,<topic>"
```

**Step 2: Wait for all to process**
```bash
python scripts/memories_api.py wait "<VIDEO_NO_1>"
python scripts/memories_api.py wait "<VIDEO_NO_2>"
```

**Step 3: Bulk insight extraction**
```bash
python scripts/memories_api.py chat_personal "Summarize the key insights from all recently uploaded videos tagged 'kb'"
```

**Step 4: Store synthesized knowledge**
```bash
python scripts/memories_api.py memory_add "Knowledge synthesis on <topic>: ..." --tags "kb,<topic>,synthesis"
```

## Workflow: Text-Only Knowledge Management

For users who just want to store and search text knowledge (no video):

**Store:**
```bash
python scripts/memories_api.py memory_add "Meeting with client: agreed on Q4 deliverables..." --tags "client,q4"
python scripts/memories_api.py memory_add "Architecture decision: chose PostgreSQL over MongoDB for..." --tags "architecture,database"
```

**Search:**
```bash
python scripts/memories_api.py memory_search "database decisions"
python scripts/memories_api.py memory_search "client agreements"
```

**Query across all memories:**
```bash
python scripts/memories_api.py chat_personal "What decisions have been made about our database architecture?"
```

**List all:**
```bash
python scripts/memories_api.py memory_list --page-size 50
```

## Tag Conventions

Recommend consistent tags for organization:
- `meeting`, `lecture`, `tutorial` -- content type
- `<project-name>` -- project scope
- `video-insight`, `synthesis` -- derived content
- `<topic>` -- subject matter

## Tips

- `chat_personal` is the primary query interface -- it searches both videos and text memories
- Store extracted insights as memories to make them searchable even faster (text search is faster than video re-analysis)
- Use `unique_id` (via `--unique-id`) to isolate different knowledge bases (e.g., per-project)
- Memories compound -- the more you store, the richer `chat_personal` answers become
