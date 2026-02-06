#!/usr/bin/env python3
"""
Narrative Integrity Validator (INI Framework) - V2 (Unified Parser)
---------------------------------------------
A logic-based linter that enforces "Double-Entry Bookkeeping" between 
Visual Action Tags and Audio Description Text.

Rule: "If it moves the mouse (Visual), it must be spoken (Audio)."

Upgrades:
    - Uses WonderlandScriptParser for robust block identification.
    - Correctly recognizes Class A/B Tags as Narrative/Audio content.
"""

import sys
import os
import re

# Add commons to path for importing markdown_parser
# Relative path: .agent/skills/validation-suite/scripts/ -> .../01_MVP_Demo/_Pipeline/commons/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
commons_path = os.path.join(project_root, "01_MVP_Demo/_Pipeline/commons")

if commons_path not in sys.path:
    sys.path.append(commons_path)

try:
    from markdown_parser import WonderlandScriptParser, BlockType, ScriptBlock
except ImportError:
    print(f"❌ Critical Error: Could not import 'markdown_parser'. Checked path: {commons_path}")
    # Try one more fallback if running from root
    try:
        sys.path.append(os.path.join(os.getcwd(), "01_MVP_Demo/_Pipeline/commons"))
        from markdown_parser import WonderlandScriptParser, BlockType, ScriptBlock
    except ImportError:
        print("Please ensure you are running from the Project Root or have PYTHONPATH set.")
        sys.exit(1)

# --- Configuration ---

# 1. Action Triggers (Visual Side) - English
VISUAL_ACTION_TRIGGERS = [
    r"Action\*?\*?:", 
    r"\bClick\b", r"\bDrag\b", r"\bSet\b", r"\bAdjust\b", r"\bPress\b", 
    r"\bSelect\b", r"\bToggle\b", r"\bMove\b", r"\bChange\b", r"\bDraw\b", r"\bPaint\b",
    r"\bHighlight\b", r"\bShow\b", r"\bOpen\b"
]

# 2. Disclosure Verbs (Audio Side) - Chinese
AUDIO_DISCLOSURE_VERBS = [
    "点击", "点选", "按下", "按",
    "拖动", "拖拽", "拉动", "推大", "推小",
    "设置", "调整", "改为", "设为", "拉到",
    "选择", "选中", "勾选",
    "移动", "滑", "绘制", "画",
    "打开", "关闭", "启用",
    "输入", "写",
    "听", "看", "观察", "注意", "演示", "请看", "利用", "使用"
]

# 3. Implicit Parameter Patterns (Toxic Parentheses in Audio)
# Matches: string ended with (**Term**) or (Term)
IMPLICIT_PARAM_PATTERN = r"[\u4e00-\u9fff]+\s*[\(\（]\s*(?:\*\*)?([A-Za-z0-9\s]+)(?:\*\*)?\s*[\)\）]"

