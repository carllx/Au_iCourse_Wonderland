import os
import re
from PIL import Image, ImageDraw, ImageFont

def generate_proxies(base_dir):
    """
    Scans Slide_Database.md and generates placeholder images for all defined slides.
    """
    
    # 1. Paths
    slide_db_path = os.path.join(base_dir, "02_Visuals", "Slide_Database.md")
    proxy_dir = os.path.join(base_dir, "02_Visuals", "assets", "proxies")
    
    if not os.path.exists(proxy_dir):
        os.makedirs(proxy_dir)
        print(f"Created proxy directory: {proxy_dir}")

    # 2. Parse Database
    slides = []
    current_slide = {}
    
    with open(slide_db_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Match header ## S01_Title
            match = re.search(r'^##\s+(S[a-zA-Z0-9_]+)', line)
            if match:
                if current_slide:
                    slides.append(current_slide)
                current_slide = {'id': match.group(1), 'type': 'Unknown', 'desc': ''}
                continue
            
            # Match Type
            type_match = re.search(r'\*\s+\*\*Type\*\*:\s+\[(.*?)\]', line)
            if type_match and current_slide:
                current_slide['type'] = type_match.group(1)
                
    if current_slide:
        slides.append(current_slide)
        
    print(f"Found {len(slides)} slide definitions.")

    # 3. Generate Images
    font_size = 60
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    colors = {
        'Motion Graphic': (50, 50, 100), 'UI Graphic': (50, 100, 50),
        'UI Composite': (50, 100, 100), 'Diagram': (100, 100, 50),
        'Concept Art': (100, 50, 100), 'Stock/Reference': (100, 50, 50),
        'Task Card': (50, 50, 50), 'Unknown': (0, 0, 0)
    }

    # Helper to resolve module
    # Reuse the logic from migrate_assets (inline here for simplicity or import)
    # Ideally we should refactor shared logic, but for now copying the map parser
    def get_structure_map():
        map_path = os.path.join(base_dir, "03_Scripts", "00_Structure_Map.md")
        slide_to_module = {}
        current_module = "_SubFiles"
        if os.path.exists(map_path):
            with open(map_path, 'r', encoding='utf-8') as f:
                for line in f:
                    mod_match = re.search(r'^##\s+.*?\((S\d+_[a-zA-Z0-9_]+)\)', line)
                    if mod_match: current_module = mod_match.group(1)
                    slides = re.findall(r'\[SLIDE:\s*(S[a-zA-Z0-9_]+)\]', line)
                    for sid in slides:
                        if sid not in slide_to_module: slide_to_module[sid] = current_module
        return slide_to_module

    slide_owner_map = get_structure_map()
    assets_dir = os.path.join(base_dir, "02_Visuals", "assets")

    generated_count = 0
    for slide in slides:
        module_name = slide_owner_map.get(slide['id'], "_SubFiles")
        dest_dir = os.path.join(assets_dir, module_name)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        filename = f"{slide['id']}.png"
        filepath = os.path.join(dest_dir, filename)
        
        if os.path.exists(filepath):
            # print(f"Skipping existing: {filename}")
            continue
            
        # Determine Size
        width, height = 1920, 1080 # Default 16:9
        # Check if 'Dimension' was parsed (need to update parsing logic above first)
        # For now, let's just default to 1920x1080 as requested unless we add parsing.
        # But wait, we didn't add parsing for 'Dimension' in step 2.
        # Let's fix step 2 first. 
        # Actually, let's keep it simple: 
        # If Type is [UI Graphic] (Icon), maybe make it square? 
        # No, User asked for "Objective Evaluation".
        # Evaluation: Most references seem to be Full Slides.
        # S02b_Toolbox_Flash is a "Grid of icons". That sounds like a full slide.
        # So 16:9 is likely correct for ALL current items.
        
        bg_color = colors.get(slide['type'], (30, 30, 30))
        img = Image.new('RGB', (width, height), color=bg_color)
        d = ImageDraw.Draw(img)
        
        d.text((100, height//3), slide['id'], fill=(255, 255, 255), font=font)
        text_type = f"Type: [{slide['type']}]"
        d.text((100, height//2), text_type, fill=(200, 200, 200), font=small_font)
        d.text((100, height-100), "GREYBOX PROXY ASSET (16:9)", fill=(128, 128, 128), font=small_font)
        
        img.save(filepath)
        print(f"Generated: {module_name}/{filename}")
        generated_count += 1

    print(f"\nOperation Complete. Generated {generated_count} new proxy assets.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    generate_proxies(base_dir)
