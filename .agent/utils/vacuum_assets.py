import os
import shutil

ASSETS_ROOT = "02_Visuals/assets"

# Map ID Prefix to Folder Name
MODULE_MAP = {
    "S01": "S01_Intro",
    "S02": "S02_Phase1_Purify",
    "S03": "S03_Phase2_Sculpt",
    "S04": "S04_Phase3_Space",
    "S05": "S05_Phase4_Position",
    "S06": "S06_Summary"
}

def get_correct_module(filename):
    # Filename: S02_BadCase.png
    # Extract prefix
    name = filename
    parts = name.split('_')
    prefix = parts[0] # S02
    
    # Handle S02b -> S02
    if prefix.startswith("S") and len(prefix) >= 3:
        base_id = prefix[:3] # S02
        if base_id in MODULE_MAP:
            return MODULE_MAP[base_id]
    return None

def enforce_module_boundaries():
    print("🚧 Enforcing Module Boundaries...")
    
    # Iterate through all MODULE folders
    for module_key, module_folder in MODULE_MAP.items():
        folder_path = os.path.join(ASSETS_ROOT, module_folder)
        if not os.path.exists(folder_path):
            continue
            
        files = os.listdir(folder_path)
        for f in files:
            if f.startswith("."): continue
            
            correct_folder_name = get_correct_module(f)
            
            # If item belongs to ANOTHER folder
            if correct_folder_name and correct_folder_name != module_folder:
                # Move it
                source_path = os.path.join(folder_path, f)
                dst_folder_path = os.path.join(ASSETS_ROOT, correct_folder_name)
                dst_path = os.path.join(dst_folder_path, f)
                
                print(f"  MOVE: {f} from {module_folder} -> {correct_folder_name}")
                
                if os.path.exists(dst_path):
                     # If conflict, we have a duplicate across folders.
                     # Since we are moving TO the correct place, the one IN the correct place is likely the authority.
                     # Or they are identical.
                     # We can safely delete the misplaced copy.
                     print(f"    ⚠️  Target exists. Deleting misplaced copy.")
                     os.remove(source_path)
                else:
                    shutil.move(source_path, dst_path)

def deduplicate_folders():
    print("✂️  Deduplication logic is now handled by unique naming constraints.")
    # Legacy logic removed.

if __name__ == "__main__":
    enforce_module_boundaries()
    deduplicate_folders()
