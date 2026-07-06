"""
Runs the entire pipeline: scripts -> animations -> captions -> thumbnails -> upload prep.
Fails fast on errors and reports exactly what went wrong.
"""

import os
import sys
import subprocess
import shutil


def run_script(script_path, description):
    """Run a Python script and return success/failure with output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Script: {script_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(script_path):
        print(f"ERROR: Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True,
            text=True,
            check=False  # We handle returncode manually
        )
        
        # Print stdout/stderr so it shows in GitHub Actions logs
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        if result.returncode != 0:
            print(f"ERROR: {description} exited with code {result.returncode}")
            return False
            
        print(f"SUCCESS: {description}")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to run {script_path}: {e}")
        return False


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def list_outputs(base_dir):
    """List what was produced in each output folder."""
    print(f"\n{'='*60}")
    print("OUTPUT SUMMARY")
    print(f"{'='*60}")
    
    folders = [
        ("Scripts", "scripts/scripts_output"),
        ("Animations", "animation/animations_output"),
        ("Captions", "captions/captions_output"),
        ("Thumbnails", "thumbnails/thumbnails_output"),
        ("Final Output", "output"),
    ]
    
    for label, rel_path in folders:
        full_path = os.path.join(base_dir, rel_path)
        if os.path.exists(full_path):
            files = os.listdir(full_path)
            print(f"{label}: {len(files)} files in {rel_path}")
            for f in files[:5]:  # Show first 5
                print(f"  - {f}")
            if len(files) > 5:
                print(f"  ... and {len(files)-5} more")
        else:
            print(f"{label}: MISSING {rel_path}")


def main():
    """Run the full pipeline. Exit non-zero on any failure."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure output directory exists before pipeline runs
    ensure_output_dir()
    
    steps = [
        (os.path.join(base_dir, "scripts", "generate_scripts.py"), "Generating scripts"),
        (os.path.join(base_dir, "animation", "stick_figure_story.py"), "Animating stick figures"),
        (os.path.join(base_dir, "captions", "add_captions.py"), "Adding captions"),
        (os.path.join(base_dir, "thumbnails", "create_thumbnail.py"), "Creating thumbnails"),
        (os.path.join(base_dir, "upload", "prepare_upload.py"), "Preparing final upload files"),
    ]
    
    failed_steps = []
    
    for script_path, description in steps:
        success = run_script(script_path, description)
        if not success:
            failed_steps.append(description)
            print(f"STEP FAILED: {description}")
            # Uncomment the next line to fail fast (stop on first error)
            # sys.exit(1)
    
    # Summary
    list_outputs(base_dir)
    
    print(f"\n{'='*60}")
    if failed_steps:
        print(f"PIPELINE FAILED: {len(failed_steps)} step(s) failed")
        for step in failed_steps:
            print(f"  - {step}")
        print(f"{'='*60}")
        sys.exit(1)
    else:
        print("PIPELINE COMPLETE - All steps succeeded")
        print(f"{'='*60}")
        sys.exit(0)


if __name__ == "__main__":
    main()
