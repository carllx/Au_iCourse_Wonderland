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
TIMELINE_JSON_PATH = PROJECT_ROOT / "03_Scripts/timeline.json"
OUTPUT_PATH = PROJECT_ROOT / "04_Delivery" / "h5_preview" / "public" / "slides.json"

# ============================================================
# 布局模板映射 (Template Mapping)
# ============================================================

TEMPLATE_MAPPING = {
    'UI Graphic': 'Layout_Content',       # 经典图文 (上标题+左文+右图)
    'UI Composite': 'Layout_Split',       # 左右分屏 (对比/组合)
    'Diagram': 'Layout_Content',          # 图表通常也是图文结构
    'Concept Art': 'Layout_FullBleed',    # 全屏艺术图
    'Motion Graphic': 'Layout_Cinema',    # 全屏视频
    'Video': 'Layout_Cinema',             # 全屏视频
    'Live Demo': 'Layout_Demo',           # 演示专用
    'Stock/Reference': 'Layout_FullBleed',# 参考图全屏
    'Title': 'Layout_Title',              # 标题页
    'Metaphor': 'Layout_FullBleed',       # 隐喻通常是全屏图
    'Photo/Historical': 'Layout_Content', # 历史照片通常配文
    'Photo/Band': 'Layout_FullBleed',     # 乐队通常全屏
    'Photo/Art': 'Layout_FullBleed',      # 艺术作品全屏
    'Chart': 'Layout_Content',            #通过图文展示
    'Task Card': 'Layout_Title',          # 任务卡片类似标题页
    'Animation': 'Layout_Cinema',         # 动画即视频
    'Text/Minimalist': 'Layout_Title',    # 极简文字
    'Diagram/Historical': 'Layout_Split', # 历史图表左右对比
    'Diagram/Comparison': 'Layout_Split', # 对比图左右对比
    'UI/Screenshot': 'Layout_FullBleed',  # 界面截图通常全屏
}

# 默认回退模板
DEFAULT_TEMPLATE = 'Layout_Content'

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
    
    # 提取 Type: \*\*Type\*\*:\s*\[(.*?)\]
    # Note: Regex slightly adjusted to be robust
    type_match = re.search(r"\*\s+\*\*Type\*\*:\s*\[(.*?)\]", content)
    if not type_match:
         # Try with space
         type_match = re.search(r"\*\s+\*\*Type\*\*\s*:\s*\[(.*?)\]", content)

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
    
    # [NEW] 读取持久化时间轴数据
    timeline_data = {} 
    if TIMELINE_JSON_PATH.exists():
        try:
            with open(TIMELINE_JSON_PATH, "r", encoding="utf-8") as f:
                timeline_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Failed to read timeline.json: {e}")

    manifest = {
        "version": "1.4", # Architecture Refactor
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
                
                # 注入模板 (Template) 而不是 Layout Zones
                stype = slide_info.get("type", "Unknown")
                # 模糊匹配逻辑：如果 type 包含 'Graphic'，优先匹配
                # 这里要做简单的 key 查找
                mapped_template = DEFAULT_TEMPLATE
                
                # 精确/模糊匹配策略
                if stype in TEMPLATE_MAPPING:
                    mapped_template = TEMPLATE_MAPPING[stype]
                else:
                    # 尝试前缀匹配 (e.g. "Diagram/Historical" -> "Layout_Split")
                    for k, v in TEMPLATE_MAPPING.items():
                        if k in stype: # 简单的子串匹配
                            mapped_template = v
                            break
                            
                slide_info["template"] = mapped_template
                
                # 查找物理资产 (图片)
                img_path = find_visual_asset(slide_id, section_id)
                if img_path:
                    slide_info["image"] = img_path
                
                # [FIX] 注入保留的时间戳 (From timeline.json)
                # Key is just slide_id now
                if slide_id in timeline_data:
                    slide_info["startTime"] = timeline_data[slide_id]

                section_data["slides"].append(slide_info)
            else:
                # 未定义的 slide，创建简单占位
                placeholder = {
                    "id": slide_id,
                    "type": "Placeholder",
                    "text": slide_id,
                    "template": "Layout_Title" # 占位符默认由 Title 样式承载
                }
                # [FIX] 注入保留的时间戳 (From timeline.json)
                if slide_id in timeline_data:
                    placeholder["startTime"] = timeline_data[slide_id]
                
                section_data["slides"].append(placeholder)
        
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
