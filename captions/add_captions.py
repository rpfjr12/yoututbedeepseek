"""
Adds captions to stick figure videos using FFmpeg.
If FFmpeg is not available, copies videos to output folder.
"""

import os
import sys
import glob
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

def add_captions_to_video(input_path, output_path, caption_text):
    """Add a simple caption overlay using FFmpeg."""
    # Simple caption at bottom of video
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vf", f"drawtext=text='{caption_text}':fontfile=Arial:fontsize=36:fontcolor=black:x=(w-text_w)/2:y=h-100:enable='between(t,0,5)'",
        "-c:a", "copy",
        "-y",
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def process_videos():
    """Add captions to all animation videos."""
    os.makedirs(CAPTIONS_DIR, exist_ok=True)
    
    ffmpeg_available = check_ffmpeg()
    
    if not ffmpeg_available:
        print("FFmpeg not found. Copying videos without captions.")
    
    # Get all animation videos
    video_files = sorted(glob.glob(os.path.join(ANIMATION_DIR, "*.mp4")))
    
    if not video_files:
        print("No videos found. Run animation script first.")
        return
    
    for video_file in video_files:
        base_name = os.path.basename(video_file)
        output_file = os.path.join(CAPTIONS_DIR, base_name)
        
        if ffmpeg_available:
            # Get caption from script file
            script_file = video_file.replace("animations_output", "scripts_output").replace(".mp4", ".txt")
            caption_text = "Watch till the end"  # Default caption
            
            if os.path.exists(script_file):
                with open(script_file, "r") as f:
                    lines = f.readlines()
                    if len(lines) > 3:
                        caption_text = lines[3].strip()
            
            print(f"Adding captions to: {base_name}")
            success = add_captions_to_video(video_file, output_file, caption_text)
            
            if success:
                print(f"Saved: {output_file}")
            else:
                print(f"Failed to add captions. Copying original.")
                import shutil
                shutil.copy2(video_file, output_file)
        else:
            # Just copy the file
            import shutil
            shutil.copy2(video_file, output_file)
            print(f"Copied: {output_file}")
    
    print("\nAll videos processed!")

if __name__ == "__main__":
    process_videos()
