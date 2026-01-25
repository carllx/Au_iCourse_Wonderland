import os
import re

def parse_structure_map(file_path):
    """
    Parses 00_Structure_Map.md to extract module timelines.
    Returns dict: {'S02': '05:00 - 11:00', ...}
    """
    if not os.path.exists(file_path):
        print(f"Error: Structure Map not found at {file_path}")
        return {}
    
    timelines = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        # Regex to find: ## 模块二：净化 (S02_Phase1_Purify)
        # Followed by: * **Time**: 05:00 - 11:00
        content = f.read()
        
        # Split by modules roughly
        modules = re.split(r'##\s+', content)
        for mod in modules:
            # Check ID
            id_match = re.search(r'\((S\d+)_', mod)
            if not id_match:
                continue
            
            mod_id = id_match.group(1)
            
            # Check Time
            time_match = re.search(r'\*\s+\*\*Time\*\*:\s+(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})', mod)
            if time_match:
                timelines[mod_id] = time_match.group(1)
                
    return timelines

def check_scripts(scripts_dir, expected_timelines):
    """
    Scans Sxx scripts and checks if Context line matches structure.
    """
    errors = []
    
    for filename in os.listdir(scripts_dir):
        # Match S02_....md
        match = re.match(r'(S\d+)_.*\.md', filename)
        if not match:
            continue
            
        mod_id = match.group(1)
        if mod_id not in expected_timelines:
            # print(f"Info: Skipping {filename} (Not in Structure Map strict time list)")
            continue
            
        full_path = os.path.join(scripts_dir, filename)
        expected_time = expected_timelines[mod_id]
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for: > **Context**: 05:00 - 11:00
            context_match = re.search(r'>\s+\*\*Context\*\*:\s+(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})', content)
            
            if not context_match:
                errors.append(f"{filename}: Missing '> **Context**:' metadata.")
            elif context_match.group(1) != expected_time:
                errors.append(f"{filename}: Timeline Mismatch. Got '{context_match.group(1)}', expected '{expected_time}' (from Structure Map).")

    return errors

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    structure_path = os.path.join(base_dir, "01_Scripts", "00_Structure_Map.md")
    scripts_dir = os.path.join(base_dir, "01_Scripts")
    
    print("🔍 Integrity Check: Structure vs Scripts Timeline...")
    
    timelines = parse_structure_map(structure_path)
    print(f"Loaded {len(timelines)} timeline definitions from Structure Map.")
    
    errors = check_scripts(scripts_dir, timelines)
    
    if errors:
        print(f"❌ Found {len(errors)} consistency errors:")
        for e in errors:
            print(f"  [X] {e}")
        exit(1)
    else:
        print("✅ Consistency Check Passed: Script timelines match Structure Map.")
