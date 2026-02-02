import glob
import re
import os

def check_file(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    filename = os.path.basename(filepath)
    
    # 1. Tags Collection and Check
    # Allowed tags (Strict): [TEACHING MOMENT], [WARNING], [VISUAL], [AUDIO], [PACING], [CULTURAL REF], [TECH NOTE], [STORY TIME], [DID YOU KNOW], [PHILOSOPHY]
    # Note: Narrative Consistency Rule 6 only explicitly mentions [TEACHING MOMENT], [WARNING], [VISUAL].
    # But files clearly use others. We will list them all.
    allowed_tags = ["TEACHING MOMENT", "WARNING", "VISUAL", "AUDIO", "PACING", "CULTURAL REF", "TECH NOTE", "STORY TIME", "DID YOU KNOW", "PHILOSOPHY"]
    
    # 2. Regex Patterns
    re_naked_audio = re.compile(r'(?<!文件: )(?<!File: )(?<!`)\basset_[\w]+\.(wav|mp3)\b(?!`)')
    re_typo_sset = re.compile(r'sset_')
    re_src_typo = re.compile(r'src_S') # Should be Sxx_
    re_invisible_action = re.compile(r'^\s*\(Action:.*\)', re.MULTILINE) # Parenthetical action without spoken text? Hard to detect strictly via regex but let's try strict format violation.
    
    # Blockquote tags pattern: > **[TAG]** or > [TAG]
    re_tag = re.compile(r'>\s*\**\[([A-Z _]+)\]\**')

    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Check Typos
        if re_typo_sset.search(line):
            issues.append(f"Line {line_num}: Found typo 'sset_' (should be 'asset_'?)")
        if re_src_typo.search(line):
            issues.append(f"Line {line_num}: Found 'src_' prefix (should be 'Sxx_'?)")
            
        # Check Naked Filenames in [AUDIO] sections
        # This is a heuristic: if we are not in a code block or link.
        matches = re_naked_audio.finditer(line)
        for m in matches:
            # check if inside [] or ()
            issues.append(f"Line {line_num}: Potential Naked Filename '{m.group(0)}' without 'File:' prefix.")

        # Check Tags
        tag_match = re_tag.search(line)
        if tag_match:
            tag = tag_match.group(1)
            if tag not in allowed_tags:
                issues.append(f"Line {line_num}: Unknown or Consistency Warning for Tag '[{tag}]'")
                
    return issues

files = sorted(glob.glob("03_Scripts/S*.md"))
print(f"Scanning {len(files)} files...")

all_issues = {}
for f in files:
    if "S05" in f: continue # Skip S05 as it was not requested
    issues = check_file(f)
    if issues:
        all_issues[f] = issues

if not all_issues:
    print("No regex issues found.")
else:
    for f, errs in all_issues.items():
        print(f"\n## {f}")
        for e in errs:
            print(f"- {e}")
