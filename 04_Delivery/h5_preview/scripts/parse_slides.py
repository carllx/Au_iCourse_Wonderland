#!/usr/bin/env python3
"""
Slide 数据解析器 - 生成 H5 预览所需的 slides.json

数据源:
  - 02_Visuals/Slide_Database.md (视觉内容 SSOT)
  - 03_Scripts/00_Structure_Map.md (章节结构)
  - 03_Scripts/Sxx_Name.md (翻页标记)
  
输出:
  - 04_Delivery/h5_preview/public/slides.json
"""

import json
import os
import re
from pathlib import Path

# 项目根目录 (从 04_Delivery/h5_preview/scripts/ 向上 3 层)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SLIDE_DB_PATH = PROJECT_ROOT / "02_Visuals" / "Slide_Database.md"
STRUCTURE_MAP_PATH = PROJECT_ROOT / "03_Scripts" / "00_Structure_Map.md"
SCRIPTS_DIR = PROJECT_ROOT / "03_Scripts"
TTS_DIR = SCRIPTS_DIR / "tts"
OUTPUT_PATH = PROJECT_ROOT / "04_Delivery" / "h5_preview" / "public" / "slides.json"

# ============================================================
# 布局模板 (Layout Templates) - 移植自 scaffold_visual_assets.py
# ============================================================

LAYOUT_TEMPLATES = {
    'Motion Graphic': {
        'zones': [
            {'name': 'TITLE', 'x': 0.1, 'y': 0.35, 'w': 0.8, 'h': 0.15},
            {'name': 'SUBTITLE', 'x': 0.2, 'y': 0.55, 'w': 0.6, 'h': 0.08},
            {'name': 'VISUAL', 'x': 0.3, 'y': 0.7, 'w': 0.4, 'h': 0.15},
        ],
        'is_centered': True
    },
    'UI Graphic': {
        'zones': [
            {'name': 'TITLE', 'x': 0.05, 'y': 0.05, 'w': 0.9, 'h': 0.12},
            {'name': 'LIST', 'x': 0.05, 'y': 0.2, 'w': 0.45, 'h': 0.6},
            {'name': 'VISUAL', 'x': 0.52, 'y': 0.2, 'w': 0.43, 'h': 0.6},
        ],
        'is_centered': False
    },
    'UI Composite': {
        'zones': [
            {'name': 'TITLE', 'x': 0.05, 'y': 0.05, 'w': 0.9, 'h': 0.1},
            {'name': 'LEFT PANEL', 'x': 0.05, 'y': 0.18, 'w': 0.43, 'h': 0.6},
            {'name': 'RIGHT PANEL', 'x': 0.52, 'y': 0.18, 'w': 0.43, 'h': 0.6},
            {'name': 'CAPTION', 'x': 0.1, 'y': 0.82, 'w': 0.8, 'h': 0.1},
        ],
        'is_centered': False
    },
    'Diagram': {
        'zones': [
            {'name': 'TITLE', 'x': 0.1, 'y': 0.08, 'w': 0.8, 'h': 0.1},
            {'name': 'DIAGRAM', 'x': 0.1, 'y': 0.22, 'w': 0.8, 'h': 0.55},
            {'name': 'CAPTION', 'x': 0.15, 'y': 0.82, 'w': 0.7, 'h': 0.1},
        ],
        'is_centered': True
    },
    'Concept Art': {
        'zones': [
            {'name': 'VISUAL (Full Bleed)', 'x': 0.0, 'y': 0.0, 'w': 1.0, 'h': 0.85},
            {'name': 'CAPTION', 'x': 0.1, 'y': 0.87, 'w': 0.8, 'h': 0.1},
        ],
        'is_centered': True
    },
    'Stock/Reference': {
        'zones': [
            {'name': 'IMAGE', 'x': 0.1, 'y': 0.1, 'w': 0.8, 'h': 0.7},
            {'name': 'SOURCE', 'x': 0.2, 'y': 0.85, 'w': 0.6, 'h': 0.08},
        ],
        'is_centered': True
    },
    'Live Demo': {
        'zones': [
            {'name': 'TITLE', 'x': 0.05, 'y': 0.05, 'w': 0.9, 'h': 0.1},
            {'name': 'TARGET', 'x': 0.05, 'y': 0.18, 'w': 0.4, 'h': 0.08},
            {'name': 'DURATION', 'x': 0.5, 'y': 0.18, 'w': 0.45, 'h': 0.08},
            {'name': 'ACTION_SCENE', 'x': 0.05, 'y': 0.3, 'w': 0.9, 'h': 0.5},
            {'name': 'CAPTION', 'x': 0.1, 'y': 0.82, 'w': 0.8, 'h': 0.1},
        ],
        'is_centered': False
    }
}

# ============================================================
# 解析器
# ============================================================

