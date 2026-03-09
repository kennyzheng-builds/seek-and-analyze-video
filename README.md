# Seek and Analyze Video

A Claude Code skill that gives AI agents the ability to **find, analyze, and build knowledge from video content** -- powered by [Memories.ai](https://memories.ai)'s Large Visual Memory Model (LVMM).

Drop a YouTube link and ask "what's in this video?" or say "research what's trending on TikTok about AI agents" -- the skill handles the rest.

---

## Why This Exists

Video is everywhere -- meetings, lectures, TikTok, YouTube, Instagram -- but it's trapped. You can't search inside it. You can't ask it questions. You can't build knowledge from it at scale.

General-purpose LLMs like ChatGPT and Gemini can look at video, but they have fundamental limitations:

| Limitation | ChatGPT | Gemini | This Skill (Memories.ai) |
|---|---|---|---|
| Video context window | ~10 min, single video | ~1 hour, single video | **Unlimited** -- index once, query forever |
| Persistent memory across videos | No | No | **Yes** -- cross-video search and Q&A |
| Search your video library | No | YouTube only (Google-owned) | **Yes** -- semantic search across any video |
| Social media research | No | No | **Yes** -- search and import from TikTok, YouTube, Instagram |
| Text + video memory combined | No | No | **Yes** -- MAG (Memory Augmented Generation) |
| Works inside an AI agent | Manual copy-paste | Manual copy-paste | **Native** -- agent calls API directly |

ChatGPT and Gemini treat video as a one-shot input: you upload one video, ask about it, and the context is gone. Memories.ai indexes video into a persistent, searchable memory layer that agents can query anytime -- across hundreds of videos simultaneously.

## What This Skill Does

### For Individual Users

**"Just tell me what's in this video"**
- Paste any video URL (YouTube, TikTok, Instagram, Vimeo) and ask questions
- Summarize a 2-hour meeting recording into bullet points and action items
- Take structured notes from a lecture or webinar
- Get transcripts (both spoken words and visual scene descriptions)

**"Help me find and research video content"**
- Search TikTok, YouTube, or Instagram for videos about any topic
- Import and analyze videos from social media by URL, hashtag, or creator
- Build a research report from multiple video sources

**"Remember this for me"**
- Store insights, notes, and summaries as searchable text memories
- Query across all your videos and memories at once with natural language
- Build a personal knowledge base that compounds over time

### For Agencies & Teams

**Content & Social Media**
- Research competitor content strategies across platforms
- Analyze what makes content go viral -- hooks, pacing, visual patterns
- Discover and evaluate influencers by analyzing their video content
- Track trends and extract actionable insights at scale

**Marketing & Brand**
- Reverse-engineer successful ad creatives
- Monitor brand mentions and sentiment across video content
- Build a searchable library of reference content for creative teams

**Operations & Knowledge**
- Index training videos, onboarding materials, and internal presentations
- Make institutional knowledge searchable and queryable
- Summarize meeting recordings automatically for distributed teams
- Isolate projects with namespace support (`MEMORIES_UNIQUE_ID`)

## Getting Started

### 1. Get Your API Key

1. Sign up at [memories.ai](https://memories.ai) -- free tier includes 100 credits, no credit card required
2. Go to [memories.ai/app/service/key](https://memories.ai/app/service/key) to get your API key

### 2. Install the Skill

**Claude Code / HappyCapy:**
```bash
claude skill install seek-and-analyze-video.skill
```

**OpenClaw:**

OpenClaw uses the same skill format. Drop the skill folder into your OpenClaw skills directory:
```bash
cp -r seek-and-analyze-video ~/.openclaw/skills/
```
Or reference the GitHub repo directly in your OpenClaw config. The skill works with any AI model OpenClaw routes through (Claude, GPT, etc.) -- the Python API client is model-agnostic.

**Manual installation (any compatible platform):**
```bash
cp -r seek-and-analyze-video ~/.claude/skills/
```

### 3. Set Your API Key

```bash
export MEMORIES_API_KEY="your-api-key-here"
```

Add to your shell profile (`~/.bashrc`, `~/.zshrc`) to persist across sessions.

### 4. Start Using It

Just talk to your AI agent naturally:

> "Summarize this YouTube video: https://youtube.com/watch?v=..."

> "What's trending on TikTok about sustainable fashion?"

> "Take notes from this meeting recording and extract action items"

> "Build a knowledge base from all the product review videos I've uploaded"

The skill automatically detects user intent and selects the right workflow.

## When to Use This Skill

| Scenario | Example prompt |
|---|---|
| Understand a video | "What are the key points in this video?" |
| Summarize a meeting | "Summarize this recording and list the action items" |
| Research a topic | "Find the top TikTok videos about AI coding tools" |
| Analyze a creator | "Analyze this YouTuber's content strategy" |
| Find specific moments | "Find where they discuss pricing in this video" |
| Build a knowledge base | "Extract insights from all my uploaded videos about marketing" |
| Quick image analysis | "Describe what's in this image" |
| Store knowledge | "Remember that the Q4 target is 500K ARR" |
| Recall knowledge | "What decisions did we make about the database?" |

## How It Works

```
User request
     |
     v
+-----------+     +----------------+     +---------------+
| AI Agent  |---->| Skill Router   |---->| Memories.ai   |
| (Claude)  |     | (SKILL.md)     |     | REST API      |
+-----------+     +----------------+     +---------------+
                        |                       |
                 Picks workflow:          Returns results:
                 - Video Q&A             - AI analysis
                 - Social Research       - Transcripts
                 - Video Notes           - Search results
                 - Knowledge Base        - Chat responses
                 - Quick Caption         - Stored memories
                 - Memory Management
```

The skill includes:
- **`SKILL.md`** -- Workflow router that maps user intent to the right workflow
- **`scripts/memories_api.py`** -- Python API client (21 commands, zero dependencies)
- **`references/`** -- Detailed workflow guides loaded on-demand by the agent

## Compared to Alternatives

### vs. Using Gemini/ChatGPT Directly

Gemini and ChatGPT can analyze individual videos you paste into the chat. But:
- Context is lost after the conversation ends
- Can't search across multiple videos
- Can't build a persistent, queryable video library
- Can't automate research workflows
- No social media search/import

This skill gives agents persistent video intelligence -- not just one-shot analysis.

### vs. Twelve Labs API

Twelve Labs is a strong video understanding platform. Key differences:
- Twelve Labs focuses on video search and classification (developer-oriented)
- Memories.ai adds text memory (MAG), social media import, and cross-video chat
- This skill wraps everything into a ready-to-use agent skill -- no integration work
- Free tier available (Twelve Labs requires enterprise contact)

### vs. Manual API Integration

You could call the Memories.ai REST API directly. But:
- This skill provides workflow logic (upload -> wait -> analyze -> store) built-in
- The agent automatically picks the right workflow based on user intent
- Error handling, retry logic, and status polling are handled
- Zero dependency Python client -- works anywhere with Python 3.8+

## Skill Structure

```
seek-and-analyze-video/
├── SKILL.md                      # Workflow router + core instructions
├── scripts/
│   └── memories_api.py           # Python API client (21 commands)
└── references/
    ├── video_qa.md               # Video Q&A workflow
    ├── social_research.md        # Social media research workflow
    ├── video_notes.md            # Meeting/lecture notes workflow
    ├── knowledge_base.md         # Knowledge base building workflow
    └── api_reference.md          # Complete API command reference
```

## Platform Compatibility

This skill is designed to work across any agent platform that supports the skill format:

| Platform | Status | Install method |
|---|---|---|
| **Claude Code** | Supported | `claude skill install` or copy to `~/.claude/skills/` |
| **OpenClaw** | Supported | Copy to `~/.openclaw/skills/` or reference via config |
| **HappyCapy** | Supported | `claude skill install` (Claude Code compatible) |

The skill uses a standard Python script as its API client -- no platform-specific dependencies. Any agent that can read a `SKILL.md` file and execute `python scripts/memories_api.py` commands will work.

**OpenClaw users**: Because OpenClaw routes through multiple AI models and messaging platforms (WhatsApp, Telegram, Discord, etc.), this skill lets you ask about videos from any conversation channel. The Python client is model-agnostic -- it works regardless of whether OpenClaw dispatches to Claude, GPT, or another model.

## API Commands

21 commands across 6 categories:

| Category | Commands |
|---|---|
| **Video** | `upload_video`, `upload_file`, `list_videos`, `video_status`, `video_info`, `delete_videos`, `transcript`, `wait` |
| **Search** | `search` (private library), `search_public` (TikTok/YouTube/Instagram), `search_audio` |
| **Chat** | `chat_video` (one video), `chat_personal` (entire library + memories) |
| **Memory** | `memory_add`, `memory_search`, `memory_list` |
| **Vision** | `caption_video`, `caption_image` |
| **Import** | `import_url`, `import_hashtag`, `import_creator` |

## Pricing

| Plan | Credits | Price |
|---|---|---|
| Free | 100 credits | $0 (no credit card) |
| Plus | 5,000 credits/month | $15/month |
| Enterprise | Custom | Contact sales |

See [memories.ai/pricing](https://memories.ai/pricing) for per-operation costs.

## Requirements

- Python 3.8+ (standard library only -- zero dependencies)
- Memories.ai API key ([get one free](https://memories.ai/app/service/key))
- Claude Code, OpenClaw, HappyCapy, or any skill-compatible agent platform

## Tested

This skill was validated against **20 real-world test scenarios** covering video Q&A, social media research, meeting summarization, knowledge base building, memory management, and edge cases. See the test suite in the repo for details.

## License

MIT