def scan_script(file_path):
    print(f"🔍 [INI Check V2] Scanning: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    parser = WonderlandScriptParser()
    blocks = parser.parse(lines)
    
    stats = {
        "visual_blocks": 0,
        "action_blocks": 0,
        "passed": 0,
        "failed": 0
    }
    
    errors = []
    
    # --- Check 1: Invisible Mechanics (Visual -> Audio coupling) ---
    for i, block in enumerate(blocks):
        if block.block_type == BlockType.VISUAL:
            stats["visual_blocks"] += 1
            
            # Does this visual block contain an action?
            is_action = False
            for trigger in VISUAL_ACTION_TRIGGERS:
                if re.search(trigger, block.content, re.IGNORECASE):
                    is_action = True
                    break
            
            if is_action:
                stats["action_blocks"] += 1
                
                # Scan ahead for Audio Disclosure
                found_audio = False
                audio_text = ""
                
                # Look at subsequent blocks
                # We stop if we hit another Visual block containing an Action (new cycle)
                # We allow accumulating multiple Audio chunks.
                
                scanned_count = 0
                max_scan = 10 # Safety limit
                
                for j in range(i + 1, len(blocks)):
                    next_block = blocks[j]
                    scanned_count += 1
                    
                    if next_block.block_type == BlockType.VISUAL:
                        # Check if this new visual block is ALSO an action.
                        # If so, our current action scope is definitely over.
                        is_next_action = False
                        for trigger in VISUAL_ACTION_TRIGGERS:
                            if re.search(trigger, next_block.content, re.IGNORECASE):
                                is_next_action = True
                                break
                        if is_next_action:
                            break
                    
                    if next_block.block_type == BlockType.AUDIO:
                        audio_text += next_block.content + " "
                        found_audio = True
                        
                    if scanned_count >= max_scan:
                        break
                            
                if not found_audio:
                     # Check Backward before failing completely
                    valid_link_found = False
                    if i > 0 and blocks[i-1].block_type == BlockType.AUDIO:
                        prev_text = blocks[i-1].content
                        for verb in AUDIO_DISCLOSURE_VERBS:
                            if verb in prev_text:
                                valid_link_found = True
                                break
                    
                    if valid_link_found:
                        stats["passed"] += 1
                    else:
                        # Severity: Critical
                        errors.append(f"🔴 [Line {block.line_no}] Action defined but NO audio follows (and no valid prompt precedes).\n   Visual: {block.content[:60]}...")
                        stats["failed"] += 1
                else:
                    # --- Logic Update: Support "Audio Prompt -> Visual Action" (Backward Check) ---
                    valid_link_found = False
                    
                    # Check Ahead (Standard)
                    if found_audio:
                        for verb in AUDIO_DISCLOSURE_VERBS:
                            if verb in audio_text:
                                valid_link_found = True
                                break
                                
                    # Check Behind (Prompt Mode) if forward failed
                    if not valid_link_found:
                         if i > 0 and blocks[i-1].block_type == BlockType.AUDIO:
                            prev_text = blocks[i-1].content
                            for verb in AUDIO_DISCLOSURE_VERBS:
                                if verb in prev_text:
                                    valid_link_found = True
                                    break
    
                    if valid_link_found:
                        stats["passed"] += 1
                    else:
                        # Severity: Warning (maybe implied, but risky)
                        debug_info = ""
                        if found_audio: debug_info += f"\n   [Forward Audio]: {audio_text[:40]}..."
                        if i > 0 and blocks[i-1].block_type == BlockType.AUDIO: debug_info += f"\n   [Backward Audio]: {blocks[i-1].content[:40]}..."
                        
                        errors.append(f"⚠️ [Line {block.line_no}] Action defined but Audio lacks disclosure verbs (Checked Forward & Backward).{debug_info}")
                        stats["failed"] += 1

    # --- Check 2: Toxic Ghost Anchors (Slide precedes Visual Block) ---
    # Logic: A [SLIDE] block should not be immediately followed by a [VISUAL] HEADER block.
    # We only care if the *next* block is a *new* [VISUAL] section start.
    # Continuation lines (like "> * Concept:...") are parsed as VISUAL blocks but are safe.
    
    for i in range(len(blocks) - 1):
        if blocks[i].block_type == BlockType.SLIDE:
            next_b = blocks[i+1]
            if next_b.block_type == BlockType.VISUAL:
                 # Check if the visual block is a Header or explicit new start
                 if "[VISUAL]" in next_b.content:
                    errors.append(f"👻 [Line {blocks[i].line_no}] GHOST ANCHOR DETECTED: Slide [{blocks[i].content}] sits outside/before the [VISUAL] Header.\n   Fix: Move the slide reference *inside* (after) the [VISUAL] header.")
                    stats["failed"] += 1

    # --- Check 3: Implicit Parameter Scan (The "Naked Parens" Rule) ---
    # Logic: Audio blocks should not bury key terms in parentheses like "调整大小 (Room Size)"
    # because TTS strips parentheses.
    
    for block in blocks:
        if block.block_type == BlockType.AUDIO:
            # simple check for Chinese followed immediately by (English)
            matches = re.finditer(IMPLICIT_PARAM_PATTERN, block.content)
            for m in matches:
                term = m.group(1)
                # Filter out likely stage directions (usually verbs or single words like "Laughs", "Silence")
                # We assume technical terms are capitalized or multi-word
                if len(term) > 2 and term[0].isupper(): 
                     errors.append(f"🔇 [Line {block.line_no}] IMPLICIT PARAMETER: '({term})' will be stripped by TTS.\n   Fix: Rewrite as explicit spoken text. E.g. \"...调整 **{term}**...\"")
                     stats["failed"] += 1

    # --- Report ---
    print("\n--- INI Validation Report (V2) ---")
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
        print("\n✨ Narrative Integrity Confirmed. Unified Parser Logic Applied.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_narrative_integrity.py <file>")
        sys.exit(1)
        
    success = scan_script(sys.argv[1])
    sys.exit(0 if success else 1)