def parse_slide_database(db_path: Path) -> dict:
    """解析 Slide_Database.md，返回 {slide_id: slide_data}"""
    if not db_path.exists():
        return {}
    content = db_path.read_text(encoding="utf-8")
    slides = {}
    
    # 匹配 ## Sxx_ID 格式的标题
    slide_pattern = r"^##\s+(S\d+[a-z]?_\S+)"
    current_slide = None
    current_lines = []
    
    for line in content.split("\n"):
        match = re.match(slide_pattern, line)
        if match:
            # 保存上一个 slide
            if current_slide:
                slides[current_slide] = parse_slide_block(current_lines)
            current_slide = match.group(1)
            current_lines = []
        elif current_slide:
            current_lines.append(line)
    
    # 保存最后一个 slide
    if current_slide:
        slides[current_slide] = parse_slide_block(current_lines)
    
    return slides


def parse_slide_block(lines: list) -> dict:
    """解析单个 Slide 块的内容"""
    data = {
        "type": "Unknown",
        "text": "",
        "sub": "",
        "list": [],
        "visual": "",
        "caption": "",
        "concept": "",
        "action": "",
        "target": "",
        "duration": "",
    }
    
    content = "\n".join(lines)
    
    # 提取 Type: \*\*Type\*\*: \[(.*?)\]
    type_match = re.search(r"\*\s+\*\*Type\*\*:\s*\[(.*?)\]", content)
    if type_match:
        data["type"] = type_match.group(1)
    
    # 提取 Text
    text_match = re.search(r"\*\s+\*\*Text\*\*:?\s*(.+?)(?:\n|$)", content)
    if text_match:
        data["text"] = text_match.group(1).strip()
    
    # 提取 Sub
    sub_match = re.search(r"\*\s+\*\*Sub\*\*:?\s*(.+?)(?:\n|$)", content)
    if sub_match:
        data["sub"] = sub_match.group(1).strip()
    
    # 提取 List (多行)
    if "**List**:" in content:
        list_items = []
        in_list = False
        for line in lines:
            if "**List**:" in line:
                in_list = True
                continue
            if in_list:
                item_match = re.match(r"\s+\*\s+(.+)", line)
                if item_match:
                    list_items.append(item_match.group(1).strip())
                elif line.strip() and not line.startswith("*"):
                    in_list = False
        data["list"] = list_items
    
    # 提取 Visual
    visual_match = re.search(r"\*\s+\*\*Visual\*\*:?\s*(.+?)(?:\n|$)", content)
    if visual_match:
        data["visual"] = visual_match.group(1).strip()
    
    # 提取 Caption
    caption_match = re.search(r"\*\s+\*\*Caption\*\*:?\s*(.+?)(?:\n|$)", content)
    if caption_match:
        data["caption"] = caption_match.group(1).strip().strip('"')
    
    # 提取 Concept
    concept_match = re.search(r"\*\s+\*\*Concept\*\*:?\s*(.+?)(?:\n|$)", content)
    if concept_match:
        data["concept"] = concept_match.group(1).strip()

    # 提取 Action (Demo)
    action_match = re.search(r"\*\s+\*\*Action\*\*:?\s*(.+?)(?:\n|$)", content)
    if action_match:
        data["action"] = action_match.group(1).strip()

    # 提取 Target (Demo)
    target_match = re.search(r"\*\s+\*\*Target\*\*:?\s*(.+?)(?:\n|$)", content)
    if target_match:
        data["target"] = target_match.group(1).strip()

    # 提取 Duration (Demo)
    duration_match = re.search(r"\*\s+\*\*Duration\*\*:?\s*(.+?)(?:\n|$)", content)
    if duration_match:
        data["duration"] = duration_match.group(1).strip()

    return data


def parse_structure_map(map_path: Path) -> list:
    """解析 Structure Map，返回 [(section_id, title), ...]"""
    if not map_path.exists():
        return []
    content = map_path.read_text(encoding="utf-8")
    sections = []
    
    # 匹配 ## 模块X：标题 (Sxx_Name)
    section_pattern = r"^##\s+模块.*?\：(.*?)\s*\((S\d+_\w+)\)"
    
    for line in content.split("\n"):
        match = re.match(section_pattern, line)
        if match:
            title = match.group(1).strip()
            section_id = match.group(2)
            sections.append((section_id, title))
    
    return sections


def extract_slide_cues(script_path: Path) -> list:
    """从脚本中提取 (PPT: Sxx) 或 [SLIDE: Sxx] 标记"""
    if not script_path.exists():
        return []
    
    content = script_path.read_text(encoding="utf-8")
    cues = []
    
    # 匹配 (PPT: Sxx_ID) 或 [SLIDE: Sxx_ID]
    # 使用正则表达式提取
    found = re.findall(r"(?:\[SLIDE:\s*|\(PPT:\s*)(S\d+[a-z]?_\S+?)(?:\]|\))", content)
    for sid in found:
        if sid not in cues:
            cues.append(sid)
    
    return cues


