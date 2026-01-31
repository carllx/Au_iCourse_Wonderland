import os
import re
import shutil

def parse_structure_map(base_dir):
    """
    Parses 00_Structure_Map.md to map Slide IDs to Module Folders.
    Returns: dict { 'S01_Title': 'S01_Intro', ... }
    """
    map_path = os.path.join(base_dir, "03_Scripts", "00_Structure_Map.md")
    if not os.path.exists(map_path):
        print(f"Error: Structure Map not found at {map_path}")
        return {}

    slide_to_module = {}
    current_module = "_Global" # Default
    
    # Regex for Module Header: ## 模块一：导入 (S01_Intro)
    module_pattern = re.compile(r'^##\s+.*?\((S\d+_[a-zA-Z0-9_]+)\)')
    # Regex for Slide Ref: `[SLIDE: S01_Title]`
    slide_pattern = re.compile(r'\[SLIDE:\s*(S[a-zA-Z0-9_]+)\]')

    with open(map_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Check for Module Change
            mod_match = module_pattern.search(line)
            if mod_match:
                current_module = mod_match.group(1)
                continue
            
            # Check for Slide References
            slides = slide_pattern.findall(line)
            for slide_id in slides:
                # First come first serve ownership
                if slide_id not in slide_to_module:
                    slide_to_module[slide_id] = current_module
    
    return slide_to_module

def migrate_assets(base_dir):
    assets_dir = os.path.join(base_dir, "02_Visuals", "assets")
    proxies_dir = os.path.join(assets_dir, "proxies")
    
    # 1. Get Mapping
    print("Parsing Structure Map...")
    slide_owner_map = parse_structure_map(base_dir)
    print(f"Mapped {len(slide_owner_map)} slides to modules.")

    # 2. Create Folders & Move
    moved_count = 0
    
    # helper to move file
    def smart_move(source_path, filename, slide_id):
        nonlocal moved_count
        
        # Determine Destination Module
        module_name = slide_owner_map.get(slide_id, "_SubFiles") # Default if not in map
        dest_dir = os.path.join(assets_dir, module_name)
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        dest_path = os.path.join(dest_dir, filename)
        
        # Move (Overwrite if exists in dest, to ensure latest proxy)
        shutil.move(source_path, dest_path)
        print(f"Moved: {filename} -> {module_name}/")
        moved_count += 1

    # A. Migrate from proxies/
    if os.path.exists(proxies_dir):
        print("\nMigrating from proxies/...")
        for filename in os.listdir(proxies_dir):
            if not filename.endswith('.png'): continue
            
            # Extract ID from filename (S01_Title.png -> S01_Title)
            slide_id = os.path.splitext(filename)[0]
            source_path = os.path.join(proxies_dir, filename)
            
            smart_move(source_path, filename, slide_id)
        
        # Cleanup empty proxies dir
        try:
            os.rmdir(proxies_dir)
            print("Removed empty proxies/ directory.")
        except:
            print("Warning: proxies/ not empty, kept.")

    # B. Consolidate specific subfolders if needed
    # (Optional: Scan other folders to ensure they are correct)
    
    print(f"\nMigration Complete. Moved {moved_count} assets.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    migrate_assets(base_dir)
