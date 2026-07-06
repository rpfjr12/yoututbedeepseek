import os

# Base directory of the repo (absolute path)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Scripts
SCRIPT_DIR = os.path.join(BASE_DIR, "scripts", "scripts_output")

# Animation
ANIMATION_DIR = os.path.join(BASE_DIR, "animation", "animations_output")

# Captions
CAPTIONS_DIR = os.path.join(BASE_DIR, "captions", "captions_output")

# Thumbnails
THUMBNAIL_DIR = os.path.join(BASE_DIR, "thumbnails", "thumbnails_output")

# Thumbnail sizes (required by create_thumbnail.py)
THUMBNAIL_WIDTH = 720
THUMBNAIL_HEIGHT = 1280

# Final output folder
FINAL_OUTPUT_DIR = os.path.join(BASE_DIR, "output")
