#!/usr/bin/env python3
"""
Memories.ai API client for Claude Code skill.

Usage:
    python memories_api.py <command> [args...] [--api-key KEY] [--unique-id ID] [--json]

Commands:
    # Video Management
    upload_video <url> [--tags TAGS] [--callback URL]
    upload_file <path> [--tags TAGS]
    list_videos [--status PARSE|UNPARSE|FAIL] [--page N] [--size N]
    video_status <task_id>
    video_info <video_no>
    delete_videos <video_no> [video_no...]
    transcript <video_no> [--audio]
    wait <video_no> [--timeout SECS]

    # Semantic Search
    search <query> [--top-k N] [--tag TAG] [--video-nos VN1,VN2]
    search_public <query> [--platform TIKTOK|YOUTUBE|INSTAGRAM] [--top-k N]
    search_audio <video_no> <query>

    # Chat
    chat_video <video_no> <prompt> [--session-id N]
    chat_personal <prompt> [--session-id N]

    # Text Memory (MAG)
    memory_add <content> [--tags TAGS]
    memory_search <query> [--page N] [--page-size N]
    memory_list [--page N] [--page-size N]

    # AI Vision / Caption
    caption_video <url> <prompt> [--think]
    caption_image <url> <prompt>

    # Social Media Import
    import_url <url> [--tags TAGS]
    import_hashtag <hashtag> [--platform TIKTOK|YOUTUBE|INSTAGRAM] [--count N]
    import_creator <creator_url> [--count N]

Environment:
    MEMORIES_API_KEY   - API key (or use --api-key)
    MEMORIES_UNIQUE_ID - Namespace (default: "default", or use --unique-id)
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
import urllib.parse
import mimetypes

BASE_URL = "https://api.memories.ai"
VISION_URL = "https://security.memories.ai"


def api_request(path, method="POST", body=None, query=None, base=None, api_key=None):
    """Make an API request to Memories.ai."""
    url = (base or BASE_URL) + path
    if query:
        params = {k: str(v) for k, v in query.items() if v is not None}
        if params:
            url += "?" + urllib.parse.urlencode(params)

    headers = {"Authorization": api_key}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(error_body)
            msg = err.get("msg", error_body)
            code = err.get("code", e.code)
        except json.JSONDecodeError:
            msg = error_body
            code = e.code
        print(json.dumps({"error": True, "code": str(code), "message": msg}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": True, "message": f"Connection error: {e.reason}"}))
        sys.exit(1)

    code = result.get("code")
    if code not in ("0000", 0, "0"):
        msg = result.get("msg", json.dumps(result))
        print(json.dumps({"error": True, "code": str(code), "message": msg}))
        sys.exit(1)

    return result


def upload_file_multipart(path, api_key, unique_id, tags=None):
    """Upload a local video file using multipart/form-data."""
    import io

    boundary = "----MemoriesAiSkillBoundary"
    filename = os.path.basename(path)
    mime_type = mimetypes.guess_type(path)[0] or "video/mp4"

    body_parts = []

    # unique_id field
    body_parts.append(f"--{boundary}\r\n")
    body_parts.append(f'Content-Disposition: form-data; name="unique_id"\r\n\r\n')
    body_parts.append(f"{unique_id}\r\n")

    # tags field
    if tags:
        body_parts.append(f"--{boundary}\r\n")
        body_parts.append(f'Content-Disposition: form-data; name="tags"\r\n\r\n')
        body_parts.append(f"{tags}\r\n")

    # file field
    body_parts.append(f"--{boundary}\r\n")
    body_parts.append(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
    )
    body_parts.append(f"Content-Type: {mime_type}\r\n\r\n")

    header_bytes = "".join(body_parts).encode("utf-8")
    footer_bytes = f"\r\n--{boundary}--\r\n".encode("utf-8")

    with open(path, "rb") as f:
        file_data = f.read()

    data = header_bytes + file_data + footer_bytes

    url = BASE_URL + "/serve/api/v1/upload_file"
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", api_key)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({"error": True, "code": str(e.code), "message": error_body}))
        sys.exit(1)

    return result


# ─── Command Handlers ───────────────────────────────────────────────


def cmd_upload_video(args, api_key, unique_id):
    body = {"url": args.url, "unique_id": unique_id}
    if args.tags:
        body["tags"] = args.tags
    if args.callback:
        body["callback"] = args.callback
    return api_request("/serve/api/v1/upload_url", body=body, api_key=api_key)


def cmd_upload_file(args, api_key, unique_id):
    if not os.path.isfile(args.path):
        print(json.dumps({"error": True, "message": f"File not found: {args.path}"}))
        sys.exit(1)
    return upload_file_multipart(args.path, api_key, unique_id, args.tags)


def cmd_list_videos(args, api_key, unique_id):
    body = {"unique_id": unique_id, "page": args.page, "size": args.size}
    if args.status:
        body["status"] = args.status
    return api_request("/serve/api/v1/list_videos", body=body, api_key=api_key)


def cmd_video_status(args, api_key, unique_id):
    return api_request(
        "/serve/api/v1/get_video_ids_by_task_id",
        method="GET",
        query={"task_id": args.task_id, "unique_id": unique_id},
        api_key=api_key,
    )


def cmd_video_info(args, api_key, unique_id):
    body = {"unique_id": unique_id, "page": 1, "size": 1, "video_no": args.video_no}
    return api_request("/serve/api/v1/list_videos", body=body, api_key=api_key)


def cmd_delete_videos(args, api_key, unique_id):
    return api_request(
        "/serve/api/v1/delete_videos",
        body=args.video_nos,
        query={"unique_id": unique_id},
        api_key=api_key,
    )


def cmd_transcript(args, api_key, unique_id):
    endpoint = (
        "/serve/api/v1/get_audio_transcription"
        if args.audio
        else "/serve/api/v1/get_video_transcription"
    )
    return api_request(
        endpoint,
        method="GET",
        query={"video_no": args.video_no, "unique_id": unique_id},
        api_key=api_key,
    )


def cmd_wait(args, api_key, unique_id):
    """Poll video_info until status is PARSE or timeout."""
    deadline = time.time() + args.timeout
    interval = 5
    while time.time() < deadline:
        body = {
            "unique_id": unique_id,
            "page": 1,
            "size": 1,
            "video_no": args.video_no,
        }
        result = api_request("/serve/api/v1/list_videos", body=body, api_key=api_key)
        records = result.get("data", {}).get("records", [])
        if records and records[0].get("status") == "PARSE":
            return {"status": "ready", "video_no": args.video_no, "data": records[0]}
        print(
            json.dumps(
                {"status": "waiting", "video_no": args.video_no, "elapsed": int(time.time() + args.timeout - deadline)}
            ),
            file=sys.stderr,
        )
        time.sleep(interval)
        interval = min(interval * 1.5, 30)
    print(
        json.dumps(
            {
                "error": True,
                "message": f"Timeout after {args.timeout}s waiting for {args.video_no}",
            }
        )
    )
    sys.exit(1)


def cmd_search(args, api_key, unique_id):
    body = {
        "search_param": args.query,
        "search_type": "BY_VIDEO",
        "unique_id": unique_id,
        "top_k": args.top_k,
    }
    if args.tag:
        body["tag"] = args.tag
    if args.video_nos:
        body["video_nos"] = args.video_nos.split(",")
    return api_request("/serve/api/v1/search", body=body, api_key=api_key)


def cmd_search_public(args, api_key, unique_id):
    body = {
        "search_param": args.query,
        "search_type": "BY_VIDEO",
        "type": args.platform,
        "top_k": args.top_k,
    }
    return api_request("/serve/api/v1/search_public", body=body, api_key=api_key)


def cmd_search_audio(args, api_key, unique_id):
    return api_request(
        "/serve/api/v1/search_audio_transcripts",
        method="GET",
        query={
            "video_no": args.video_no,
            "query": args.query,
            "unique_id": unique_id,
        },
        api_key=api_key,
    )


def cmd_chat_video(args, api_key, unique_id):
    body = {
        "video_nos": [args.video_no],
        "prompt": args.prompt,
        "unique_id": unique_id,
    }
    if args.session_id:
        body["session_id"] = args.session_id
    return api_request("/serve/api/v1/chat", body=body, api_key=api_key)


def cmd_chat_personal(args, api_key, unique_id):
    body = {"prompt": args.prompt, "unique_id": unique_id}
    if args.session_id:
        body["session_id"] = args.session_id
    return api_request("/serve/api/v1/chat_personal", body=body, api_key=api_key)


def cmd_memory_add(args, api_key, unique_id):
    from datetime import datetime, timezone

    body = {
        "unique_id": unique_id,
        "memories": [{"role": "user", "content": args.content}],
        "memories_at": datetime.now(timezone.utc).isoformat(),
    }
    if args.tags:
        body["tags"] = [t.strip() for t in args.tags.split(",")]
    return api_request("/serve/api/v1/memories/add", body=body, api_key=api_key)


def cmd_memory_search(args, api_key, unique_id):
    body = {
        "unique_id": unique_id,
        "query": args.query,
        "page": args.page,
        "page_size": args.page_size,
    }
    return api_request("/serve/api/v1/memories/search", body=body, api_key=api_key)


def cmd_memory_list(args, api_key, unique_id):
    body = {
        "unique_id": unique_id,
        "page": args.page,
        "page_size": args.page_size,
    }
    return api_request("/serve/api/v1/memories", body=body, api_key=api_key)


def cmd_caption_video(args, api_key, unique_id):
    body = {
        "video_url": args.url,
        "user_prompt": args.prompt,
        "system_prompt": "You are a helpful video analyst.",
        "thinking": args.think,
    }
    return api_request(
        "/v1/understand/upload", body=body, base=VISION_URL, api_key=api_key
    )


def cmd_caption_image(args, api_key, unique_id):
    body = {
        "image_url": args.url,
        "user_prompt": args.prompt,
        "system_prompt": "You are a helpful image analyst.",
    }
    return api_request(
        "/v1/understand/uploadImg", body=body, base=VISION_URL, api_key=api_key
    )


def cmd_import_url(args, api_key, unique_id):
    body = {"url": args.url, "unique_id": unique_id}
    if args.tags:
        body["tags"] = args.tags
    return api_request("/serve/api/v1/scraper_url", body=body, api_key=api_key)


def cmd_import_hashtag(args, api_key, unique_id):
    body = {
        "tag": args.hashtag,
        "type": args.platform,
        "count": args.count,
        "unique_id": unique_id,
    }
    return api_request("/serve/api/v1/scraper_tag", body=body, api_key=api_key)


def cmd_import_creator(args, api_key, unique_id):
    body = {"url": args.creator_url, "count": args.count, "unique_id": unique_id}
    return api_request("/serve/api/v1/scraper", body=body, api_key=api_key)


# ─── CLI Parser ─────────────────────────────────────────────────────


def build_parser():
    parser = argparse.ArgumentParser(
        description="Memories.ai API client", prog="memories_api"
    )
    parser.add_argument("--api-key", help="API key (or set MEMORIES_API_KEY env var)")
    parser.add_argument(
        "--unique-id", help="Namespace (or set MEMORIES_UNIQUE_ID env var)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # upload_video
    p = sub.add_parser("upload_video", help="Upload video from URL")
    p.add_argument("url", help="Video URL")
    p.add_argument("--tags", help="Comma-separated tags")
    p.add_argument("--callback", help="Webhook callback URL")

    # upload_file
    p = sub.add_parser("upload_file", help="Upload local video file")
    p.add_argument("path", help="Path to video file")
    p.add_argument("--tags", help="Comma-separated tags")

    # list_videos
    p = sub.add_parser("list_videos", help="List indexed videos")
    p.add_argument("--status", choices=["PARSE", "UNPARSE", "FAIL"])
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=20)

    # video_status
    p = sub.add_parser("video_status", help="Check task processing status")
    p.add_argument("task_id", help="Task ID from upload")

    # video_info
    p = sub.add_parser("video_info", help="Get video details by video_no")
    p.add_argument("video_no", help="Video number")

    # delete_videos
    p = sub.add_parser("delete_videos", help="Delete videos")
    p.add_argument("video_nos", nargs="+", help="Video numbers to delete")

    # transcript
    p = sub.add_parser("transcript", help="Get video transcription")
    p.add_argument("video_no", help="Video number")
    p.add_argument("--audio", action="store_true", help="Get audio transcript instead")

    # wait
    p = sub.add_parser("wait", help="Wait for video processing to complete")
    p.add_argument("video_no", help="Video number")
    p.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")

    # search
    p = sub.add_parser("search", help="Search private video library")
    p.add_argument("query", help="Search query")
    p.add_argument("--top-k", type=int, default=10)
    p.add_argument("--tag", help="Filter by tag")
    p.add_argument("--video-nos", help="Comma-separated video numbers to search within")

    # search_public
    p = sub.add_parser("search_public", help="Search public platforms")
    p.add_argument("query", help="Search query")
    p.add_argument(
        "--platform", choices=["TIKTOK", "YOUTUBE", "INSTAGRAM"], default="YOUTUBE"
    )
    p.add_argument("--top-k", type=int, default=10)

    # search_audio
    p = sub.add_parser("search_audio", help="Search audio transcripts")
    p.add_argument("video_no", help="Video number")
    p.add_argument("query", help="Search query")

    # chat_video
    p = sub.add_parser("chat_video", help="Chat about a specific video")
    p.add_argument("video_no", help="Video number")
    p.add_argument("prompt", help="Your question")
    p.add_argument("--session-id", type=int, help="Session ID for multi-turn")

    # chat_personal
    p = sub.add_parser("chat_personal", help="Chat across personal library")
    p.add_argument("prompt", help="Your question")
    p.add_argument("--session-id", type=int, help="Session ID for multi-turn")

    # memory_add
    p = sub.add_parser("memory_add", help="Store a text memory")
    p.add_argument("content", help="Text content to store")
    p.add_argument("--tags", help="Comma-separated tags")

    # memory_search
    p = sub.add_parser("memory_search", help="Search memories")
    p.add_argument("query", help="Search query")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int, default=20)

    # memory_list
    p = sub.add_parser("memory_list", help="List all memories")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", type=int, default=20)

    # caption_video
    p = sub.add_parser("caption_video", help="Analyze video without uploading")
    p.add_argument("url", help="Video URL")
    p.add_argument("prompt", help="Analysis prompt")
    p.add_argument("--think", action="store_true", help="Enable reasoning mode")

    # caption_image
    p = sub.add_parser("caption_image", help="Analyze image")
    p.add_argument("url", help="Image URL")
    p.add_argument("prompt", help="Analysis prompt")

    # import_url
    p = sub.add_parser("import_url", help="Import from social media URL")
    p.add_argument("url", help="Social media video URL")
    p.add_argument("--tags", help="Comma-separated tags")

    # import_hashtag
    p = sub.add_parser("import_hashtag", help="Import by hashtag")
    p.add_argument("hashtag", help="Hashtag (without #)")
    p.add_argument(
        "--platform", choices=["TIKTOK", "YOUTUBE", "INSTAGRAM"], default="TIKTOK"
    )
    p.add_argument("--count", type=int, default=10)

    # import_creator
    p = sub.add_parser("import_creator", help="Import from creator profile")
    p.add_argument("creator_url", help="Creator profile URL")
    p.add_argument("--count", type=int, default=10)

    return parser


COMMANDS = {
    "upload_video": cmd_upload_video,
    "upload_file": cmd_upload_file,
    "list_videos": cmd_list_videos,
    "video_status": cmd_video_status,
    "video_info": cmd_video_info,
    "delete_videos": cmd_delete_videos,
    "transcript": cmd_transcript,
    "wait": cmd_wait,
    "search": cmd_search,
    "search_public": cmd_search_public,
    "search_audio": cmd_search_audio,
    "chat_video": cmd_chat_video,
    "chat_personal": cmd_chat_personal,
    "memory_add": cmd_memory_add,
    "memory_search": cmd_memory_search,
    "memory_list": cmd_memory_list,
    "caption_video": cmd_caption_video,
    "caption_image": cmd_caption_image,
    "import_url": cmd_import_url,
    "import_hashtag": cmd_import_hashtag,
    "import_creator": cmd_import_creator,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("MEMORIES_API_KEY")
    if not api_key:
        print(
            json.dumps(
                {
                    "error": True,
                    "message": "No API key. Set MEMORIES_API_KEY env var or use --api-key. "
                    "Get your key at: https://memories.ai/app/service/key",
                }
            )
        )
        sys.exit(1)

    unique_id = args.unique_id or os.environ.get("MEMORIES_UNIQUE_ID", "default")

    handler = COMMANDS[args.command]
    result = handler(args, api_key, unique_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
