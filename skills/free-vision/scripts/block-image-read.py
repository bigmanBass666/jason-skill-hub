#!/usr/bin/env python3
"""PreToolUse hook: block Read tool from opening image files.

Controlled by VISION_BLOCK_READ env var (=1 to enable blocking).
When blocked, outputs JSON decision so Claude sees the reason and can use
free-vision skill instead of crashing on a text-only model.
"""
import json
import os
import sys

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.ico'}

def main():
    if os.environ.get('VISION_BLOCK_READ') != '1':
        return

    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    file_path = data.get('tool_input', {}).get('file_path', '')
    if not file_path:
        return

    _, ext = os.path.splitext(file_path)
    if ext.lower() not in IMAGE_EXTS:
        return

    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Image file detected. The current model is text-only "
                "and cannot process images. Use the free-vision skill instead: "
                "call the script at ~/.agents/skills/free-vision/scripts/vision_read.py "
                "with the image path."
            )
        }
    }, sys.stdout)

if __name__ == '__main__':
    main()
