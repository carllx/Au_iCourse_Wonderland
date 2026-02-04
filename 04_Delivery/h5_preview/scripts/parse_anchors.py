#!/usr/bin/env python3
"""
Anchor Parser - 从 Markdown 脚本中提取 "Slide ID" 与 "Anchor Text" 的对应关系
核心逻辑：
1. 找到 [SLIDE: Sxx] 标记
2. 向下寻找最近的 **[AUDIO]** 标记
3. 提取 Audio 块下的第一句有效台词作为 Anchor Text
"""

import sys
from pathlib import Path
import json

# Add commons directory to sys.path to allow direct import
current_file = Path(__file__).resolve()
project_root = current_file.parents[3] # 04_Delivery/h5_preview/scripts -> project_root
commons_dir = project_root / "01_MVP_Demo" / "_Pipeline" / "commons"
sys.path.append(str(commons_dir))

from markdown_parser import WonderlandScriptParser, BlockType


def parse_anchors(script_path: Path):
    if not script_path.exists():
        print(f"Error: 脚本文件不存在 {script_path}", file=sys.stderr)
        return []

    content = script_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    content = script_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    anchors = []
    parser = WonderlandScriptParser()
    blocks = parser.parse(lines)
    
    pending_slide = None
    processed_slides = set()
    
    for block in blocks:
        if block.block_type == BlockType.SLIDE:
            pending_slide = block.content # Slide ID
            continue
            
        if block.block_type == BlockType.AUDIO:
            if pending_slide or block.slide_id:
                # Use the slide_id from the block if available (for semantic blocks associated with prev slide)
                # Or the current pending slide.
                target_slide = block.slide_id if block.slide_id else pending_slide
                
                if target_slide and target_slide not in processed_slides:
                    anchors.append({
                        "slide_id": target_slide,
                        "anchor_text": block.content,
                        "line_no": block.line_no
                    })
                    processed_slides.add(target_slide)

    # Re-evaluating the usage of parser output.
    # The parser returns blocks.
    # ScriptBlock has .slide_id field.
    # If the parser logic correctly assigned slide_id to AUDIO blocks, we just need to filter and map.
    
    for block in blocks:
        if block.block_type == BlockType.AUDIO and block.slide_id:
             anchors.append({
                "slide_id": block.slide_id,
                "anchor_text": block.content,
                "line_no": block.line_no
            })
            
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
