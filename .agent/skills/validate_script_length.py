
import os
import re

# Refined constraints for a 60-minute tutorial
# Target: 60 minutes total.
# Speech Speed: ~220-240 chars/min (Teaching pace, clearer and slower than conversation)
# English Speed: ~130 words/min
# Action Padding: Time allocated for user to watch an action or listen to a sample.

AVG_CN_CPM = 240
AVG_EN_WPM = 130
Action_Delay_Seconds = 15  # Avg time for an operation step
Playback_Delay_Seconds = 20 # Avg time for listening to a sample

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Count "Time Sinks" (Actions & Playback) BEFORE cleaning
    # Matches lines starting with (操作 or [ACTION or (播放
    action_counts = len(re.findall(r'\(操作:|\[ACTION:', content))
    playback_counts = len(re.findall(r'\(播放', content))

    # 2. Clean Text for Speech Counting
    # 2. Clean Text for Speech Counting
    # STRATEGY: Structure over Content
    
    # Remove Metadata (lines starting with >)
    content_clean = re.sub(r'^>.*$', '', content, flags=re.MULTILINE)
    
    # Remove Headers (lines starting with #)
    content_clean = re.sub(r'^#+.*$', '', content_clean, flags=re.MULTILINE)
    
    # Remove Stage Directions (Strict Structural Rule)
    # Rule: Any line that looks like **(...)** is a stage direction.
    # Regex: Start of line, optional whitespace, **, (, anything, ), **, optional whitespace, End of line.
    content_clean = re.sub(r'^\s*\*\*\(.*?\)\*\*\s*$', '', content_clean, flags=re.MULTILINE)
    
    # Remove Standalone Tags [ACTION:...]
    content_clean = re.sub(r'\[(ACTION|SLIDE|REF).*?\]', '', content_clean, flags=re.IGNORECASE)
    
    # Remove explicit visual cues if they slipped into text (fallback)
    # Still keep this but make it less aggressive? 
    # Actually, user wants to rely on rules. Let's stick to the Structural Rule mostly.
    # But for backward compatibility with existing files (S01, S02), 
    # we might need to support the old (操作:...) format until they are refactored.
    # However, to be "Robust", we should encourage updating the files.
    # For now, I will keep the explicit parenthesis removal for safety, but make it work inline too.
    content_clean = re.sub(r'\((操作|PPT|镜头|播放|Deep Listening|Demonstration|Demo|Ref|Action).*?\)', '', content_clean, flags=re.IGNORECASE)
    
    # Remove image links completely: ![alt](url)
    content_clean = re.sub(r'!\[.*?\]\(.*?\)', '', content_clean)
    # Replace links with text: [text](url) -> text
    content_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content_clean)
    
    # Remove formatting markers (*, _)
    content_clean = content_clean.replace('*', '').replace('_', '')

    # 1. Count Text
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content_clean)
    num_chinese = len(chinese_chars)
    
    english_words = re.findall(r'[a-zA-Z0-9]+', content_clean)
    num_english = len(english_words)

    # (Action counts moved to top)

    return {
        "cn": num_chinese,
        "en": num_english,
        "actions": action_counts,
        "playbacks": playback_counts
    }

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}m {secs}s"

