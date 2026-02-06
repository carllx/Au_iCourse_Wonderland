#!/usr/bin/env python3
"""
Build Timeline Engine - Script-to-Timeline 核心实现
用法: python build_timeline.py <Section_ID> (e.g. S03)

流程:
1. Parse Anchors from 03_Scripts/Sxx.md
2. Transcribe Audio 03_Scripts/tts/Sxx.mp3 using stable-ts
3. Build Char-Time Map
4. Fuzzy Match Anchors -> Get Start Time
5. Update 04_Delivery/h5_preview/public/slides.json
"""

import sys
import json
import re
import difflib
try:
    import stable_whisper
except ImportError:
    stable_whisper = None
from pathlib import Path

# 导入 parse_anchors
sys.path.append(str(Path(__file__).parent))
from parse_anchors import parse_anchors

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TIMELINE_JSON_PATH = PROJECT_ROOT / "03_Scripts/timeline.json"
SCRIPTS_DIR = PROJECT_ROOT / "03_Scripts"
AUDIO_DIR = PROJECT_ROOT / "03_Scripts/tts"

def normalize_text(text):
    """
    Robust Normalization:
    1. Strip Markdown links/bold (Basic)
    2. Strip Parentheticals (English/Chinese) to match TTS logic
    3. Remove punctuation/spaces/case
    """
    # 1. Strip Markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # 2. Strip Parentheticals (Crucial for matching rich MD with clean TTS)
    # Remove (...) and （...）
    text = re.sub(r'[\(\（].*?[\)\）]', '', text)
    
    # 3. Strip Non-Alphanumeric (standard normalization)
    return re.sub(r"[^\w]", "", text).lower()

