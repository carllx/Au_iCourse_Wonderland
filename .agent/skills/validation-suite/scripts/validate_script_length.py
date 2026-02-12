

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

def format_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m {s}s"



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
    slide_counter = 0  # 用于 Slide 序号
    
    parser = WonderlandScriptParser()
    blocks = parser.parse(lines)
    
    for block in blocks:
        if block.block_type == BlockType.AUDIO:
            raw_text = block.content
            
            # Use logic to filter out metadata/comments/visual cues first
            # We must strip markdown to get accurate counts
            pure_text = strip_markdown(raw_text)
            
            # Filter out [Attention/Audio] metadata
            if pure_text.strip().startswith("[") and pure_text.strip().endswith("]"):
                 continue
            if "[AUDIO" in pure_text or "AUDIO]" in pure_text:
                 continue

            # Filter out HTML comments
            if pure_text.strip().startswith("<!--"):
                 continue

            # Filter out Stage Directions / Notes
            if re.match(r'^[\(\（].*?[\)\）]$', pure_text.strip()):
                 continue
            
            if blind_mode:
                if "Ref:" in pure_text or "[VISUAL]" in pure_text:
                    continue
            
            if pure_text.strip():
                 # Count strictly on filtered text
                 cn_count += len(re.findall(r'[\u4e00-\u9fff]', pure_text))
                 en_count += len(re.findall(r'[a-zA-Z0-9]+', pure_text))
                 text_lines.append(pure_text.strip())
                     
        elif block.block_type == BlockType.SLIDE:
            if extract_text and not blind_mode:
                 # Newline for better readability in output
                 slide_counter += 1
                 text_lines.append(f"\n[SLIDE #{slide_counter}: {block.content}]")

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

def extract_vocabulary(text):
    """Extracts English terms/phrases from text."""
    # Match sequences of English/Numbers/Extended Latin that might contain spaces/hyphens/dots/plus in between
    # e.g. "Noise Reduction", "Shift + P", "Voss", "Einstürzende"
    # Added slash for "1/f"
    # Added \u00C0-\u00FF for Latin-1 Supplement (Accents, Umlauts etc.)
    pattern = r'(?:[a-zA-Z0-9\u00C0-\u00FF]+(?:[\s\+\-\.\/]+[a-zA-Z0-9\u00C0-\u00FF]+)*)'
    matches = re.findall(pattern, text)
    
    stop_words = {
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are", "as", "with", 
        "his", "they", "i", "at", "be", "this", "have", "from", "or", "one", "had", "by", "word", "but", "not", "what", 
        "all", "were", "we", "when", "your", "can", "said", "there", "use", "an", "each", "which", "she", "do", "how", 
        "their", "if", "will", "up", "other", "about", "out", "many", "then", "them", "these", "so", "some", "her", 
        "would", "make", "like", "him", "into", "time", "has", "look", "two", "more", "write", "go", "see", "number", 
        "no", "way", "could", "people", "my", "than", "first", "water", "been", "call", "who", "oil", "its", "now", 
        "find", "long", "down", "day", "did", "get", "come", "made", "may", "part", "action", "step", "note", "scene", 
        "context", "role", "tone", "warning", "result", "act", "ref", "slide", "ppt"
    }

    vocab = []
    for m in matches:
        m = m.strip()
        m_lower = m.lower()
        
        # 1. Length Check (Chars)
        if len(m) <= 1 and m_lower not in ['i', 'a']:
            continue
            
        # 2. Word Count Check (Max 6 words)
        words = m.split()
        if len(words) > 6:
            continue
            
        # 3. Stopword Check (If single word is stopword, drop. If phrase starts/ends with stopword, clean?)
        # For now, just drop if the *entire* match is in stop words
        if m_lower in stop_words:
            continue
        
        # 4. Pure Number Check (Drop "2026", "10", "0")
        if re.match(r'^[\d\-\.\/]+$', m):
            # Exception: "1/f", "5.1", "44.1kHz" (has letters)
            # If it has letters, it won't match ^[\d\-\.\/]+$
            # So "1/f" passes. "44.1kHz" passes. "2026" fails. "0-10" fails.
            continue
            
        # 5. Start/End Cleaning (Remove trailing particles like " of", " the"?)
        # Maybe too complex for regex match.
        
        vocab.append(m)
    return vocab

