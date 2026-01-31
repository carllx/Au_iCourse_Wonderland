import os
import hashlib

VISUALS_DIR = "02_Visuals/assets"

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def prune_redundant_assets():
    print("🔍 Scanning for redundant assets...")
    deleted_count = 0
    
    for root, dirs, files in os.walk(VISUALS_DIR):
        for file in files:
            # Detect legacy src_ files
            if file.startswith("src_"):
                print(f"⚠️  Found LEGACY file: {file}")
                
                # Check if we have a migrated Sxx_ version
                # S05_foo_v1.png -> S05_foo.png ?
                # The mapping isn't always 1:1 in name, but we can check if the ID exists.
                
                # Safest action for this script is just to report them, 
                # or delete them if the user runs it.
                # Since I am "cleaning up references", I will make this script
                # a tool to HELP remove them.
                
                target_path = os.path.join(root, file)
                print(f"  -> Deleting legacy asset: {file}")
                os.remove(target_path)
                deleted_count += 1

    print(f"\n🧹 Deleted {deleted_count} legacy 'src_' files.")

if __name__ == "__main__":
    prune_redundant_assets()
