import subprocess
import json
import os
import sys
import re

CHANNEL_URL = "https://www.youtube.com/@digitalcreatoravi/videos"
OUTPUT_DIR = "research/digital-creator-avi"
TRANSCRIPTS_DIR = os.path.join(OUTPUT_DIR, "transcripts")

os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

def get_playlist_entries():
    print(f"Fetching playlist entries from {CHANNEL_URL}...")
    cmd = ["yt-dlp", "--dump-single-json", "--flat-playlist", CHANNEL_URL]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        print("Error fetching playlist:", res.stderr)
        return []
    data = json.loads(res.stdout)
    entries = data.get("entries", [])
    print(f"Total video entries found: {len(entries)}")
    return entries

def clean_vtt(vtt_path):
    if not os.path.exists(vtt_path):
        return ""
    with open(vtt_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    text_lines = []
    seen = set()
    for line in lines:
        line = line.strip()
        if not line or "-->" in line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean not in seen:
            text_lines.append(clean)
            seen.add(clean)
    return " ".join(text_lines)

def fetch_details_and_subtitles(entries, limit=45):
    detailed_videos = []
    selected_entries = entries[:limit]
    
    for idx, entry in enumerate(selected_entries):
        video_id = entry.get("id")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"[{idx+1}/{len(selected_entries)}] Processing: {entry.get('title')} ({video_id})")
        
        # Get full json metadata
        meta_cmd = ["yt-dlp", "--dump-json", "--skip-download", video_url]
        meta_res = subprocess.run(meta_cmd, capture_output=True, text=True, encoding="utf-8")
        meta = {}
        if meta_res.returncode == 0 and meta_res.stdout.strip():
            try:
                meta = json.loads(meta_res.stdout)
            except Exception as e:
                print(f"  Error parsing metadata for {video_id}: {e}")
        
        # Download subtitle
        vtt_target = os.path.join(TRANSCRIPTS_DIR, f"{video_id}")
        expected_vtt = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.en.vtt")
        txt_target = os.path.join(TRANSCRIPTS_DIR, f"{video_id}.txt")
        
        transcript_text = ""
        if not os.path.exists(txt_target):
            sub_cmd = [
                "yt-dlp",
                "--skip-download",
                "--write-auto-sub",
                "--sub-lang", "en",
                "--output", f"{vtt_target}.%(ext)s",
                video_url
            ]
            subprocess.run(sub_cmd, capture_output=True, text=True, encoding="utf-8")
            
            transcript_text = clean_vtt(expected_vtt)
            if transcript_text:
                with open(txt_target, "w", encoding="utf-8") as tf:
                    tf.write(transcript_text)
                print(f"  Saved transcript ({len(transcript_text)} chars)")
            else:
                print("  No transcript found or empty")
        else:
            with open(txt_target, "r", encoding="utf-8") as tf:
                transcript_text = tf.read()
            print(f"  Loaded existing transcript ({len(transcript_text)} chars)")
            
        video_record = {
            "id": video_id,
            "title": meta.get("title", entry.get("title")),
            "url": video_url,
            "upload_date": meta.get("upload_date"),
            "view_count": meta.get("view_count"),
            "duration": meta.get("duration"),
            "duration_string": meta.get("duration_string", entry.get("duration_string")),
            "description": meta.get("description", ""),
            "tags": meta.get("tags", []),
            "has_transcript": bool(transcript_text),
            "transcript_len": len(transcript_text)
        }
        detailed_videos.append(video_record)
        
    with open(os.path.join(OUTPUT_DIR, "videos_raw.json"), "w", encoding="utf-8") as f:
        json.dump(detailed_videos, f, indent=2)
    print(f"Successfully saved {len(detailed_videos)} video records to {OUTPUT_DIR}/videos_raw.json")

if __name__ == "__main__":
    entries = get_playlist_entries()
    fetch_details_and_subtitles(entries, limit=45)
