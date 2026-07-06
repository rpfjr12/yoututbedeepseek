"""
Prepares final upload files by copying captioned videos and thumbnails
into the output/ folder for GitHub Actions artifact upload.
"""

import os
import sys
import glob
import shutil

# Import config paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAPTIONS_DIR, THUMBNAIL_DIR, FINAL_OUTPUT_DIR


def prepare_upload_files():
    """Copy captioned videos + thumbnails into FINAL_OUTPUT_DIR."""
    os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)

    # Find all captioned videos
    video_files = sorted(glob.glob(os.path.join(CAPTIONS_DIR, "*.mp4")))

    if not video_files:
        print(f"ERROR: No captioned videos found in {CAPTIONS_DIR}")
        print("Run captions step first.")
        return

    copied = 0

    for video in video_files:
        base = os.path.basename(video)
        dest_video = os.path.join(FINAL_OUTPUT_DIR, base)

        # Copy video
        shutil.copy2(video, dest_video)
        print(f"Copied video → {base}")
        copied += 1

        # Copy thumbnail if exists
        thumb_name = base.replace(".mp4", ".png")
        src_thumb = os.path.join(THUMBNAIL_DIR, thumb_name)
        dest_thumb = os.path.join(FINAL_OUTPUT_DIR, thumb_name)

        if os.path.exists(src_thumb):
            shutil.copy2(src_thumb, dest_thumb)
            print(f"Copied thumbnail → {thumb_name}")
        else:
            print(f"Missing thumbnail for {base}")

    # Final summary
    final_files = sorted(os.listdir(FINAL_OUTPUT_DIR))
    print("\n" + "=" * 60)
    print(f"UPLOAD READY → {FINAL_OUTPUT_DIR}")
    print(f"Total files: {len(final_files)}")
    for f in final_files:
        size_mb = os.path.getsize(os.path.join(FINAL_OUTPUT_DIR, f)) / (1024 * 1024)
        print(f"  - {f} ({size_mb:.1f} MB)")
    print("=" * 60)


if __name__ == "__main__":
    prepare_upload_files()