def main():
    script_dir = "03_Scripts"
    if not os.path.exists(script_dir):
        print(f"Directory {script_dir} not found.")
        return

    parser = argparse.ArgumentParser(description="Validate script length and optionally extract text.")
    parser.add_argument("--dump-text", action="store_true", help="Extract and print pure spoken text with visual markers.")
    parser.add_argument("--blind-mode", action="store_true", help="Extract and print pure spoken text without visual markers.")
    parser.add_argument("--dump-vocab", action="store_true", help="Extract unique English vocabulary list.")
    args = parser.parse_args()
    
    # Header
    # If standard mode, print header
    if not (args.blind_mode or args.dump_text or args.dump_vocab):
        print(f"{'File Name':<25} | {'Words':<10} | {'Acts':<5} | {'Pacing':<8} | {'Est. Time':<10}")
        print("-" * 80)
    elif args.blind_mode and not args.dump_text:
        # Blind Header
         print(f"{'File Name (Blind)':<25} | {'Words':<10} | {'Pacing':<8} | {'Est. Time':<10}")
         print("-" * 80)

    total_cn = 0
    total_en = 0
    total_visuals = 0
    total_secs = 0
    
    all_vocab_by_chapter = {}

    files = sorted([f for f in os.listdir(script_dir) if f.endswith(".md")])

    for filename in files:
        if "Structure_Map" in filename or filename.endswith("_Report.md") or filename.startswith("Extension_"):
             if filename.endswith("_Report.md"): 
                 continue
             if "Structure_Map" in filename:
                 continue
        
        path = os.path.join(script_dir, filename)
        
        # 1. Standard Analysis logic
        # Only run standard if not in blind mode OR explicitly asked for dump
        run_standard = not args.blind_mode or args.dump_text
        
        if run_standard:
            stats_full = analyze_file(path, extract_text=True, blind_mode=False)

            if not (args.dump_text or args.dump_vocab) and not args.blind_mode:
                 # Standard Reporting
                 speech_sec = (stats_full['cn'] / AVG_CN_CPM * 60) + (stats_full['en'] / AVG_EN_WPM * 60)
                 file_total_sec = speech_sec + stats_full['visual_sec'] + stats_full['pacing_sec']
                 
                 print(f"{filename:<25} | {str(stats_full['cn']) + '/' + str(stats_full['en']):<10} | {stats_full['actions']:<5} | {str(stats_full['pacing_sec']) + 's':<8} | {format_time(file_total_sec):<10}")
                 
                 total_cn += stats_full['cn']
                 total_en += stats_full['en']
                 total_visuals += stats_full['actions']
                 total_secs += file_total_sec

            # Dump Standard Text
            if args.dump_text:
                if stats_full['text_lines']:
                    base_name = os.path.splitext(filename)[0]
                    tts_dir = os.path.join(script_dir, "tts")
                    if not os.path.exists(tts_dir):
                        os.makedirs(tts_dir)
                    
                    output_path = os.path.join(tts_dir, f"{base_name}.txt")
                    try:
                        with open(output_path, 'w', encoding='utf-8') as out_f:
                            for line in stats_full['text_lines']:
                                out_f.write(line + "\n")
                        print(f"✅ [Standard] Extracted to: {output_path}")
                    except Exception as e:
                        print(f"❌ Failed to write {output_path}: {e}")

        # 2. Blind Mode Logic (Stats & Dump)
        if args.blind_mode or args.dump_vocab:
            # Re-run analysis in blind mode
            stats_blind = analyze_file(path, extract_text=True, blind_mode=True)
            
            # Blind Stats Reporting
            if args.blind_mode and not args.dump_text:
                speech_sec = (stats_blind['cn'] / AVG_CN_CPM * 60) + (stats_blind['en'] / AVG_EN_WPM * 60)
                # For blind mode, ignore visual_sec (demo padding), but include PACING
                # Blind means "Audio Only" experience. Pacing (silence) is part of audio. Visual padding is waiting for screen.
                blind_total_sec = speech_sec + stats_blind['pacing_sec']
                
                print(f"{filename:<25} | {str(stats_blind['cn']) + '/' + str(stats_blind['en']):<10} | {str(stats_blind['pacing_sec']) + 's':<8} | {format_time(blind_total_sec):<10}")
                
                total_cn += stats_blind['cn']
                total_en += stats_blind['en']
                total_secs += blind_total_sec

            # Dump Blind Text
            if args.blind_mode and stats_blind['text_lines']:
                base_name = os.path.splitext(filename)[0]
                tts_dir = os.path.join(script_dir, "tts")
                if not os.path.exists(tts_dir):
                    os.makedirs(tts_dir)

                output_path = os.path.join(tts_dir, f"{base_name}_blind.txt")
                try:
                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        for line in stats_blind['text_lines']:
                            out_f.write(line + "\n")
                    if args.dump_text: # only log if dumping text too, to avoid clutter in stats view? Or log anyway?
                         print(f"✅ [Blind   ] Extracted to: {output_path}")
                except Exception as e:
                    print(f"❌ Failed to write {output_path}: {e}")
            
            # Vocab Collection
            if args.dump_vocab and stats_blind['text_lines']:
                 chapter_vocab = set()
                 for line in stats_blind['text_lines']:
                      terms = extract_vocabulary(line)
                      for t in terms:
                           chapter_vocab.add(t)
                 all_vocab_by_chapter[filename] = chapter_vocab

    # 5. Write Vocab List
    if args.dump_vocab and all_vocab_by_chapter:
        tts_dir = os.path.join(script_dir, "tts")
        if not os.path.exists(tts_dir):
            os.makedirs(tts_dir)
        vocab_path = os.path.join(tts_dir, "Vocabulary_List.md")
        
        try:
             with open(vocab_path, 'w', encoding='utf-8') as f:
                 f.write("# Course Vocabulary List\n")
                 f.write(f"Generated from {len(all_vocab_by_chapter)} chapters.\n\n")
                 
                 for filename in sorted(all_vocab_by_chapter.keys()):
                      terms = sorted(list(all_vocab_by_chapter[filename]), key=lambda x: x.lower())
                      base_name = os.path.splitext(filename)[0]
                      
                      f.write(f"\n## {base_name}\n")
                      if not terms:
                           f.write("_No significant English vocabulary found._\n")
                      else:
                           for term in terms:
                                f.write(f"- {term}\n")
                                
             print(f"✅ [Vocab   ] Extracted vocabulary to: {vocab_path}")
        except Exception as e:
             print(f"❌ Failed to write vocabulary list: {e}")

    # Summary Footer
    if not (args.dump_text or args.dump_vocab): # Show footer for Standard OR Blind stats
        print("-" * 80)
        print(f"Total Speech  : {total_cn} chars (CN) / {total_en} words (EN)")
        if not args.blind_mode:
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
