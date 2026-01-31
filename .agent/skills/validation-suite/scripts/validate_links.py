import os
import re

def parse_definitions(file_path, id_pattern):
    """Parses a markdown file to extract IDs based on a header pattern."""
    ids = set()
    if not os.path.exists(file_path):
        print(f"Warning: Definition file not found: {file_path}")
        return ids

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Use findall to capture multiple definitions on one line
            matches = id_pattern.findall(line)
            for m in matches:
                ids.add(m)
    return ids

def get_slide_types(db_path):
    """
    Parses Slide_Database.md to extract {slide_id: slide_type}.
    """
    types = {}
    if not os.path.exists(db_path):
        return types
        
    current_id = None
    with open(db_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match Header: ## Sxx_ID
            id_match = re.match(r'^##\s+(S[a-zA-Z0-9]+_[a-zA-Z0-9_]+)', line)
            if id_match:
                current_id = id_match.group(1)
                continue
            
            # Match Type: * **Type**: [Concept Art]
            if current_id:
                type_match = re.search(r'\*\s+\*\*Type\*\*:\s+\[(.*?)\]', line)
                if type_match:
                    types[current_id] = type_match.group(1)
                    current_id = None # Check complete for this ID
    return types

def validate_scripts(scripts_dir, valid_slides, valid_actions):
    """Scans scripts for tags and validates them against known IDs."""

    # Patterns to match tags in scripts
    # Matches [REF: Sxx_...], [SLIDE: Sxx_...], [ACTION: ACT_xx_...]
    # We allow "Slide_ID" or just "ID" inside the tag, assuming the ID itself contains the prefix
    tag_pattern = re.compile(r'\[(REF|SLIDE|ACTION):\s*([a-zA-Z0-9_]+)\]')

    errors = []

    if not os.path.exists(scripts_dir):
        print(f"Error: Scripts directory not found: {scripts_dir}")
        return

    for filename in os.listdir(scripts_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(scripts_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    # Broader pattern to capture ANY reference to a Slide ID (e.g. S01_Title, S11b_Tail_Timer)
    # We look for word boundaries to avoid partial matches
    slide_ref_pattern = re.compile(r'\b(S\d+[a-z]?_[a-zA-Z0-9_]+)\b')

    errors = []
    warnings = []

    if not os.path.exists(scripts_dir):
        print(f"Error: Scripts directory not found: {scripts_dir}")
        return

    for filename in os.listdir(scripts_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(scripts_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            # 1. Scan for Slide IDs
            potential_refs = slide_ref_pattern.findall(line)
            for ref_id in potential_refs:
                # If it looks like a Slide ID, check if it's in the DB
                if ref_id not in valid_slides:
                    # It might be a file name (e.g. S02_Purify.png), ignore if extension exists
                    # But the regex \b..._...\b might catch "S02_Purify" inside "S02_Purify.png"
                    # Simple check: does the line contain ref_id + "."?
                    if f"{ref_id}." in line:
                         continue # Likely a filename
                    
                    # Ignore own filename reference (e.g. inside S01_Intro.md, "S01_Intro")
                    if ref_id in filename:
                        continue

                    warnings.append(f"{filename}:{i} - ⚠️  Orphan Reference: '{ref_id}' found in text but NOT defined in Slide_Database.")

            # 2. Keep the strict tag check for Actions as it's more specific
            action_matches = re.findall(r'\[ACTION:\s*([a-zA-Z0-9_]+)\]', line)
            for action_id in action_matches:
                 if action_id not in valid_actions:
                        errors.append(f"{filename}:{i} - ❌ Invalid Action Tag: '{action_id}'")

    print(f"\nScanning {len(os.listdir(scripts_dir))} scripts for references...")

    if warnings:
        print(f"\n⚠️  Found {len(warnings)} potential loose/orphan references:")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print(f"\n❌ Found {len(errors)} critical broken links:")
        for e in errors:
            print(f"  {e}")
        exit(1)
    else:
        print("\n✅ Link Validation Passed (Critical). Check warnings above for loose threads.")

if __name__ == "__main__":
    # 1. Setup Paths (Relative to where script is run, usually project root)
    # The script is in .agent/skills/validate_links.py
    # So __file__ is /path/to/.agent/skills/validate_links.py
    # dirname -> skills
    # dirname -> .agent
    # dirname -> root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

    slide_db_path = os.path.join(base_dir, "02_Visuals", "Slide_Database.md")
    Design_Spec_path = os.path.join(base_dir, "01_MVP_Demo", "00_Design_Spec_Alice.md")
    scripts_dir = os.path.join(base_dir, "03_Scripts")

    print(f"Validating project at: {base_dir}")

    # 2. Parse Definitions
    # Slides: ## S01_Title (Supports S02b)
    slide_id_pattern = re.compile(r'^##\s+(S[a-zA-Z0-9]+_[a-zA-Z0-9_]+)')
    valid_slides = parse_definitions(slide_db_path, slide_id_pattern)
    print(f"Loaded {len(valid_slides)} Visual Slides.")

    # Actions: Defined in Design Spec via > *ACT_ID: [ACT_01], [ACT_02]*
    # Regex looks for [ACT_...]
    action_id_pattern = re.compile(r'\[(ACT_[a-zA-Z0-9_]+)\]')
    valid_actions = parse_definitions(Design_Spec_path, action_id_pattern)
    print(f"Loaded {len(valid_actions)} MVP Actions.")

    # 3. Validate
    # We now also check if the DEFINITIONS themselves point to real files
    # But for now, let's at least check valid_scripts -> valid_slides/actions logic
    # AND verify that the defined Actions point to real assets if mentioned.

    validate_scripts(scripts_dir, valid_slides, valid_actions)

    # 4. Physical Asset Validation (New Feature v2.0)
    print("\n🔍 Validating Physical Assets (ID-Centric)...")
    
    # 4.1 Audio Assets (from Design Spec)
    missing_assets = []
    with open(Design_Spec_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            match = re.search(r'(_Library/[a-zA-Z0-9_/-]+\.\w+)', line)
            if match:
                relative_path = match.group(1)
                full_path = os.path.join(base_dir, "01_MVP_Demo", relative_path)
                if not os.path.exists(full_path):
                    missing_assets.append(f"Design_Spec.md:{line_num} - Missing Audio: {relative_path}")

    # 4.2 Visual Assets (from Slide Database)
    # Logic: For every Slide ID, is there a file starting with "ID"  in 02_Visuals/assets?
    visuals_root = os.path.join(base_dir, "02_Visuals", "assets")
    if not os.path.exists(visuals_root):
        print(f"Error: Visuals directory not found: {visuals_root}")
        exit(1)

    # Load Slide Types for exemption logic
    slide_types = get_slide_types(slide_db_path)

    # 1. Collect all filenames in 02_Visuals/assets recursively
    all_files = []
    for root, dirs, files in os.walk(visuals_root):
        for file in files:
            if file.startswith('.'): continue
            all_files.append(file)
            
    # 2. Check each slide
    visual_errors = []
    
    # Track verified assets for reporting
    verified_count = 0
    exempt_count = 0
    
    for slide_id in valid_slides:
        # Check exemption
        slide_type = slide_types.get(slide_id, "Unknown")
        if slide_type == "Live Demo":
            # Live Demo is rendered dynamically by code (H5), so physical asset is optional.
            # We skip specific file check for it.
            exempt_count += 1
            continue
            
        # Rule: A match exists if ANY file starts with "{slide_id}"
        # AND followed by a separator or dot (to avoid S01 matching S010)
        
        found = False
        pattern_prefix = slide_id
        
        for fname in all_files:
            # Check plain prefix (Sxx_Name...)
            # Case insensitive check for Zero-Copy support
            lower_fname = fname.lower()
            lower_prefix = pattern_prefix.lower()
            
            if lower_fname.startswith(lower_prefix + ".") or lower_fname.startswith(lower_prefix + "_"):
                found = True
                break
            

                
        if not found:
            visual_errors.append(f"Missing Visual Asset for ID: {slide_id} (Type: {slide_type})")
        else:
            verified_count += 1

    if missing_assets or visual_errors:
        print(f"\n❌ Validation Failed with {len(missing_assets) + len(visual_errors)} errors:")
        for m in missing_assets:
            print(f"  [Audio] {m}")
        for v in visual_errors:
            print(f"  [Visual] {v}")
        exit(1)
    else:
        print(f"✅ Asset Validation Passed: {verified_count} assets verified, {exempt_count} Live Demos exempt.")
