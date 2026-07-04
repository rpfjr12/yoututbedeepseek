"""
Animates stick figure stories using Manim.
Reads scripts from scripts/scripts_output/ and renders MP4 files.
"""

import os
import sys
import glob
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from manim import *
from config import ANIMATION_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, FPS

# Configure Manim for vertical Shorts format
config.pixel_width = VIDEO_WIDTH
config.pixel_height = VIDEO_HEIGHT
config.frame_rate = FPS
config.background_color = WHITE

class StickFigureStory(Scene):
    """Base class for stick figure animations."""
    
    def __init__(self, script_lines, **kwargs):
        super().__init__(**kwargs)
        self.script_lines = script_lines
    
    def construct(self):
        # Create stick figure
        stick_figure = self.create_stick_figure()
        stick_figure.move_to(ORIGIN)
        
        # Animate each line
        for i, line in enumerate(self.script_lines):
            # Create text
            text = self.create_caption(line)
            text.next_to(stick_figure, DOWN, buff=1.0)
            
            # Animate stick figure (simple wave)
            self.play(
                Create(stick_figure) if i == 0 else AnimationGroup(),
                Write(text),
                run_time=0.5
            )
            
            # Hold for reading time
            self.wait(2.5 - 0.5)  # 2.5 seconds per line minus animation time
            
            # Fade out text if not last line
            if i < len(self.script_lines) - 1:
                self.play(FadeOut(text), run_time=0.3)
        
        # Final hold
        self.wait(1)
    
    def create_stick_figure(self):
        """Create a simple stick figure."""
        # Head
        head = Circle(radius=0.3, color=BLACK, fill_opacity=0)
        
        # Body
        body = Line(ORIGIN, DOWN * 1.0, color=BLACK)
        
        # Arms
        left_arm = Line(ORIGIN, LEFT * 0.6 + UP * 0.2, color=BLACK)
        right_arm = Line(ORIGIN, RIGHT * 0.6 + UP * 0.2, color=BLACK)
        
        # Legs
        left_leg = Line(DOWN * 1.0, DOWN * 1.0 + LEFT * 0.4, color=BLACK)
        right_leg = Line(DOWN * 1.0, DOWN * 1.0 + RIGHT * 0.4, color=BLACK)
        
        # Combine
        stick_figure = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        
        # Add a simple face
        left_eye = Dot(point=LEFT * 0.1 + UP * 0.05, radius=0.03, color=BLACK)
        right_eye = Dot(point=RIGHT * 0.1 + UP * 0.05, radius=0.03, color=BLACK)
        mouth = Arc(arc_center=ORIGIN, radius=0.08, angle=PI/2, color=BLACK)
        mouth.shift(DOWN * 0.05)
        
        face = VGroup(left_eye, right_eye, mouth)
        face.move_to(head.get_center())
        
        stick_figure.add(face)
        return stick_figure
    
    def create_caption(self, text):
        """Create caption text with background."""
        caption = Text(text, font_size=40, color=BLACK, font="Arial")
        caption.set_stroke(BLACK, width=0)
        
        # Add background rectangle
        bg = Rectangle(
            width=caption.width + 0.5,
            height=caption.height + 0.3,
            color=WHITE,
            fill_opacity=0.8,
            stroke_color=BLACK,
            stroke_width=2
        )
        bg.move_to(caption.get_center())
        
        return VGroup(bg, caption)

def find_manim_output():
    """Find the Manim-rendered MP4 file."""
    # Search for StickFigureStory.mp4 in media/ directory
    for root, dirs, files in os.walk("media"):
        for f in files:
            if f == "StickFigureStory.mp4":
                return os.path.join(root, f)
    return None

def render_all_scripts():
    """Render all scripts as stick figure animations."""
    os.makedirs(ANIMATION_DIR, exist_ok=True)
    
    # Get all script files
    script_files = sorted(glob.glob("scripts/scripts_output/*.txt"))
    
    if not script_files:
        print("No scripts found. Run generate_scripts.py first.")
        return
    
    for script_file in script_files:
        # Read script
        with open(script_file, "r") as f:
            lines = f.readlines()
        
        # Extract title and lines
        title = lines[0].replace("Title: ", "").strip()
        script_lines = [line.strip() for line in lines[3:] if line.strip()]
        
        print(f"Rendering: {title} ({len(script_lines)} lines)")
        
        # Create output filename
        base_name = os.path.basename(script_file).replace(".txt", "")
        output_file = os.path.join(ANIMATION_DIR, f"{base_name}.mp4")
        
        # Skip if already exists
        if os.path.exists(output_file):
            print(f"Already exists: {output_file}")
            continue
        
        # Clean up old media folder to avoid confusion
        if os.path.exists("media"):
            shutil.rmtree("media")
        
        # Render using Manim
        scene = StickFigureStory(script_lines)
        scene.render()
        
        # Find the actual output file
        default_output = find_manim_output()
        
        if default_output and os.path.exists(default_output):
            shutil.move(default_output, output_file)
            print(f"Saved: {output_file}")
        else:
            print(f"ERROR: Could not find rendered video.")
            print("Searched in media/ for StickFigureStory.mp4")
    
    # Clean up media folder
    if os.path.exists("media"):
        shutil.rmtree("media")
    
    print("\nAll animations rendered!")

if __name__ == "__main__":
    render_all_scripts()