def get_tts_assets(section_id: str) -> dict:
    """获取 TTS 相关资产路径"""
    audio_exts = [".mp3", ".wav", ".aac"]
    audio_path = None
    
    for ext in audio_exts:
        path = TTS_DIR / f"{section_id}{ext}"
        if path.exists():
            audio_path = f"tts/{section_id}{ext}"
            break
    
    srt_path = TTS_DIR / f"{section_id}.srt"
    srt_rel = f"tts/{section_id}.srt" if srt_path.exists() else None
    
    return {
        "audio": audio_path,
        "srt": srt_rel,
    }

def find_visual_asset(slide_id: str, section_id: str) -> str:
    """
    智能资产查找逻辑: 
    基于 ID 前缀匹配，不再寻找硬编码文件名。
    """
    assets_dir = PROJECT_ROOT / "02_Visuals" / "assets"
    
    # 搜索范围: 对应章节目录 -> 全局目录
    search_dirs = [section_id, "_Global"]
    
    # 支持的扩展名
    EXTENSIONS = ('.png', '.jpg', '.jpeg', '.mp4', '.mov', '.webp', '.webm')
    
    for d_name in search_dirs:
        dir_path = assets_dir / d_name
        if not dir_path.exists():
            continue
            
        # 获取目录下所有匹配 slide_id 开头的文件
        # 例如 S05_UI_The_Wall -> 匹配 S05_UI_The_Wall.png, S05_UI_The_Wall_src.jpg 等

        for file in dir_path.iterdir():
            # Case insensitive matching
            f_lower = file.name.lower()
            id_lower = slide_id.lower()

            # Standard Sxx_...
            match_standard = f_lower.startswith(f"{id_lower}_") or f_lower == f"{id_lower}.png" or f_lower == f"{id_lower}.mp4"
            
            if match_standard:
                if file.suffix.lower() in EXTENSIONS:
                    # 排除特定前缀 (如果是灰盒逻辑下残余的图，但原则上 ID 匹配优先)
                    # 找到第一个匹配的就作为该 ID 的代表素材
                    return f"visuals/{d_name}/{file.name}"
            
            # 特殊处理：有些 ID 本身不带后缀，如 S05_Jungian_Shadow
            if file.stem == slide_id and file.suffix.lower() in EXTENSIONS:
                return f"visuals/{d_name}/{file.name}"
            
    return None

def build_manifest() -> dict:
    """构建完整的 slides.json"""
    # 解析所有数据源
    slides_db = parse_slide_database(SLIDE_DB_PATH)
    sections = parse_structure_map(STRUCTURE_MAP_PATH)
    
    manifest = {
        "version": "1.1",
        "generated": "",
        "sections": []
    }
    
    for section_id, section_title in sections:
        section_data = {
            "id": section_id,
            "title": section_title,
            "slides": [],
        }
        
        # 获取 TTS 资产
        tts = get_tts_assets(section_id)
        section_data["audio"] = tts["audio"]
        section_data["srt"] = tts["srt"]
        
        # 获取该章节引用的 slides
        script_path = SCRIPTS_DIR / f"{section_id}.md"
        cues = extract_slide_cues(script_path)
        
        # 为每个 cue 生成 slide 数据
        for slide_id in cues:
            if slide_id in slides_db:
                slide_info = slides_db[slide_id].copy()
                slide_info["id"] = slide_id
                
                # 注入布局模板
                stype = slide_info.get("type", "Unknown")
                slide_info["layout"] = LAYOUT_TEMPLATES.get(stype, LAYOUT_TEMPLATES['UI Graphic'])
                
                # 查找物理资产 (图片)
                img_path = find_visual_asset(slide_id, section_id)
                if img_path:
                    slide_info["image"] = img_path
                
                section_data["slides"].append(slide_info)
            else:
                # 未定义的 slide，创建简单占位
                section_data["slides"].append({
                    "id": slide_id,
                    "type": "Placeholder",
                    "text": slide_id,
                    "layout": LAYOUT_TEMPLATES['UI Graphic']
                })
        
        manifest["sections"].append(section_data)
    
    return manifest


def main():
    """主入口"""
    print("🔄 正在深度解析项目数据...")
    
    # 确保输出目录存在
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    manifest = build_manifest()
    
    # 添加生成时间戳
    from datetime import datetime
    manifest["generated"] = datetime.now().isoformat()
    
    # 写入 JSON
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"✅ H5 数据字典已生成: {OUTPUT_PATH}")
    print(f"   - 模块总数: {len(manifest['sections'])}")
    total_slides = sum(len(s['slides']) for s in manifest['sections'])
    print(f"   - Slide 总数: {total_slides}")


if __name__ == "__main__":
    main()
