#!/usr/bin/env python3
"""
build_tiktok_video.py

End-to-End Autonomous TikTok Video Generator for UEFA Champions League Tracker.
1. Generates data-driven script & storyboard
2. Headless renders 1080x1920 9:16 visual cards via Chrome/Edge
3. Synthesizes neural voiceover via edge-tts
4. Assembles full video with Ken Burns motion, text overlays, and subtitles using FFmpeg
5. Emits production-ready MP4 + posting metadata
"""

import os
import sys
import json
import re
import asyncio
import subprocess
import argparse
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import edge_tts
import imageio_ffmpeg

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "output"
FRAMES_DIR = OUTPUT_DIR / "frames"
AUDIO_DIR = OUTPUT_DIR / "audio"
CLIPS_DIR = OUTPUT_DIR / "clips"

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def ensure_dirs():
    for d in [OUTPUT_DIR, FRAMES_DIR, AUDIO_DIR, CLIPS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def run_command(cmd, desc):
    print(f"▶ {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"❌ Error in {desc}:")
        print(res.stderr[:800])
        sys.exit(1)
    return res

def get_audio_duration(audio_path):
    cmd = [FFMPEG_EXE, "-i", str(audio_path)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 5.0

async def synthesize_speech(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(str(out_path))

def render_scene_clip(frame_path, audio_path, duration, caption, zoom_dir, out_clip_path):
    fps = 30
    total_frames = max(30, int(duration * fps))
    
    # Smooth Ken Burns zoom: in (1.0 -> 1.05) or out (1.05 -> 1.0)
    if zoom_dir == "out":
        zoom_expr = f"min(1.05-on*0.0004,1.05)"
    else:
        zoom_expr = f"min(1.0+on*0.0004,1.06)"
        
    safe_caption = caption.replace("'", "").replace(":", "-").replace('"', '')
    
    # FFmpeg filter: zoompan + high-contrast TikTok pill caption
    filter_complex = (
        f"zoompan=z='{zoom_expr}':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},"
        f"drawtext=text='{safe_caption}':fontcolor=white:fontsize=44:box=1:boxcolor=black@0.65:boxborderw=16:x=(w-text_w)/2:y=h-240"
    )
    
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-loop", "1",
        "-i", str(frame_path),
        "-i", str(audio_path),
        "-vf", filter_complex,
        "-t", f"{duration:.2f}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(out_clip_path)
    ]
    
    run_command(cmd, f"Rendering clip {out_clip_path.name} ({duration:.1f}s)")

def concatenate_clips(clip_paths, final_output_path):
    concat_list_path = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in clip_paths:
            # Format path for ffmpeg concat
            f.write(f"file '{p.resolve().as_posix()}'\n")
            
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(final_output_path)
    ]
    
    run_command(cmd, "Concatenating full video")

def main():
    parser = argparse.ArgumentParser(description="Autonomous TikTok Video Generator")
    parser.add_argument("--type", choices=["match", "standings"], default="match", help="Type of video to produce")
    parser.add_argument("--home", type=str, default=None, help="Home team override")
    parser.add_argument("--away", type=str, default=None, help="Away team override")
    parser.add_argument("--voice", type=str, default="en-GB-RyanNeural", help="Neural voice name (e.g. en-GB-RyanNeural, en-US-ChristopherNeural)")
    parser.add_argument("--matchdays-only", action="store_true", help="Only run if Champions League matches are scheduled today")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DIR / "cl_tiktok_video.mp4"), help="Final MP4 destination")
    args = parser.parse_args()

    ensure_dirs()

    # Check matchdays-only if requested
    if args.matchdays_only:
        from datetime import datetime, timezone
        standings_file = ROOT_DIR / "data" / "standings.json"
        if standings_file.exists():
            with open(standings_file, "r", encoding="utf-8") as f:
                s_data = json.load(f)
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            today_matches = [m for m in s_data.get("matches", []) if m.get("date", "").startswith(today_str)]
            if not today_matches:
                print(f"⚽ [MATCHDAY CHECK] No Champions League matches scheduled for today ({today_str}).")
                print("Skipping video creation as --matchdays-only is active. Exiting cleanly.")
                sys.exit(10)
            else:
                print(f"🔥 [MATCHDAY CHECK] Matchday confirmed! {len(today_matches)} matches scheduled today.")
    print("=" * 60)
    print("🏆 CL LEAGUE TRACKER • AI TIKTOK VIDEO PIPELINE")
    print("=" * 60)

    # 1. Generate Storyboard & Narration Script
    storyboard_path = OUTPUT_DIR / "storyboard.json"
    script_cmd = [
        sys.executable,
        str(ROOT_DIR / "scripts" / "generate_tiktok_script.py"),
        "--type", args.type,
        "--output", str(storyboard_path)
    ]
    if args.home and args.away:
        script_cmd.extend(["--home", args.home, "--away", args.away])
        
    run_command(script_cmd, "Generating AI script and storyboard")

    with open(storyboard_path, "r", encoding="utf-8") as f:
        storyboard = json.load(f)

    scenes = storyboard.get("scenes", [])
    meta = storyboard.get("meta", {})
    print(f"\n🎬 Title: {meta.get('title')}")
    print(f"🎙 Voice: {args.voice}")
    print(f"📑 Scenes: {len(scenes)}")

    # 2. Render 1080x1920 Canvas Cards Headlessly
    render_script = ROOT_DIR / "scripts" / "render_card_headless.mjs"
    render_cmd = ["node", str(render_script), str(storyboard_path), str(FRAMES_DIR)]
    run_command(render_cmd, "Headless rendering 1080x1920 cards via browser")

    # 3. Synthesize Audio & Build Video Clips
    clip_paths = []
    total_duration = 0.0

    for i, scene in enumerate(scenes):
        s_id = scene.get("id", f"scene_{i+1}")
        frame_file = FRAMES_DIR / f"{s_id}.png"
        audio_file = AUDIO_DIR / f"{s_id}.mp3"
        clip_file = CLIPS_DIR / f"{s_id}.mp4"

        voice_text = scene.get("voice_text", "")
        caption = scene.get("caption", "")
        zoom_dir = scene.get("zoom_direction", "in")

        # Synthesize audio
        print(f"\n🎙 [Scene {i+1}/{len(scenes)}] Synthesizing speech: \"{voice_text[:45]}...\"")
        asyncio.run(synthesize_speech(voice_text, args.voice, audio_file))

        # Measure audio duration
        dur = get_audio_duration(audio_file)
        # Add 0.3s cushion for natural pacing
        dur = dur + 0.3
        total_duration += dur

        # Render clip
        render_scene_clip(frame_file, audio_file, dur, caption, zoom_dir, clip_file)
        clip_paths.append(clip_file)

    # 4. Concatenate All Clips
    final_mp4 = Path(args.output)
    concatenate_clips(clip_paths, final_mp4)

    # 5. Save Publishing Metadata
    post_meta_path = OUTPUT_DIR / "tiktok_post.json"
    post_meta = {
        "video_path": str(final_mp4.resolve()),
        "title": meta.get("title", "Champions League AI Prediction"),
        "description": meta.get("description", "#UCL #ChampionsLeague #Football #Predictions"),
        "duration_seconds": round(total_duration, 1),
        "resolution": "1080x1920 (9:16)",
        "scenes_count": len(scenes)
    }

    with open(post_meta_path, "w", encoding="utf-8") as f:
        json.dump(post_meta, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("🎉 TIKTOK VIDEO SUCCESSFULLY CREATED!")
    print("=" * 60)
    print(f"📹 Output MP4: {final_mp4}")
    print(f"⏱ Total Length: {total_duration:.1f}s")
    print(f"📋 Caption & Hashtags:\n")
    print(post_meta["description"])
    print("=" * 60)

if __name__ == "__main__":
    main()
