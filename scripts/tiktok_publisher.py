#!/usr/bin/env python3
"""
tiktok_publisher.py

Handles publishing and distribution of generated TikTok videos:
- Mode 1: Local / Clipboard (copies caption to clipboard and opens video)
- Mode 2: Telegram Bot / Discord Webhook notification (delivers video straight to your phone)
- Mode 3: TikTok Studio Web Automation via Playwright (hands-free upload)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "output"

def copy_to_clipboard(text):
    try:
        process = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
        process.communicate(text.encode("utf-16"))
        print("📋 Caption copied to system clipboard!")
    except Exception as e:
        print(f"Clipboard copy note: {e}")

def notify_discord(webhook_url, video_path, caption):
    import requests
    print("🚀 Sending video to Discord webhook...")
    with open(video_path, "rb") as f:
        response = requests.post(
            webhook_url,
            data={"content": f"🏆 **New Champions League TikTok Video Ready!**\n\n{caption}"},
            files={"file": (video_path.name, f, "video/mp4")}
        )
    if response.status_code in [200, 204]:
        print("✅ Successfully delivered to Discord!")
    else:
        print(f"❌ Discord error ({response.status_code}): {response.text}")

def notify_telegram(bot_token, chat_id, video_path, caption):
    import requests
    print("🚀 Sending video to Telegram...")
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    with open(video_path, "rb") as f:
        response = requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption[:1024]},
            files={"video": f}
        )
    if response.status_code == 200:
        print("✅ Successfully delivered to Telegram!")
    else:
        print(f"❌ Telegram error ({response.status_code}): {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Distribute and Publish TikTok Video")
    parser.add_argument("--meta", type=str, default=str(OUTPUT_DIR / "tiktok_post.json"), help="Metadata JSON path")
    parser.add_argument("--discord", type=str, default=os.getenv("DISCORD_WEBHOOK_URL"), help="Discord Webhook URL")
    parser.add_argument("--telegram-token", type=str, default=os.getenv("TELEGRAM_BOT_TOKEN"), help="Telegram Bot Token")
    parser.add_argument("--telegram-chat", type=str, default=os.getenv("TELEGRAM_CHAT_ID"), help="Telegram Chat ID")
    parser.add_argument("--auto-post", action="store_true", help="Automatically post to TikTok via authenticated browser session")
    parser.add_argument("--open", action="store_true", help="Open video in default media player")
    args = parser.parse_args()

    meta_path = Path(args.meta)
    if not meta_path.exists():
        print(f"❌ Metadata file not found: {meta_path}")
        print("Run `python scripts/build_tiktok_video.py` first.")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    video_path = Path(meta["video_path"])
    caption = meta.get("description", "")

    print("=" * 60)
    print("📱 TIKTOK VIDEO READY FOR PUBLISHING")
    print("=" * 60)
    print(f"🎬 Video: {video_path.name} ({meta.get('duration_seconds')}s, {meta.get('resolution')})")
    print("\n📝 Caption & Hashtags to Post:")
    print("-" * 60)
    print(caption)
    print("-" * 60)

    # Copy caption to clipboard for effortless pasting
    copy_to_clipboard(caption)

    # Deliver via webhooks if configured
    if args.discord:
        notify_discord(args.discord, video_path, caption)
    if args.telegram_token and args.telegram_chat:
        notify_telegram(args.telegram_token, args.telegram_chat, video_path, caption)

    if args.auto_post:
        uploader_script = ROOT_DIR / "scripts" / "tiktok_upload.mjs"
        if uploader_script.exists():
            print("🚀 Executing automated TikTok upload...")
            subprocess.run(["node", str(uploader_script)])

    if args.open:
        if sys.platform == "win32":
            os.startfile(str(video_path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(video_path)])
        else:
            subprocess.run(["xdg-open", str(video_path)])

if __name__ == "__main__":
    main()