def main():
    script_dir = "01_Scripts"
    if not os.path.exists(script_dir):
        print(f"Directory {script_dir} not found.")
        return

    total_cn = 0
    total_en = 0
    total_actions = 0
    total_playbacks = 0

    print(f"{'File Name':<25} | {'Words(C/E)':<12} | {'Actions':<8} | {'Est. Time':<10}")
    print("-" * 65)

    files = sorted([f for f in os.listdir(script_dir) if f.endswith(".md")])
    
    for filename in files:
        if "Structure_Map" in filename:
            continue
        path = os.path.join(script_dir, filename)
        stats = analyze_file(path)
        
        # Calculate file duration
        speech_time_sec = (stats['cn'] / AVG_CN_CPM * 60) + (stats['en'] / AVG_EN_WPM * 60)
        action_time_sec = (stats['actions'] * Action_Delay_Seconds) + (stats['playbacks'] * Playback_Delay_Seconds)
        total_file_sec = speech_time_sec + action_time_sec
        
        print(f"{filename:<25} | {str(stats['cn']) + '/' + str(stats['en']):<12} | {str(stats['actions']) + '/' + str(stats['playbacks']):<8} | {format_time(total_file_sec):<10}")

        total_cn += stats['cn']
        total_en += stats['en']
        total_actions += stats['actions']
        total_playbacks += stats['playbacks']

    print("-" * 65)
    
    # Grand Totals
    total_speech_sec = (total_cn / AVG_CN_CPM * 60) + (total_en / AVG_EN_WPM * 60)
    total_action_sec = (total_actions * Action_Delay_Seconds) + (total_playbacks * Playback_Delay_Seconds)
    grand_total_sec = total_speech_sec + total_action_sec
    
    print(f"Total Speech Content : {total_cn} CN chars + {total_en} EN words")
    print(f"Total Operations     : {total_actions} Actions + {total_playbacks} Playbacks")
    print("-" * 30)
    print(f"Est. Speech Time     : {format_time(total_speech_sec)}")
    print(f"Est. Action/Demo Time: {format_time(total_action_sec)}")
    print(f"TOTAL COURSE TIME    : {format_time(grand_total_sec)}")
    print("-" * 30)
    
    grand_total_mins = grand_total_sec / 60
    
    # Define thresholds
    MIN_PASS = 55
    MAX_PASS = 65
    
    MIN_WARN = 45
    MAX_WARN = 75
    
    if grand_total_mins < MIN_WARN:
        # Severe Under (< 45 min)
        # Using ::error:: for red visibility, but exiting 0 to not block.
        print(f"::error title=Course Duration Critical::Severe Shortage! Total: {format_time(grand_total_sec)}. Target: 60m.")
        print(f"STATUS: CRITICAL SHORT. Add {int(MIN_PASS - grand_total_mins)} mins immediately.")
    
    elif grand_total_mins > MAX_WARN:
        # Severe Over (> 75 min)
        print(f"::error title=Course Duration Critical::Severe Any! Total: {format_time(grand_total_sec)}. Target: 60m.")
        print(f"STATUS: CRITICAL LONG. Cut {int(grand_total_mins - MAX_PASS)} mins immediately.")

    elif grand_total_mins < MIN_PASS:
        # Warning Under (45-55 min)
        print(f"::warning title=Course Duration Warning::Slightly Short. Total: {format_time(grand_total_sec)}.")
        print(f"STATUS: SHORT (Yellow). Consider adding {int(MIN_PASS - grand_total_mins)} mins.")

    elif grand_total_mins > MAX_PASS:
        # Warning Over (65-75 min)
        print(f"::warning title=Course Duration Warning::Slightly Long. Total: {format_time(grand_total_sec)}.")
        print(f"STATUS: LONG (Yellow). Consider cutting {int(grand_total_mins - MAX_PASS)} mins.")

    else:
        # Green (55-65 min)
        print(f"::notice title=Course Duration Passed::Perfect! Total: {format_time(grand_total_sec)}.")
        print("STATUS: PERFECT (Green). Within 60min standard.")

    # Always exit 0 to not block CI unless specifically desired, 
    # but the ::error annotations will mark the run as "check failed" in some views 
    # while letting the pipeline continue if 'continue-on-error' is set or if exit code is 0 (annotations don't stop build unless exit code != 0).
    # Wait, actually ::error:: annotation does NOT automatically fail the build if return code is 0. 
    # It just shows a red failure annotation. This is exactly what user wants.
    exit(0)

    print("\n(Params: CN Speed=240cpm, EN Speed=130wpm, Action=15s, Playback=20s)")

if __name__ == "__main__":
    main()
