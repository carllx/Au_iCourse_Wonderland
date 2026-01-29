import os
import re
import sys

# Pedagogy Rules Configuration
# 1. Narrative Keywords (Director's Voice)
# We expect these words to appear near technical parameters (numbers)
NARRATIVE_KEYWORDS = [
    "故事", "因为", "为了", "感受", "听到", "想象", "代表", "隐喻", 
    "角色", "情感", "人性", "脆弱", "深渊", "梦境", "打破", "营造",
    "Story", "Reason", "Feel", "Imagine", "Metaphor", "Character"
]

# 2. Silence/Deep Listening Tags
# We expect at least one of these tags in the script
SILENCE_TAGS = [
    r"\(Silence:.*?\)",
    r"\(留白:.*?\)",
    r"\(Wait:.*?\)"
]

def check_naked_numbers(content, filename):
    """
    Scans for technical parameters (numbers) and checks if they have 
    narrative justification nearby (-200 to +200 chars).
    """
    errors = []
    # Match numbers that are likely parameters (e.g. "3000ms", "+3", "75%", "0.5")
    # Exclude simple list indices "1." or "Step 1" if possible, but keeping it simple first.
    # Regex: Look for digits, potentially with signs or decimals, followed by optional unit strings?
    # Actually, a safer bet for "Naked Numbers" is just picking any significant number and checking context.
    
    # Let's target specific Audition parameters to avoid false positives on list numbers
    # Patterns: "+3", "-5dB", "3000ms", "48kHz", "75%"
    param_pattern = re.compile(r'([+-]?\d+\.?\d*(ms|Hz|dB|%|st|semitones|s))')
    
    lines = content.split('\n')
    full_text = content
    
    warnings = []
    
    for i, line in enumerate(lines, 1):
        # Skip headers, metadata, and comments
        if line.startswith('#') or line.startswith('>') or line.startswith('<!--'):
            continue
            
        matches = param_pattern.findall(line)
        for match in matches:
            number_str = match[0]
            
            # Get Context window
            start = max(0, full_text.find(line) - 200)
            end = min(len(full_text), full_text.find(line) + len(line) + 200)
            context = full_text[start:end]
            
            # Check for keywords
            has_narrative = any(kw in context for kw in NARRATIVE_KEYWORDS)
            
            if not has_narrative:
                warnings.append(f"{filename}:{i} - ⚠️ Naked Parameter Detected: '{number_str}'. No narrative keywords found nearby. (Add 'Story/Reason/Feeling')")

    return warnings

def check_deep_listening(content, filename):
    """
    Ensures the script contains at least one Silence/Listening gap.
    """
    for pattern in SILENCE_TAGS:
        if re.search(pattern, content, re.IGNORECASE):
            return [] # Passed
            
    return [f"{filename}: ❌ Missing 'Deep Listening' moment. Please add '(Silence: 10s)' or similar to allow students to listen."]

def validate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    filename = os.path.basename(file_path)
    issues = []
    
    # 1. Deep Listening Check
    issues.extend(check_deep_listening(content, filename))
    
    # 2. Naked Number Check
    issues.extend(check_naked_numbers(content, filename))
    
    return issues

if __name__ == "__main__":
    # Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    scripts_dir = os.path.join(base_dir, "03_Scripts")
    
    print("🎭 Pedagogy Audit: Checking for Director's Voice & Deep Listening...")
    
    total_issues = 0
    
    if not os.path.exists(scripts_dir):
        print(f"Error: Scripts directory not found at {scripts_dir}")
        sys.exit(1)

    for filename in sorted(os.listdir(scripts_dir)):
        if filename.endswith(".md") and filename.startswith("S"):
            file_path = os.path.join(scripts_dir, filename)
            issues = validate_file(file_path)
            
            if issues:
                print(f"\n📄 {filename}:")
                for issue in issues:
                    print(f"  {issue}")
                total_issues += len(issues)
            else:
                 # Optional: Print clean files?
                 pass

    if total_issues > 0:
        print(f"\n⚠️ Audit Completed. Found {total_issues} pedagogical issues.")
        # We don't exit(1) for warnings yet, unless we want to block CI. 
        # For Phase 1, let's keep it as warnings (exit 0) or strict (exit 1)?
        # User implies strictness. Let's return verification failure if Deep Listening is missing, but maybe just warn for Naked Numbers?
        # Let's be strict.
        sys.exit(1)
    else:
        print("\n✅ Pedagogy Audit Passed: All scripts have Soul.")
        sys.exit(0)
