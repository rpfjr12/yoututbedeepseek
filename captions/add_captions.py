"""
Adds captions to stick figure videos using FFmpeg.
If FFmpeg is not available, copies videos to output folder.
"""

import os
import sys
import glob
import shutil
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAPTIONS_DIR, ANIMATION_DIR

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.FileNotFoundError, subprocess.CalledProcessError):
        return False

def escape_ffmpeg_text(text):
    """Escape special characters for FFmpeg drawtext filter."""
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "'\\\\''")
    text = text.replace(":", "\\:")
    text = text.replace("=", "\\=")
    text = text.replace("%", "%%")
    return text

def add_captions_to_video(input_path, output_path, caption_text):
    """Add a simple caption overlay using FFmpeg."""
    safe_text = escape_ffmpeg_text(caption_text)
    
    # Use DejaVu font (available on Ubuntu)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    # If font doesn't exist, try to find any available font
    if not os.path.exists(font_path):
        possible_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ]
        for pf in possible_fonts:
            if os.path.exists(pf):
                font_path = pf
                break
    
    drawtext_filter = (
        f"drawtext=fontfile={font_path}:"
        f"text='{safe_text}':"
        f"fontsize=48:"
        f"fontcolor=white:"
        f"box=1:"
        f"boxcolor=black@0.7:"
        f"boxborderw=10:"
        f"x=(w-text_w)/2:"
        f"y=h-150:"
        f"enable='between(t,0,3)'"
    )
    
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", drawtext_filter,
        "-c:a", "copy",
        "-y",
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr[:500]}")
        return False

def process_videos():
    """Add captions to all animation videos."""
    os.makedirs(CAPTIONS_DIR, exist_ok=True)
    
    ffmpeg_available = check_ffmpeg()
    print(f"FFmpeg available: {ffmpeg_available}")
    
    # Get all animation videos
    video_files = sorted(glob.glob(os.path.join(ANIMATION_DIR, "*.mp4")))
    
    if not video_files:
        print(f"No videos found in {ANIMATION_DIR}. Run animation script first.")
        return
    
    for video_file in video_files:
        base_name = os.path.basename(video_file)
        output_file = os.path.join(CAPTIONS_DIR, base_name)
        
        # Skip if already exists
        if os.path.exists(output_file):
            print(f"Already exists: {output_file}")
            continue
        
        # Get caption from script file
        script_file = video_file.replace("animations_output", "scripts_output").replace(".mp4", ".txt")
        caption_text = "Watch till the end"  # Default caption
        
        if os.path.exists(script_file):
            with open(script_file, "r") as f:
                lines = f.readlines()
                for line in lines[3:]:
                    if line.strip():
                        caption_text = line.strip()
                        break
        
        if ffmpeg_available:
            print(f"Adding captions to: {base_name}")
            success = add_captions_to_video(video_file, output_file, caption_text)
            
            if success:
                print(f"Saved: {output_file}")
            else:
                print(f"FFmpeg failed. Copying original.")
                shutil.copy2(video_file, output_file)
        else:
            shutil.copy2(video_file, output_file)
            print(f"Copied (no FFmpeg): {output_file}")
    
    print("\nAll videos processed!")

if __name__ == "__main__":
    process_videos()
