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

        for i, line in enumerate(lines, 1):
            matches = tag_pattern.findall(line)
            for tag_type, tag_id in matches:
                if tag_type in ['REF', 'SLIDE']:
                    if tag_id not in valid_slides:
                        # Fallback check: sometimes IDs might be referenced loosely?
                        # But strictly they should match.
                        errors.append(f"{filename}:{i} - Invalid Slide Reference: '{tag_id}' (Tag: [{tag_type}: {tag_id}])")
                elif tag_type == 'ACTION':
                    if tag_id not in valid_actions:
                        errors.append(f"{filename}:{i} - Invalid Action Reference: '{tag_id}' (Tag: [{tag_type}: {tag_id}])")

    if errors:
        print(f"Found {len(errors)} broken links:")
        for e in errors:
            print(f"  [X] {e}")
        exit(1) # Return error code 1 for CI/CD
    else:
        print("✅ Link Validation Passed: All references point to valid definitions.")

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

    # 4. Physical Asset Validation (New Feature)
    print("\n🔍 Validating Physical Assets...")
    missing_assets = []

    # Scan Design Spec for "assets/..." references
    with open(Design_Spec_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Look for: `_Library/...` references or `../02_Visuals/...`
            # Regex captures: _Library/S02_Purify/asset_name.wav
            match = re.search(r'(_Library/[a-zA-Z0-9_/-]+\.\w+)', line)
            if match:
                relative_path = match.group(1)
                full_path = os.path.join(base_dir, "01_MVP_Demo", relative_path)
                if not os.path.exists(full_path):
                    missing_assets.append(f"Design_Spec.md:{line_num} - Missing Asset: {relative_path}")

    if missing_assets:
        print(f"❌ Found {len(missing_assets)} missing physical assets:")
        for m in missing_assets:
            print(f"  [X] {m}")
        exit(1)
    else:
        print("✅ Asset Validation Passed: All referenced audio files exist.")
