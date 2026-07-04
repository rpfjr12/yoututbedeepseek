"""
Runs the entire pipeline: scripts -> animations -> captions -> thumbnails -> upload prep.
"""

import os
import sys
import subprocess

def run_script(script_path, description):
    """Run a Python script and print status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run {script_path}: {e}")
        return False

def main():
    """Run the full pipeline."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    steps = [
        (os.path.join(base_dir, "scripts", "generate_scripts.py"), "Generating scripts"),
        (os.path.join(base_dir, "animation", "stick_figure_story.py"), "Animating stick figures"),
        (os.path.join(base_dir, "captions", "add_captions.py"), "Adding captions"),
        (os.path.join(base_dir, "thumbnails", "create_thumbnail.py"), "Creating thumbnails"),
        (os.path.join(base_dir, "upload", "prepare_upload.py"), "Preparing final upload files"),
    ]
    
    for script_path, description in steps:
        success = run_script(script_path, description)
        if not success:
            print(f"Step failed: {description}")
            print("Continuing anyway...")
    
    print(f"\n{'='*60}")
    print("Pipeline complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
