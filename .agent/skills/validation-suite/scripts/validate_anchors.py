#!/usr/bin/env python3
"""
Pre-Flight Check: Anchor Validator
----------------------------------
确保脚本中的 [SLIDE: Sxx] 标记后紧跟有效的朗读文本，避免 Timeline 对齐失败。

检查项:
1. GHOST_ANCHOR: 有 Slide ID 但无法提取到有效台词
2. WEAK_ANCHOR:  提取到的台词过短 (< 2 chars) 或包含非法字符
3. FORMAT_WARN:  台词看似是元数据 (Technique:, Note:) 但未被清理规则拦截

Usage:
    python validate_anchors.py <script_md_file>
"""

import sys
import re
import importlib.util
from pathlib import Path

# 动态加载 Production Pipeline 中的解析器，确保逻辑一致性
# 这里的路径是相对于项目根目录的硬编码，假设脚本运行在项目根目录或其子目录
def import_parser():
    possible_paths = [
        Path("04_Delivery/h5_preview/scripts/parse_anchors.py"),
        Path("../../04_Delivery/h5_preview/scripts/parse_anchors.py"), # If run from skills/validation-suite/scripts
        Path("../../../04_Delivery/h5_preview/scripts/parse_anchors.py")
    ]
    
    parser_path = None
    for p in possible_paths:
        if p.exists():
            parser_path = p
            break
            
    if not parser_path:
        # Fallback: 如果找不到文件，尝试从绝对路径寻找 (Based on User Context)
        # 这里做一个简单的查找逻辑
        current = Path.cwd()
        target = current / "04_Delivery/h5_preview/scripts/parse_anchors.py"
        if target.exists():
            parser_path = target
        else:
            print("❌ Critical Error: Could not find 'parse_anchors.py' production script.")
            print("   Please run this script from the Project Root.")
            sys.exit(1)
            
    spec = importlib.util.spec_from_file_location("parse_anchors", parser_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["parse_anchors"] = module
    spec.loader.exec_module(module)
    return module

def validate_script(script_path):
    parser = import_parser()
    
    print(f"🔍 Inspecting: {script_path}")
    
    # 1. 获取所有 Slide ID (Raw Regex)
    # 我们自己再扫一遍 Raw Content 来对比 Parser 的结果，找出遗漏的
    content = Path(script_path).read_text(encoding="utf-8")
    slide_pattern = re.compile(r"(?:\[SLIDE:\s*|\(PPT:\s*)(S\d+[a-z]?_\w+)(?:\]|\))")
    
    all_slides_defined = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        match = slide_pattern.search(line)
        if match:
            all_slides_defined.append({
                "id": match.group(1),
                "line": i + 1,
                "raw": line.strip()
            })
            
    print(f"   Found {len(all_slides_defined)} Slide definitions in raw text.")
    
    # 2. 运行解析器
    try:
        anchors = parser.parse_anchors(Path(script_path))
    except Exception as e:
        print(f"❌ Parser Crashed: {e}")
        return False

    print(f"   Parser extracted {len(anchors)} valid anchors.")
    
    # 3. 对比分析
    errors = []
    warnings = []
    
    # Map anchors by slide_id for easy lookup
    anchor_map = {a['slide_id']: a for a in anchors}
    
    for slide in all_slides_defined:
        s_id = slide['id']
        line_num = slide['line']
        
        if s_id not in anchor_map:
            # Error 1: Ghost Anchor (彻底丢了)
            errors.append(f"[Line {line_num}] 👻 GHOST ANCHOR: Slide '{s_id}' has no matching audio text.")
            continue
            
        anchor = anchor_map[s_id]
        text = anchor['anchor_text']
        
        # Error 2: Weak Anchor
        if len(text) < 2:
             errors.append(f"[Line {anchor['line_no']}] ⚠️ WEAK ANCHOR: Slide '{s_id}' matched text is too short: '{text}'")
        
        # Warning 3: Suspicious Metadata
        if re.match(r"^[A-Za-z]+:", text):
             warnings.append(f"[Line {anchor['line_no']}] ❓ SUSPICIOUS: Slide '{s_id}' matched text looks like metadata: '{text}'")

    # 4. Report
    if errors:
        print("\n❌ VALIDATION FAILED:")
        for e in errors:
            print(f"   {e}")
    else:
        print("\n✅ NO BLOCKING ERRORS")
        
    if warnings:
        print("\n⚠️  WARNINGS (Please Check Manually):")
        for w in warnings:
            print(f"   {w}")
            
    return len(errors) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_anchors.py <script_file>")
        sys.exit(1)
        
    script_file = sys.argv[1]
    success = validate_script(script_file)
    sys.exit(0 if success else 1)
