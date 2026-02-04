#!/usr/bin/env python3
"""
Syntax Validator (Radio Play Protocol)
---------------------------------------------
Checks for forbidden syntax in the spoken parts of the script.

Forbidden:
1. " > " (Navigation Paths) -> Should be natural language.

Usage:
    python validate_syntax.py <script_file>
"""

import sys
import re
from pathlib import Path

def scan_syntax(file_path):
    print(f"🔍 [Syntax Check] Scanning: {file_path}")
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        return False
        
    try:
        content = Path(file_path).read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

    lines = content.splitlines()
    errors = []
    
    # Regex for " > " with surrounding spaces.
    # We want to avoid flagging HTML like <br> or <tag>, but usually those don't have spaces around >.
    # The problematic pattern is exactly " > ".
    forbidden_pattern = re.compile(r" \> ")

    for i, line in enumerate(lines):
        stripped = line.strip()
        line_num = i + 1
        
        # skip empty
        if not stripped:
            continue
            
        # skip metadata blockquotes (start with >)
        # Handle standard blockquotes and nested blockquotes in lists (e.g. "  - > [Note]")
        # Regex: optional whitespace, optional list marker, optional whitespace, then >
        if re.match(r'^\s*([-*+]|\d+\.)?\s*>', line):
            continue
            
        # skip headers
        if stripped.startswith("#"):
            continue
            
        # skip separators
        if stripped.startswith("---"):
            continue
        
        # Check for forbidden " > "
        if forbidden_pattern.search(line):
            errors.append(f"❌ [Line {line_num}] Forbidden Navigation Syntax ' > ' found: '{stripped}'\n   Fix: Replace with natural language (e.g. 'Click File, then New...').")

        # Check for forbidden Numbered Lists "1. "
        # We want to avoid lists in spoken text. They should be "First, ... Second, ..."
        if re.match(r'^\s*\d+\.\s+', line):
             errors.append(f"❌ [Line {line_num}] Forbidden Numbered List found: '{stripped}'\n   Fix: Replace bullets with natural language (e.g. 'First...', 'Then...').")

    if errors:
        print("\n[Violations Found]")
        for e in errors:
            print(e)
        return False
    else:
        print("\n✨ Syntax Check Passed. No forbidden navigation paths.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_syntax.py <file>")
        sys.exit(1)
        
    success = scan_syntax(sys.argv[1])
    sys.exit(0 if success else 1)
