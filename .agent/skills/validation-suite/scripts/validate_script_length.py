

import os
import re
import sys
import argparse
from pathlib import Path

# Add commons directory to sys.path
current_file = Path(__file__).resolve()
project_root = current_file.parents[4] # .agent/skills/validation-suite/scripts -> ROOT
commons_dir = project_root / "01_MVP_Demo" / "_Pipeline" / "commons"
sys.path.append(str(commons_dir))

from markdown_parser import WonderlandScriptParser, BlockType


# Smart Course Standards
# Target: 60 minutes total.
# Speech Speed: ~200 chars/min (Educational Standard)
#   - Range: 180 (Slow/Deep) - 220 (Fast/Excited)
# Action Padding: Time allocated for Visual Actions.

AVG_CN_CPM = 200
AVG_EN_WPM = 130
DEFAULT_ACTION_DELAY = 5 

def strip_markdown(text):
    """Removes common markdown symbols for pure text extraction."""
    # Remove bold/italic markers
    text = re.sub(r'(\*\*|__|\*)', '', text)
    # Remove code ticks
    text = re.sub(r'`', '', text)
    # Remove link URLs [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    return text

def parse_time_str(text):
    """Extracts seconds from text like '30s', '停顿 3秒', 'Pause: 5s'"""
    # Look for explicit numbers followed by s/秒
    match = re.search(r'(\d+)\s*(s|sec|秒)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0



def analyze_file(file_path, extract_text=False, blind_mode=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Stats
    cn_count = 0
    en_count = 0
    visual_action_count = 0
    pacing_seconds = 0
    visual_seconds = 0
    text_lines = []
    
    parser = WonderlandScriptParser()
    blocks = parser.parse(lines)
    
    for block in blocks:
        if block.block_type == BlockType.AUDIO:
            clean_text = block.content
             # Count CN
            cn_count += len(re.findall(r'[\u4e00-\u9fff]', clean_text))
            # Count EN
            en_count += len(re.findall(r'[a-zA-Z0-9]+', clean_text))
            
            if extract_text and clean_text.strip():
                pure_text = strip_markdown(clean_text)
                
                if blind_mode:
                    if "Ref:" in pure_text or "[VISUAL]" in pure_text:
                        continue
                
                if pure_text.strip():
                     text_lines.append(pure_text.strip())
                     
        elif block.block_type == BlockType.VISUAL:
            if "[ACT:" in block.content:
                visual_action_count += 1
                t = parse_time_str(block.content)
                if t > 0:
                     visual_seconds += t
                else:
                     visual_seconds += DEFAULT_ACTION_DELAY

        elif block.block_type == BlockType.PACING:
            t = parse_time_str(block.content)
            pacing_seconds += t

    return {
        "cn": cn_count,
        "en": en_count,
        "actions": visual_action_count,
        "pacing_sec": pacing_seconds,
        "visual_sec": visual_seconds,
        "text_lines": text_lines
    }

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs}s"

def main():
    script_dir = "03_Scripts"
    if not os.path.exists(script_dir):
        print(f"Directory {script_dir} not found.")
        return

    parser = argparse.ArgumentParser(description="Validate script length and optionally extract text.")
    parser.add_argument("--dump-text", action="store_true", help="Extract and print pure spoken text.")
    parser.add_argument("--blind-mode", action="store_true", help="Strictly remove all visual cues for Audio-Only review.")
    args = parser.parse_args()
    
    # Enable dump_text automatically if blind_mode is on
    if args.blind_mode:
        args.dump_text = True

    # Header
    if not args.dump_text:
        print(f"{'File Name':<25} | {'Words':<10} | {'Acts':<5} | {'Pacing':<8} | {'Est. Time':<10}")
        print("-" * 80)

    total_cn = 0
    total_en = 0
    total_visuals = 0
    total_secs = 0
    
    files = sorted([f for f in os.listdir(script_dir) if f.endswith(".md")])

    for filename in files:
        if "Structure_Map" in filename:
            continue
        path = os.path.join(script_dir, filename)
        stats = analyze_file(path, extract_text=args.dump_text, blind_mode=args.blind_mode)

        if args.dump_text:
            if stats['text_lines']:
                # Construct output path
                base_name = os.path.splitext(filename)[0]
                tts_dir = os.path.join(script_dir, "tts")
                if not os.path.exists(tts_dir):
                    os.makedirs(tts_dir)
                
                suffix = "_blind" if args.blind_mode else ""
                output_path = os.path.join(tts_dir, f"{base_name}{suffix}.txt")
                
                try:
                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        for line in stats['text_lines']:
                            out_f.write(line + "\n")
                    print(f"✅ Text extracted to: {output_path}")
                except Exception as e:
                    print(f"❌ Failed to write {output_path}: {e}")
        else:
            # Duration Calc
            speech_sec = (stats['cn'] / AVG_CN_CPM * 60) + (stats['en'] / AVG_EN_WPM * 60)
            
            file_total_sec = speech_sec + stats['visual_sec'] + stats['pacing_sec']
            
            print(f"{filename:<25} | {str(stats['cn']) + '/' + str(stats['en']):<10} | {stats['actions']:<5} | {str(stats['pacing_sec']) + 's':<8} | {format_time(file_total_sec):<10}")

            total_cn += stats['cn']
            total_en += stats['en']
            total_visuals += stats['actions']
            total_secs += file_total_sec

    if not args.dump_text:
        print("-" * 80)
        
        print(f"Total Speech  : {total_cn} chars (CN) / {total_en} words (EN)")
        print(f"Total Visuals : {total_visuals} actions")
        print(f"Est. Duration : {format_time(total_secs)} (Target: 60m)")
        
        if total_secs < 45 * 60:
             print(f"::warning title=Duration Short::Total {format_time(total_secs)} is below 45m minimum.")
        elif total_secs > 75 * 60:
             print(f"::warning title=Duration Long::Total {format_time(total_secs)} exceeds 75m limit.")
        else:
             print(f"::notice title=Duration Perfect::Total {format_time(total_secs)} is within standard.")


if __name__ == "__main__":
    main()
