"""
Prepares final upload files by copying outputs to a single folder.
"""

import os
import sys
import shutil
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAPTIONS_DIR, THUMBNAIL_DIR, FINAL_OUTPUT_DIR

def prepare_upload():
    """Copy all final files to the output folder."""
    os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)
    
    # Copy captioned videos
    video_files = sorted(glob.glob(os.path.join(CAPTIONS_DIR, "*.mp4")))
    for video_path in video_files:
        filename = os.path.basename(video_path)
        dest_path = os.path.join(FINAL_OUTPUT_DIR, filename)
        shutil.copy2(video_path, dest_path)
        print(f"Copied video: {dest_path}")
    
    # Copy thumbnails
    thumbnail_files = sorted(glob.glob(os.path.join(THUMBNAIL_DIR, "*.png")))
    for thumb_path in thumbnail_files:
        filename = os.path.basename(thumb_path)
        dest_path = os.path.join(FINAL_OUTPUT_DIR, filename)
        shutil.copy2(thumb_path, dest_path)
        print(f"Copied thumbnail: {dest_path}")
    
    print(f"\nAll files ready in: {FINAL_OUTPUT_DIR}")
    print(f"Videos: {len(video_files)}")
    print(f"Thumbnails: {len(thumbnail_files)}")

if __name__ == "__main__":
    prepare_upload()
