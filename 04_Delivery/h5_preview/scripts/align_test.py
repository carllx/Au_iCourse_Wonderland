#!/usr/bin/env python3
"""
Align Test - 验证 "Script-to-Timeline" 的核心逻辑
用法: python align_test.py <audio_path> <anchor_text>
"""

import sys
import stable_whisper
import difflib
from pathlib import Path

def align_anchor(audio_path, anchor_text):
    print(f"Loading model... (Audio: {audio_path})")
    # 使用 base 模型进行快速验证，生产环境可用 medium/large
    model = stable_whisper.load_model('base')
    
    print("Transcribing and aligning...")
    # regroup=True 可以让结果按句子重组，提高可读性
    # initial_prompt 强制简体中文
    result = model.transcribe(str(audio_path), language='zh', regroup=True, initial_prompt="以下是简体中文的内容。")
    
    # 简单的模糊匹配策略
    best_score = 0.0
    best_segment = None
    
    # 滑动窗口或逐段匹配
    # 这里为了演示简单，直接逐段匹配
    for i, segment in enumerate(result.segments):
        segment_text = segment.text
        print(f"[{i}] {segment.start}-{segment.end}: {segment_text}")
        # 计算相似度 (0.0 - 1.0)
        ratio = difflib.SequenceMatcher(None, anchor_text, segment_text).ratio()
        
        if ratio > best_score:
            best_score = ratio
            best_segment = segment
            
        # 如果包含关系，也可以加分
        if anchor_text in segment_text:
            if ratio < 0.8: ratio = 0.8 # Boost
            if ratio > best_score:
                best_score = ratio
                best_segment = segment

    if best_segment and best_score > 0.4: # 阈值 0.4
        print(f"\n✅ Found Match (Score: {best_score:.2f})")
        print(f"   Target: {anchor_text}")
        print(f"   Actual: {best_segment.text}")
        print(f"   Timestamp: {best_segment.start}s -> {best_segment.end}s")
        return best_segment.start
    else:
        print(f"\n❌ No close match found for: {anchor_text}")
        if best_segment:
             print(f"   Best candidate (Score: {best_score:.2f}): {best_segment.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python align_test.py <audio_file> <text_to_find>")
        sys.exit(1)
        
    audio = Path(sys.argv[1])
    text = sys.argv[2]
    
    if not audio.exists():
        print(f"Audio file not found: {audio}")
        sys.exit(1)
        
    align_anchor(audio, text)
