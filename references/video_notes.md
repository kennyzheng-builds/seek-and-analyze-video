# Video Summarization & Notes Workflow

Convert video content into structured summaries, notes, and key takeaways.

## When to Use

- User says "summarize this video", "take notes from this lecture"
- User has a meeting recording and wants action items
- User wants to extract key points from a webinar or presentation
- User asks for a transcript of a video
- User says "what were the main topics discussed"

## Workflow

**Step 1: Upload the video**
```bash
python scripts/memories_api.py upload_video "<VIDEO_URL>" --tags "notes"
```
Extract `videoNo` from the response.

**Step 2: Wait for processing**
```bash
python scripts/memories_api.py wait "<VIDEO_NO>" --timeout 600
```

**Step 3: Get transcriptions**

Get both visual and audio transcriptions for comprehensive notes:
```bash
python scripts/memories_api.py transcript "<VIDEO_NO>"
python scripts/memories_api.py transcript "<VIDEO_NO>" --audio
```

- Visual transcript: scene descriptions, what's shown on screen
- Audio transcript: spoken words with timestamps

**Step 4: Generate structured summary**
```bash
python scripts/memories_api.py chat_video "<VIDEO_NO>" "Provide a comprehensive summary of this video with: 1) Main topics covered 2) Key points for each topic 3) Any action items or takeaways 4) Important quotes or statements"
```

**Step 5: Deep dive on specifics (optional)**
```bash
python scripts/memories_api.py chat_video "<VIDEO_NO>" "What specific recommendations were made?" --session-id 1
python scripts/memories_api.py chat_video "<VIDEO_NO>" "Were there any disagreements or debates?" --session-id 1
```
Use `--session-id` to maintain conversation context across multiple questions.

**Step 6: Store summary as memory (optional)**
```bash
python scripts/memories_api.py memory_add "Summary of <video title>: ..." --tags "notes,meeting"
```

## Output Formats by Context

### Meeting Notes
```
## Meeting Summary
**Date**: ...
**Participants**: (from speaker recognition)
**Duration**: ...

### Key Decisions
- ...

### Action Items
- [ ] ...

### Discussion Points
- ...
```

### Lecture Notes
```
## Lecture: <Title>
### Topic 1: ...
- Key concept: ...
- Examples given: ...

### Topic 2: ...
- Key concept: ...

### Key Takeaways
1. ...
```

### Webinar/Presentation Summary
```
## Presentation Summary
### Main Argument
...

### Supporting Points
1. ...

### Data & Evidence Cited
- ...

### Q&A Highlights
- ...
```

## Tips

- For long videos (>30 min), get transcript first, then use targeted chat questions
- Audio transcript is essential for meetings; visual transcript adds value for presentations with slides
- Use `search_audio` to find specific moments: `search_audio <VIDEO_NO> "budget discussion"`
- Store summaries as memories so they're searchable via `chat_personal` later
