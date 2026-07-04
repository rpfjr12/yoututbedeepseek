"""
Prepares final upload files by copying captioned videos to output folder.
"""

import os
import sys
import glob
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAPTIONS_DIR, THUMBNAIL_DIR, FINAL_OUTPUT_DIR

def prepare_upload_files():
    """Copy final videos and thumbnails to output folder."""
    os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)
    
    # Get all captioned videos
    video_files = sorted(glob.glob(os.path.join(CAPTIONS_DIR, "*.mp4")))
    
    if not video_files:
        print(f"No videos found in {CAPTIONS_DIR}. Run captions script first.")
        return
    
    copied_count = 0
    
    for video_file in video_files:
        base_name = os.path.basename(video_file)
        video_output = os.path.join(FINAL_OUTPUT_DIR, base_name)
        
        # Copy video
        if not os.path.exists(video_output):
            shutil.copy2(video_file, video_output)
            print(f"Video: {base_name}")
            copied_count += 1
        else:
            print(f"Already exists: {base_name}")
        
        # Copy matching thumbnail
        thumb_name = base_name.replace(".mp4", ".png")
        thumb_source = os.path.join(THUMBNAIL_DIR, thumb_name)
        thumb_output = os.path.join(FINAL_OUTPUT_DIR, thumb_name)
        
        if os.path.exists(thumb_source) and not os.path.exists(thumb_output):
            shutil.copy2(thumb_source, thumb_output)
            print(f"Thumbnail: {thumb_name}")
    
    # List final output
    final_files = os.listdir(FINAL_OUTPUT_DIR)
    print(f"\n{'='*60}")
    print(f"Upload folder ready: {FINAL_OUTPUT_DIR}")
    print(f"Total files: {len(final_files)}")
    for f in sorted(final_files):
        size = os.path.getsize(os.path.join(FINAL_OUTPUT_DIR, f))
        print(f"  - {f} ({size/1024/1024:.1f} MB)")
    print(f"{'='*60}")

if __name__ == "__main__":
    prepare_upload_files()
