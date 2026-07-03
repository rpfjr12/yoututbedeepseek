"""
Creates thumbnails for each script using Pillow.
No external API needed.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THUMBNAIL_DIR, THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, SCRIPT_DIR
from PIL import Image, ImageDraw, ImageFont
import glob

# Color schemes for thumbnails
COLOR_SCHEMES = [
    {"bg": (0, 0, 0), "text": (255, 255, 255), "accent": (255, 200, 0)},      # Black + yellow
    {"bg": (20, 20, 40), "text": (255, 255, 255), "accent": (0, 200, 255)},    # Dark blue + cyan
    {"bg": (40, 10, 10), "text": (255, 255, 255), "accent": (255, 50, 50)},    # Dark red + red
    {"bg": (10, 40, 10), "text": (255, 255, 255), "accent": (50, 255, 50)},    # Dark green + green
    {"bg": (30, 30, 30), "text": (255, 255, 255), "accent": (200, 100, 255)},  # Gray + purple
]

def get_title_from_script(script_path):
    """Extract the title from a script file."""
    with open(script_path, "r") as f:
        first_line = f.readline().strip()
    if first_line.startswith("Title:"):
        return first_line.replace("Title:", "").strip()
    return os.path.basename(script_path).replace(".txt", "").replace("_", " ").title()

def get_first_line_from_script(script_path):
    """Get the first content line (hook) from a script."""
    with open(script_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("Title:") and not line.startswith("Duration:") and not line.startswith("-"):
            return line
    return "Watch This"

def create_thumbnail(script_path, output_path, scheme_index=0):
    """Create a thumbnail image for a script."""
    title = get_title_from_script(script_path)
    hook = get_first_line_from_script(script_path)
    
    scheme = COLOR_SCHEMES[scheme_index % len(COLOR_SCHEMES)]
    
    # Create image
    img = Image.new("RGB", (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), scheme["bg"])
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 80)  # Bold
        hook_font = ImageFont.truetype("arial.ttf", 50)
        small_font = ImageFont.truetype("arial.ttf", 30)
    except:
        title_font = ImageFont.load_default()
        hook_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw accent bar at top
    draw.rectangle([(0, 0), (THUMBNAIL_WIDTH, 20)], fill=scheme["accent"])
    
    # Draw accent bar at bottom
    draw.rectangle([(0, THUMBNAIL_HEIGHT - 20), (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT)], fill=scheme["accent"])
    
    # Draw title (centered, upper portion)
    title_text = title.upper()
    try:
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = bbox[2] - bbox[0]
    except:
        title_width = len(title_text) * 40
    
    title_x = (THUMBNAIL_WIDTH - title_width) // 2
    title_y = 200
    
    # Draw shadow for title
    draw.text((title_x + 3, title_y + 3), title_text, fill=(0, 0, 0), font=title_font)
    draw.text((title_x, title_y), title_text, fill=scheme["accent"], font=title_font)
    
    # Draw hook text (smaller, below title)
    hook_text = f'"{hook}"'
    try:
        bbox = draw.textbbox((0, 0), hook_text, font=hook_font)
        hook_width = bbox[2] - bbox[0]
    except:
        hook_width = len(hook_text) * 25
    
    hook_x = (THUMBNAIL_WIDTH - hook_width) // 2
    hook_y = 450
    
    draw.text((hook_x + 2, hook_y + 2), hook_text, fill=(0, 0, 0), font=hook_font)
    draw.text((hook_x, hook_y), hook_text, fill=scheme["text"], font=hook_font)
    
    # Draw "SHORTS" badge at bottom
    badge_text = "YOUTUBE SHORTS"
    try:
        bbox = draw.textbbox((0, 0), badge_text, font=small_font)
        badge_width = bbox[2] - bbox[0]
    except:
        badge_width = len(badge_text) * 15
    
    badge_x = (THUMBNAIL_WIDTH - badge_width) // 2
    badge_y = THUMBNAIL_HEIGHT - 150
    
    # Badge background
    badge_padding = 20
    draw.rectangle(
        [(badge_x - badge_padding, badge_y - 10), 
         (badge_x + badge_width + badge_padding, badge_y + 50)],
        fill=scheme["accent"]
    )
    draw.text((badge_x, badge_y), badge_text, fill=(0, 0, 0), font=small_font)
    
    # Draw simple stick figure icon (bottom left)
    center_x = 200
    center_y = THUMBNAIL_HEIGHT - 300
    
    # Head
    draw.ellipse([(center_x - 40, center_y - 40), (center_x + 40, center_y + 40)], 
                 outline=scheme["accent"], width=5)
    # Body
    draw.line([(center_x, center_y + 40), (center_x, center_y + 150)], 
              fill=scheme["accent"], width=5)
    # Arms
    draw.line([(center_x, center_y + 70), (center_x - 80, center_y + 120)], 
              fill=scheme["accent"], width=5)
    draw.line([(center_x, center_y + 70), (center_x + 80, center_y + 120)], 
              fill=scheme["accent"], width=5)
    # Legs
    draw.line([(center_x, center_y + 150), (center_x - 60, center_y + 250)], 
              fill=scheme["accent"], width=5)
    draw.line([(center_x, center_y + 150), (center_x + 60, center_y + 250)], 
              fill=scheme["accent"], width=5)
    
    # Save
    img.save(output_path, "PNG")
    print(f"Thumbnail saved: {output_path}")

def main():
    """Generate thumbnails for all scripts."""
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)
    
    # Find all script files
    script_files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "*.txt")))
    
    if not script_files:
        print("No script files found. Run scripts/generate_scripts.py first.")
        return
    
    for i, script_path in enumerate(script_files):
        title = get_title_from_script(script_path)
        output_filename = f"thumbnail_{i+1:02d}_{title.lower().replace(' ', '_')}.png"
        output_path = os.path.join(THUMBNAIL_DIR, output_filename)
        
        create_thumbnail(script_path, output_path, scheme_index=i)
    
    print(f"\nTotal thumbnails created: {len(script_files)}")

if __name__ == "__main__":
    main()
