#!/usr/bin/env python3
"""
Anchor Parser - 从 Markdown 脚本中提取 "Slide ID" 与 "Anchor Text" 的对应关系
核心逻辑：
1. 找到 [SLIDE: Sxx] 标记
2. 向下寻找最近的 **[AUDIO]** 标记
3. 提取 Audio 块下的第一句有效台词作为 Anchor Text
"""

import re
import sys
import json
from pathlib import Path

def parse_anchors(script_path: Path):
    if not script_path.exists():
        print(f"Error: 脚本文件不存在 {script_path}", file=sys.stderr)
        return []

    content = script_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    anchors = []
    
    # 状态机变量
    pending_slide = None
    looking_for_audio_tag = False
    
    # 正则
    # 匹配 [SLIDE: Sxx] 或 (PPT: Sxx)
    # 兼容 [Ref]: [SLIDE: Sxx] 这种嵌套写法
    slide_pattern = re.compile(r"(?:\[SLIDE:\s*|\(PPT:\s*)(S\d+[a-z]?_\w+)(?:\]|\))")
    
    # 匹配 **[AUDIO]**
    audio_tag_pattern = re.compile(r"\*\*\[AUDIO\]\*\*")
    
    # 匹配 (语气词) 或 > 引用 等非台词行
    # 我们只想要纯净的台词
    meta_pattern = re.compile(r"^\s*\(|^\s*>|^\s*#|^\s*---|^\s*$")

    for i, line in enumerate(lines):
        # 1. 扫描 Slide 标记
        slide_match = slide_pattern.search(line)
        if slide_match:
            slide_id = slide_match.group(1)
            # 如果之前有一个 pending_slide 还没找到 Audio，覆盖它 (说明连续两个 Slide，或者上一个没对应音频)
            # 或者将其作为一个无 Anchor 的 Slide (StartTime = Previous + delta)? 
            # 暂时简化策略：覆盖。因为通常 Slide 后面紧跟 Audio。
            pending_slide = slide_id
            # looking_for_audio_tag = True # No longer needed
            # print(f"Found Slide Trigger: {slide_id} at line {i+1}")
            continue
        
        # 2. 寻找台词 (Implicit Mode)
        if pending_slide:
            # 如果遇到 **[AUDIO]** 标签，仅仅是跳过它
            if audio_tag_pattern.search(line):
                continue
            
            # 先去除 Markdown (如 加粗) 以便进行元数据检测
            clean_line = re.sub(r"\*\*|__", "", line).strip()
            
            # --- Robustness Improvements (2026-02-02) ---
            # 1. Strip List Markers ("1. ", "2. ")
            clean_line = re.sub(r"^\d+\.\s*", "", clean_line)
            
            # 2. Strip Metadata Prefixes ("Technique: ", "Step: ", "Note: ")
            # If the line starts with these, it's likely metadata, not dialogue.
            # But if we strip it, we might be left with the content. 
            # Strategy: If it looks like metadata, skip the whole line? 
            # Or assume the content is spoken? 
            # For "Technique: 偷梁换柱", likely not spoken if it's a title.
            if re.match(r"^(Technique|Step|Note|Scene|Action):", clean_line, re.IGNORECASE):
                continue

            # 3. Strip Parenthetical Notes at end of line (e.g. " (End: Piercing)")
            # or within the text if they look like notes ?
            # Let's just remove anything in (...) if it's at the end, or maybe globally?
            # "S05_Needle_Pan_Radius_cap" had "2. 半径 (Radius): ..."
            # We want "半径: ..."
            clean_line = re.sub(r"\([^\)]+\)", "", clean_line).strip()
            
            # 4. Remove trailing colons/punctuation commonly used in headers
            clean_line = re.sub(r"[:：]$", "", clean_line).strip()
            # -----------------------------------------------
            
            # -----------------------------------------------
            # [PATCH 2026-02-02] Support Class A/B Semantic Tags (Spoken Content)
            # Check for > [TAG] pattern before skipping metadata
            semantic_spoken_match = re.match(r"^\s*>\s*\[(STORY TIME|PHILOSOPHY|CULTURAL REF|TEACHING MOMENT|TECH NOTE|DID YOU KNOW|WARNING)[^\]]*\]:?\s*(.*)", clean_line, re.IGNORECASE)
            if semantic_spoken_match:
                # Extract the content after the tag
                content_after_tag = semantic_spoken_match.group(2).strip()
                if content_after_tag:
                   # Treat as valid spoken anchor
                   anchor_text = content_after_tag
                   anchor_text = re.sub(r"\*\*|__", "", anchor_text)
                   anchors.append({
                       "slide_id": pending_slide,
                       "anchor_text": anchor_text,
                       "line_no": i + 1
                   })
                   pending_slide = None
                   continue

            # 跳过元数据行 (空行, 语气提示, 引用, 分割线, 镜头指示)
            # 现在 checks clean_line, 所以 **(镜头)** 变成了 (镜头), 可以被 ^\( 匹配
            if meta_pattern.match(clean_line):
                continue

            # 找到了有效台词！
            anchor_text = clean_line
            # 去除可能存在的 markdown 格式 (如 **加粗**)
            anchor_text = re.sub(r"\*\*|__", "", anchor_text)
            
            anchors.append({
                "slide_id": pending_slide,
                "anchor_text": anchor_text,
                "line_no": i + 1
            })
            
            #以此为闭环，重置状态
            pending_slide = None
            
    return anchors

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_anchors.py <path_to_script.md>")
        sys.exit(1)
        
    script_file = Path(sys.argv[1])
    result = parse_anchors(script_file)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
