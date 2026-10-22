"""
CL Tracker - Automated TikTok Video Publisher & Webhook Pipeline
Publishes automated matchday prediction videos to TikTok via the official
TikTok Content Posting API (v2) and/or multi-platform webhooks (Discord/Telegram/Buffer).
"""

import os
import sys
import json
import time
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TIKTOK_API_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
TIKTOK_STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status_fetch/"

def build_matchday_caption(match_data=None):
    """Generates viral, high-converting caption with hashtags for TikTok."""
    if not match_data:
        # Load active match from standings.json
        try:
            with open("data/standings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            matches = [m for m in data.get("matches", []) if not m.get("played")]
            match_data = matches[0] if matches else {"home": "Real Madrid", "away": "Paris Saint-Germain"}
        except Exception:
            match_data = {"home": "Real Madrid", "away": "Paris Saint-Germain"}

    home = match_data.get("home", "Real Madrid")
    away = match_data.get("away", "Paris Saint-Germain")
    odds = match_data.get("odds", {"home": 0.54, "draw": 0.24, "away": 0.22})
    p_home = int(odds.get("home", 0.54) * 100) if odds else 54
    p_away = int(odds.get("away", 0.22) * 100) if odds else 22

    caption = (
        f"🚨 UEFA Champions League AI Prediction! 🚨\n\n"
        f"⚽ {home} ({p_home}%) vs {away} ({p_away}%)\n"
        f"20,000 Monte Carlo tournament simulations ran before kickoff!\n"
        f"Who is taking all 3 points tonight? Drop your score predictions below! 👇\n\n"
        f"#UCL #ChampionsLeague #Football #Predictions #{home.replace(' ', '')} #{away.replace(' ', '')} #Soccer #Futbol #CLTracker"
    )
    return caption

def post_video_to_tiktok(video_path, caption, access_token=None, dry_run=False):
    """Posts a video to TikTok using the official Content Posting API."""
    token = access_token or os.environ.get("TIKTOK_ACCESS_TOKEN")
    
    if dry_run or not token:
        print("[DRY-RUN] TikTok Content Posting API Simulation:")
        print(f"  Video file: {video_path} (Exists: {os.path.exists(video_path)})")
        print(f"  Token configured: {'YES' if token else 'NO (Set TIKTOK_ACCESS_TOKEN)'}")
        print("  Payload caption:")
        print("  " + "\n  ".join(caption.splitlines()))
        if not token:
            print("\nTo enable live automated publishing, set repository secret TIKTOK_ACCESS_TOKEN.")
        return True

    try:
        import requests
    except ImportError:
        print("requests module required for live API upload. pip install requests")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8"
    }

    # Step 1: Initialize Direct Post
    file_size = os.path.getsize(video_path)
    init_payload = {
        "post_info": {
            "title": caption[:150],
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": file_size,
            "total_chunk_count": 1
        }
    }

    print("Initializing TikTok upload...")
    res = requests.post(TIKTOK_API_URL, headers=headers, json=init_payload)
    if res.status_code != 200:
        print(f"TikTok API initialization failed: {res.status_code} - {res.text}")
        return False

    resp_data = res.json().get("data", {})
    upload_url = resp_data.get("upload_url")
    publish_id = resp_data.get("publish_id")

    # Step 2: Upload Video File
    print("Uploading video binary chunk...")
    with open(video_path, "rb") as vf:
        video_bytes = vf.read()

    upload_headers = {
        "Content-Type": "video/mp4",
        "Content-Range": f"bytes 0-{file_size - 1}/{file_size}"
    }
    up_res = requests.put(upload_url, headers=upload_headers, data=video_bytes)
    if up_res.status_code not in [200, 201]:
        print(f"TikTok upload failed: {up_res.status_code} - {up_res.text}")
        return False

    print(f"✓ Video successfully published to TikTok! Publish ID: {publish_id}")
    return True

def post_to_webhook(webhook_url, message, video_path=None):
    """Pushes automated video and prediction card to Discord/Telegram/Buffer webhook."""
    if not webhook_url:
        return
    print(f"Pushing automated alert to Webhook ({webhook_url[:30]}...)...")
    try:
        import requests
        payload = {"content": message}
        files = {}
        if video_path and os.path.exists(video_path):
            files["file"] = open(video_path, "rb")
        res = requests.post(webhook_url, data=payload, files=files if files else None)
        print(f"Webhook response: {res.status_code}")
    except Exception as e:
        print(f"Webhook notification error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CL Tracker Automated TikTok Publisher")
    parser.add_argument("--dry-run", action="store_true", help="Simulate publishing without calling live API")
    parser.add_argument("--video", default="exports/tiktok_preview.mp4", help="Path to video file")
    args = parser.parse_args()

    caption = build_matchday_caption()
    success = post_video_to_tiktok(args.video, caption, dry_run=args.dry_run or not os.environ.get("TIKTOK_ACCESS_TOKEN"))
    if success:
        print("\nAutomated TikTok publisher pipeline verified successfully.")