def build_timeline(section_id):
    # 1. 确定文件路径
    # 查找匹配的脚本文件 (S03_Phase2_Sculpt.md)
    script_files = list(SCRIPTS_DIR.glob(f"{section_id}_*.md"))
    if not script_files:
        print(f"❌ Script not found for {section_id}")
        return
    script_path = script_files[0]
    
    # 查找匹配的音频文件 (mp3/wav)
    audio_files = list(AUDIO_DIR.glob(f"{section_id}_*.mp3")) + list(AUDIO_DIR.glob(f"{section_id}_*.wav")) + list(AUDIO_DIR.glob(f"{section_id}_*.aac"))
    if not audio_files:
        print(f"❌ Audio not found for {section_id}")
        return
    audio_path = audio_files[0]
    
    print(f"📜 Script: {script_path.name}")
    print(f"🔊 Audio:  {audio_path.name}")
    
    # 2. 解析锚点
    print("🔍 Parsing anchors...")
    anchors = parse_anchors(script_path)
    if not anchors:
        print("⚠️ No anchors found in script.")
        return
    print(f"   Found {len(anchors)} anchors.")
    
    # 3. 检查 SRT 是否存在
    srt_files = list(Path(AUDIO_DIR).glob(f"{section_id}_*.srt"))
    
    full_text = ""
    char_time_map = []
    
    if srt_files:
        srt_path = srt_files[0]
        print(f"📄 Found SRT: {srt_path.name}")
        
        # Parse SRT manually
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        blocks = re.split(r'\n\s*\n', content.strip())
        for block in blocks:
            lines = block.split('\n')
            if len(lines) < 3: continue
            
            times = lines[1]
            if '-->' not in times: continue
            
            start_str, end_str = times.split(' --> ')
            
            def to_sec(t_str):
                h, m, s = t_str.replace(',', '.').split(':')
                return int(h) * 3600 + int(m) * 60 + float(s)
            
            try:
                start = to_sec(start_str.strip())
                end = to_sec(end_str.strip())
            except:
                continue
            
            text = " ".join(lines[2:])
            clean_text = normalize_text(text)
            
            if not clean_text: continue
            
            s_duration = end - start
            char_duration = s_duration / len(clean_text)
            
            for i, char in enumerate(clean_text):
                full_text += char
                char_time_map.append(start + (i * char_duration))
                
    else:
        print("🤖 Transcribing & Aligning (this may take a while)...")
        if stable_whisper is None:
             print("❌ stable-ts not installed and no SRT found. Skipping.")
             return

        # 使用 base 模型, 强制简体中文
        model = stable_whisper.load_model('base')
        result = model.transcribe(str(audio_path), language='zh', regroup=False, initial_prompt="以下是简体中文的内容。")
        
        for segment in result.segments:
            # 如果有 word_timestamps
            if segment.words:
                for word in segment.words:
                     # ... (Keep existing logic if prefer fallback, but simplicity suggests focusing on SRT)
                     w_text = word.word
                     w_start = word.start
                     w_end = word.end
                     w_duration = w_end - w_start
                     if not w_start: continue
                     
                     clean_word = w_text.strip()
                     if not clean_word: continue
                     
                     char_duration = w_duration / len(clean_word)
                     for i, char in enumerate(clean_word):
                         full_text += char
                         char_time_map.append(w_start + (i * char_duration))
            else:
                 s_text = segment.text
                 clean_text = normalize_text(s_text)
                 if not clean_text: continue
                 s_duration = segment.end - segment.start
                 char_duration = s_duration / len(clean_text)
                 for i, char in enumerate(clean_text):
                     full_text += char
                     char_time_map.append(segment.start + (i * char_duration))
                 
    # 6. 匹配锚点 (Sequential Walking Match)
    print("🔗 Matching anchors (Sequential Mode)...")
    
    match_results = {} # slide_id -> start_time
    
    # 在 Full Text 中搜索 Anchor Text (Normalize 后)
    normalized_full_text = normalize_text(full_text)
    search_start_idx = 0  # 指针：只向后看，不回头
    
    for anchor in anchors:
        anchor_raw = anchor['anchor_text']
        anchor_norm = normalize_text(anchor_raw)
        slide_id = anchor['slide_id']
        
        if not anchor_norm: continue
        
        # 使用 sequence matcher 找最佳匹配位置
        # 关键优化: a=normalized_full_text, b=anchor_norm
        # 我们限制 a 的搜索范围从 search_start_idx 开始
        matcher = difflib.SequenceMatcher(None, normalized_full_text, anchor_norm)
        
        # find_longest_match(alo, ahi, blo, bhi)
        # alo = search_start_idx (我们只看当前指针之后的内容)
        match = matcher.find_longest_match(search_start_idx, len(normalized_full_text), 0, len(anchor_norm))
        
        # 简单阈值：匹配长度要足够大
        if match.size > len(anchor_norm) * 0.6: # 匹配度 > 60%
            start_idx = match.a
            timestamp = char_time_map[start_idx] if start_idx < len(char_time_map) else 0
            timestamp = round(timestamp, 2)
            
            if slide_id not in match_results:
                match_results[slide_id] = timestamp
                matched_snippet = normalized_full_text[match.a:match.a+match.size]
                print(f"   ✅ {slide_id}: {timestamp:.2f}s (seq={start_idx})")
                
                # [CRITICAL UPDATE]
                # 找到匹配后，将搜索指针向前推进。
                # 这样下一次搜索 "Look at screen" 时，就会从这次匹配的 *后面* 开始找。
                search_start_idx = match.a + 1 
            else:
                print(f"   ℹ️ {slide_id}: Skipped update (Duplicate ID)")
        else:
            print(f"   ❌ {slide_id}: Match failed (searched from char {search_start_idx})")
            
    # 6. 更新 timeline.json (Persistent Storage)
    print("💾 Updating timeline.json...")
    
    current_timings = {}
    if TIMELINE_JSON_PATH.exists():
        try:
            with open(TIMELINE_JSON_PATH, 'r', encoding='utf-8') as f:
                current_timings = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to read existing timeline.json: {e}")

    # 合并新数据
    current_timings.update(match_results)
    
    try:
        with open(TIMELINE_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(current_timings, f, indent=2, sort_keys=True)
        print(f"   ✅ Saved {len(match_results)} timestamps to 03_Scripts/timeline.json")
    except Exception as e:
        print(f"Error saving JSON: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_timeline.py <Section_ID>")
        sys.exit(1)
        
    build_timeline(sys.argv[1])
