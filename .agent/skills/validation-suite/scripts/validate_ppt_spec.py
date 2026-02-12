#!/usr/bin/env python3
import re
import sys
import os

def parse_database(db_path):
    """
    Parses Slide_Database.md and returns a dict mapping SlideID -> {Type, Fields}
    """
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        sys.exit(1)

    with open(db_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find slide blocks: ## S0x_ID ... content ...
    # precise regex: ^## (S\w+)
    slide_pattern = re.compile(r'^##\s+(S[\w_]+)', re.MULTILINE)
    
    db = {}
    lines = content.split('\n')
    current_id = None
    
    for line in lines:
        match = re.match(r'^##\s+(S[\w_]+)', line)
        if match:
            current_id = match.group(1)
            db[current_id] = {'fields': set()}
            continue
        
        if current_id:
            # Capture field names like * **Type**: ...
            field_match = re.match(r'^\*\s+\*\*(\w+)\*\*:', line)
            if field_match:
                field = field_match.group(1)
                db[current_id]['fields'].add(field)
                # Capture value of Type specifically
                if field == 'Type':
                    type_val_match = re.search(r'\[(.*?)\]', line)
                    if type_val_match:
                        db[current_id]['type'] = type_val_match.group(1)

    return db

def parse_script(script_path):
    """
    Parses a markdown script and returns list of referenced SlideIDs
    and a map of ID -> has_text_override boolean
    """
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        sys.exit(1)
        
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    refs = []
    overrides = {}
    
    # Regex for [SLIDE: ID]
    # Also need to check if there is a > Text: override in the same block (heuristic)
    
    # Simple pass for Refs first
    ref_matches = re.finditer(r'\[SLIDE:\s*(S[\w_]+)\]', content)
    for m in ref_matches:
        slide_id = m.group(1)
        if slide_id not in refs:
            refs.append(slide_id)
            
        # Check for immediate Text override in subsequent lines (up to 5 lines)
        # This is a basic heuristic
        start_pos = m.end()
        search_window = content[start_pos:start_pos+500] 
        # Look for "> Text:" or "> Caption:" before next "> [VISUAL]" or Header
        if re.search(r'>\s*[\*\-]?\s+\**(Text|Caption)\**:', search_window):
             overrides[slide_id] = True
        else:
             overrides[slide_id] = False
             
    return refs, overrides

def validate(script_path):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    db_path = os.path.join(project_root, '02_Visuals', 'Slide_Database.md')
    
    print(f"🔍 Validating PPT Spec for: {os.path.basename(script_path)}")
    print(f"📂 Database: {os.path.basename(db_path)}")
    
    db = parse_database(db_path)
    refs, overrides = parse_script(script_path)
    
    errors = 0
    warnings = 0
    
    print("-" * 40)
    
    # Check 1: Existence
    for slide_id in refs:
        if slide_id not in db:
            print(f"❌ [MISSING] {slide_id} referenced in script but not found in Database.")
            errors += 1
            continue
            
        # Check 2: Content Requirements
        slide_data = db[slide_id]
        slide_type = slide_data.get('type', 'Unknown')
        slide_fields = slide_data['fields']
        has_override = overrides.get(slide_id, False)
        
        # Rule: Title Card must have Text
        if 'Title Card' in slide_type:
            if 'Text' not in slide_fields and not has_override:
                 print(f"❌ [CONTENT] {slide_id} (Title Card) missing '**Text**' field.")
                 errors += 1
                 
        # Rule: Concept Art must have Caption
        elif 'Concept Art' in slide_type:
             if 'Caption' not in slide_fields and not has_override:
                 print(f"⚠️ [CONTENT] {slide_id} (Concept Art) missing '**Caption**' field.")
                 warnings += 1

        # Rule: UI/Screenshot implies instruction
        elif 'UI' in slide_type or 'Screenshot' in slide_type:
             # Ideally needs Text or List or Caption
             has_content = any(f in slide_fields for f in ['Text', 'List', 'Caption'])
             if not has_content and not has_override:
                 print(f"⚠️ [CONTENT] {slide_id} (UI) has no text content. Ensure script has voiceover covering this.")
                 warnings += 1
                 
    # Check 3: Orphans (Only if checking all scripts, but here we check single script, so irrelevant? 
    # Actually user wants "Script is King", so orphans in DB are bad generally, but checking a single script 
    # doesn't reveal global orphans. We skip global orphan check here or we'd get false positives.)

    print("-" * 40)
    if errors == 0:
        print(f"✅ PPT Spec check passed (Warnings: {warnings})")
        sys.exit(0)
    else:
        print(f"FAILED: Found {errors} errors and {warnings} warnings.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_ppt_spec.py <script_md_path>")
        sys.exit(1)
        
    script_path = sys.argv[1]
    validate(script_path)
