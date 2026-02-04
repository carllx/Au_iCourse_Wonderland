#!/usr/bin/env python3
"""
Narrative Integrity Validator (INI Framework)
---------------------------------------------
A logic-based linter that enforces "Double-Entry Bookkeeping" between 
Visual Action Tags and Audio Description Text.

Rule: "If it moves the mouse (Visual), it must be spoken (Audio)."

Logic:
1. Parse script for `> [VISUAL]` blocks.
2. Detect "Action Verbs" in Visual blocks (e.g., Click, Drag, Set).
3. Assert that the *immediately following* Audio block contains a corresponding "Disclosure Verb" (e.g., "点击", "拖动").

Usage:
    python validate_narrative_integrity.py <script_file>
"""

import sys
import re
from pathlib import Path

# --- Configuration ---

# 1. Action Triggers (Visual Side) - English
# If these words appear in a > [VISUAL] block, it counts as an "Action".
VISUAL_ACTION_TRIGGERS = [
    r"Action\*?\*?:", # Matches Action:, **Action**:, *Action*:
    r"Click",
    r"Drag",
    r"Set",
    r"Adjust",
    r"Press",
    r"Select",
    r"Toggle",
    r"Move",
    r"Change"
]

# 2. Disclosure Verbs (Audio Side) - Chinese
# The audio text must contain at least one of these to "disclose" the action.
AUDIO_DISCLOSURE_VERBS = [
    "点击", "点选", "按下", "按",
    "拖动", "拖拽", "拉动",
    "设置", "调整", "改为", "设为",
    "选择", "选中",
    "移动", "滑",
    "打开", "关闭",
    "输入", "写",
    "听", "看", "观察", "注意" # Sensory verifications are also acceptable disclosures
]

def scan_script(file_path):
    print(f"🔍 [INI Check] Scanning: {file_path}")
    content = Path(file_path).read_text(encoding='utf-8')
    lines = content.splitlines()

    stats = {
        "visual_blocks": 0,
        "action_blocks": 0,
        "passed": 0,
        "failed": 0
    }

    errors = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 1. Detect Visual Block Start (Flexible)
        # Matches "> [VISUAL]" or "> **[VISUAL]**"
        if line.startswith(">") and "[VISUAL]" in line:
            stats["visual_blocks"] += 1
            visual_lines = []
            
            # 2. Consume full blockquote
            # Keep reading as long as lines start with ">"
            while i < len(lines):
                curr_line = lines[i].strip()
                if not curr_line.startswith(">"):
                    break
                visual_lines.append(curr_line)
                i += 1
            
            # We are now at the first line AFTER the blockquote
            visual_content = "\n".join(visual_lines)
            line_num = i - len(visual_lines) + 1
            
            # 3. Check if it contains an "Action"
            is_action = False
            for trigger in VISUAL_ACTION_TRIGGERS:
                if re.search(trigger, visual_content, re.IGNORECASE):
                    is_action = True
                    break
            
            if is_action:
                stats["action_blocks"] += 1
                
                # 4. Find the next Audio Block
                # Scan ahead until we hit text that is NOT a tag/header
                audio_text = ""
                # Note: 'i' is already at the next line
                lookahead = i
                found_audio = False
                
                while lookahead < len(lines):
                    next_line = lines[lookahead].strip()
                    lookahead += 1
                    
                    if not next_line:
                        continue
                        
                    # [Patch] Ignore meta-comments (e.g., "(Action)", "(切回界面)")
                    # These break the visual-audio link if counted as "audio text" but don't contain verbs.
                    if next_line.startswith("(") and next_line.endswith(")"):
                        continue
                        
                    # Stop if we hit structure markers
                    if next_line.startswith("#") or next_line.startswith("---"):
                        break
                        
                    # Stop if we hit another blockquote (Metadata)
                    if next_line.startswith(">"):
                        break
                        
                    # Stop if we hit [AUDIO] tag (this is good, the text follows)
                    if "[AUDIO]" in next_line:
                        continue
                        
                    # Found candidate text
                    audio_text = next_line
                    found_audio = True
                    break
                
                # 5. Verify Audio
                if not found_audio:
                    # Error: Silence (Metadata Black Hole)
                    errors.append(f"🔴 [Line {line_num}] Action defined but NO audio follows.\n   Visual: {visual_lines[0]}...")
                    stats["failed"] += 1
                else:
                    # Check for Disclosure Verbs
                    has_disclosure = False
                    for verb in AUDIO_DISCLOSURE_VERBS:
                        if verb in audio_text:
                            has_disclosure = True
                            break
                    
                    if has_disclosure:
                        stats["passed"] += 1
                    else:
                        errors.append(f"⚠️ [Line {line_num}] Action defined but Audio lacks disclosure verbs.\n   Visual Action: ...{visual_content[0:50]}...\n   Audio Text:    {audio_text}")
                        stats["failed"] += 1
            
            continue # Loop continues from current 'i'

        # 6. Detect "Inverted Header" / "Toxic Merge" (Ref before Visual Header)
        # If a Ref line is immediately followed by a [VISUAL] header in the same block, 
        # the parser might confuse the anchor point (Ghost Anchor).
        # We only flag this specific toxic pattern, allowing standalone/inline Refs.
        elif line.startswith(">") and "[SLIDE:" in line:
            # Look ahead
            if i + 1 < len(lines):
                 next_line = lines[i+1].strip()
                 if next_line.startswith(">") and "[VISUAL]" in next_line:
                     errors.append(f"👻 [Line {i+1}] GHOST ANCHOR (TOXIC PATTERN): Slide Reference immediately precedes a [VISUAL] header.\n   Content: {line}\n   Next: {next_line}\n   Fix: Move the Ref *inside* (after) the [VISUAL] header.")
                     stats["failed"] += 1

        i += 1
    
    # --- Report ---
    print("\n--- INI Validation Report ---")
    print(f"Total Visual Blocks: {stats['visual_blocks']}")
    print(f"Action Blocks Found: {stats['action_blocks']}")
    print(f"✅ Verified:          {stats['passed']}")
    print(f"❌ Failed:            {stats['failed']}")
    
    if errors:
        print("\n[Violations Found]")
        for e in errors:
            print(e)
        return False
    else:
        print("\n✨ Narrative Integrity Confirmed. No invisible instructions.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_narrative_integrity.py <file>")
        sys.exit(1)
        
    success = scan_script(sys.argv[1])
    sys.exit(0 if success else 1)
