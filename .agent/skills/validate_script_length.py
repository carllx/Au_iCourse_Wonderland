
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

    # Pre-cleaning
    # Remove image links completely: ![alt](url)
    content_no_imgs = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    # Replace links with text: [text](url) -> text
    content_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content_no_imgs)
    # Remove headers markers
    content_clean = re.sub(r'#{1,6}\s', '', content_clean)
    # Remove bold/italic markers
    content_clean = content_clean.replace('*', '').replace('_', '')

    # 1. Count Text
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content_clean)
    num_chinese = len(chinese_chars)
    
    english_words = re.findall(r'[a-zA-Z0-9]+', content_clean)
    num_english = len(english_words)

    # 2. Count "Time Sinks" (Actions & Playback)
    # Looking for patterns like (操作: ...), (播放...), [ACTION: ...]
    # We'll use a regex to capture these directive lines.
    
    # Matches lines starting with (操作 or [ACTION or (播放
    # Or embedded markers.
    action_counts = len(re.findall(r'\(操作:|\[ACTION:', content))
    playback_counts = len(re.findall(r'\(播放', content))

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
    
    TARGET_MIN = 55
    TARGET_MAX = 65
    
    grand_total_mins = grand_total_sec / 60
    
    if grand_total_mins < TARGET_MIN:
        print(f"STATUS: SHORT. Add approx {int(TARGET_MIN - grand_total_mins)} mins of content.")
    elif grand_total_mins > TARGET_MAX:
        print(f"STATUS: LONG. Cut approx {int(grand_total_mins - TARGET_MAX)} mins of content.")
    else:
        print("STATUS: PERFECT. Within 60min standard (+/- 5min).")

    print("\n(Params: CN Speed=240cpm, EN Speed=130wpm, Action=15s, Playback=20s)")

if __name__ == "__main__":
    main()
