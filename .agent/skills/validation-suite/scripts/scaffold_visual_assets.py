#!/usr/bin/env python3
"""
视觉资产灰盒生成器 v2 (Layout Greybox Generator)
生成带有布局框架的低保真占位图

功能:
- 解析 Slide_Database.md 中的 Type, Text, Sub, List 字段
- 根据 Type 选择布局模板
- 绘制虚线框标注文字/图像区域
- 输出 1920x1080 PNG 占位图

使用方法:
    # 生成所有缺失的灰盒
    python scaffold_visual_assets.py
    
    # 强制重新生成指定 Slide
    python scaffold_visual_assets.py --force S01_Title S02_BadCase
"""

import os
import re
import argparse
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Optional, Tuple

# ============================================================
# 配置区 (Configuration)
# ============================================================

# 尺寸
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
MARGIN = 60
PADDING = 30

# 颜色 (RGB)
BG_COLORS = {
    'Motion Graphic': (30, 30, 60),
    'UI Graphic': (30, 50, 40),
    'UI Composite': (30, 50, 60),
    'Diagram': (50, 50, 30),
    'Concept Art': (50, 30, 60),
    'Stock/Reference': (50, 40, 30),
    'Task Card': (40, 40, 40),
    'Unknown': (25, 25, 25)
}

ZONE_COLOR = (120, 120, 120)       # 虚线框颜色
TITLE_COLOR = (255, 255, 255)      # 标题文字
TEXT_COLOR = (200, 200, 200)       # 普通文字
LABEL_COLOR = (100, 100, 100)      # 区域标签

# 字体路径 (macOS)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FALLBACK_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

# ============================================================
# 布局模板 (Layout Templates)
# ============================================================

def get_layout_template(slide_type: str) -> Dict:
    """
    根据 Slide Type 返回布局模板
    每个模板定义区域的位置 (相对坐标 0-1)
    """
    templates = {
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
        }
    }
    return templates.get(slide_type, templates['UI Graphic'])


# ============================================================
# 解析器 (Parser)
# ============================================================

def parse_slide_database(db_path: str) -> List[Dict]:
    """
    解析 Slide_Database.md，提取所有 Slide 定义
    """
    slides = []
    current_slide = None
    in_list = False
    list_items = []
    
    with open(db_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            
            # 匹配 Slide Header: ## S01_Title
            header_match = re.match(r'^##\s+(S[a-zA-Z0-9_]+)', stripped)
            if header_match:
                # 保存上一个 Slide
                if current_slide:
                    if list_items:
                        current_slide['list'] = list_items
                    slides.append(current_slide)
                    list_items = []
                
                current_slide = {
                    'id': header_match.group(1),
                    'type': 'Unknown',
                    'text': '',
                    'sub': '',
                    'list': [],
                    'visual': '',
                    'caption': ''
                }
                in_list = False
                continue
            
            if not current_slide:
                continue
            
            # 匹配字段
            # Type
            type_match = re.search(r'\*\s+\*\*Type\*\*:\s+\[(.*?)\]', stripped)
            if type_match:
                current_slide['type'] = type_match.group(1)
                in_list = False
                continue
            
            # Text
            text_match = re.search(r'\*\s+\*\*Text\*\*:\s*(.+)', stripped)
            if text_match:
                current_slide['text'] = text_match.group(1).strip()
                in_list = False
                continue
            
            # Sub
            sub_match = re.search(r'\*\s+\*\*Sub\*\*:\s*(.+)', stripped)
            if sub_match:
                current_slide['sub'] = sub_match.group(1).strip()
                in_list = False
                continue
            
            # Caption
            caption_match = re.search(r'\*\s+\*\*Caption\*\*:\s*(.+)', stripped)
            if caption_match:
                current_slide['caption'] = caption_match.group(1).strip().strip('"\'')
                in_list = False
                continue
            
            # Visual (单行描述)
            visual_match = re.search(r'\*\s+\*\*Visual\*\*:\s*(.+)', stripped)
            if visual_match:
                current_slide['visual'] = visual_match.group(1).strip()
                in_list = False
                continue
            
            # List 开始
            if re.search(r'\*\s+\*\*List\*\*:', stripped):
                in_list = True
                list_items = []
                continue
            
            # List 项目
            if in_list:
                item_match = re.match(r'\s+\*\s+(.+)', line)  # 使用原始 line 保留缩进
                if item_match:
                    # 清理 markdown 格式
                    item_text = item_match.group(1).strip()
                    item_text = re.sub(r'\*\*(.+?)\*\*', r'\1', item_text)  # 移除加粗
                    list_items.append(item_text)
                elif stripped and not stripped.startswith('*'):
                    in_list = False
        
        # 保存最后一个 Slide
        if current_slide:
            if list_items:
                current_slide['list'] = list_items
            slides.append(current_slide)
    
    return slides


def get_structure_map(base_dir: str) -> Dict[str, str]:
    """
    解析 00_Structure_Map.md 获取 Slide -> Module 映射
    """
    map_path = os.path.join(base_dir, "03_Scripts", "00_Structure_Map.md")
    slide_to_module = {}
    current_module = "_Global"
    
    if not os.path.exists(map_path):
        return slide_to_module
    
    with open(map_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 匹配模块头: ## ... (S01_Intro)
            mod_match = re.search(r'^##\s+.*?\((S\d+_[a-zA-Z0-9_]+)\)', line)
            if mod_match:
                current_module = mod_match.group(1)
            
            # 匹配 Slide 引用
            slides = re.findall(r'\[SLIDE:\s*(S[a-zA-Z0-9_]+)\]', line)
            for sid in slides:
                if sid not in slide_to_module:
                    slide_to_module[sid] = current_module
    
    return slide_to_module


# ============================================================
# 渲染器 (Renderer)
# ============================================================

def draw_dashed_rect(draw: ImageDraw.ImageDraw, 
                     x1: int, y1: int, x2: int, y2: int,
                     color: Tuple[int, int, int], 
                     dash_length: int = 10, gap_length: int = 5):
    """绘制虚线矩形"""
    def dashed_line(sx, sy, ex, ey):
        length = ((ex - sx) ** 2 + (ey - sy) ** 2) ** 0.5
        dashes = int(length / (dash_length + gap_length))
        for i in range(dashes):
            start = i * (dash_length + gap_length) / length
            end = start + dash_length / length
            if end > 1:
                end = 1
            px1 = sx + (ex - sx) * start
            py1 = sy + (ey - sy) * start
            px2 = sx + (ex - sx) * end
            py2 = sy + (ey - sy) * end
            draw.line([(px1, py1), (px2, py2)], fill=color, width=2)
    
    # 四边
    dashed_line(x1, y1, x2, y1)  # 上
    dashed_line(x2, y1, x2, y2)  # 右
    dashed_line(x2, y2, x1, y2)  # 下
    dashed_line(x1, y2, x1, y1)  # 左


def render_greybox(slide: Dict, output_path: str, fonts: Dict):
    """
    渲染单个 Slide 的灰盒图
    """
    slide_type = slide.get('type', 'Unknown')
    template = get_layout_template(slide_type)
    
    # 创建画布
    bg_color = BG_COLORS.get(slide_type, BG_COLORS['Unknown'])
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # 绘制布局区域
    for zone in template['zones']:
        x1 = int(zone['x'] * CANVAS_WIDTH)
        y1 = int(zone['y'] * CANVAS_HEIGHT)
        x2 = int((zone['x'] + zone['w']) * CANVAS_WIDTH)
        y2 = int((zone['y'] + zone['h']) * CANVAS_HEIGHT)
        
        # 虚线框
        draw_dashed_rect(draw, x1, y1, x2, y2, ZONE_COLOR)
        
        # 区域标签 (左上角)
        label = zone['name']
        draw.text((x1 + 10, y1 + 5), label, fill=LABEL_COLOR, font=fonts['label'])
        
        # 填充内容
        zone_name_lower = zone['name'].lower()
        content_y = y1 + 35
        
        if 'title' in zone_name_lower and slide.get('text'):
            # 绘制标题文字
            text = slide['text']
            if len(text) > 30:
                text = text[:30] + "..."
            draw.text((x1 + 20, y1 + 40), text, fill=TITLE_COLOR, font=fonts['title'])
            
            # 副标题
            if slide.get('sub'):
                sub = slide['sub']
                if len(sub) > 50:
                    sub = sub[:50] + "..."
                draw.text((x1 + 20, y1 + 90), sub, fill=TEXT_COLOR, font=fonts['body'])
        
        elif 'list' in zone_name_lower and slide.get('list'):
            # 绘制列表
            items = slide['list'][:5]  # 最多显示 5 项
            for i, item in enumerate(items):
                if len(item) > 40:
                    item = item[:40] + "..."
                bullet = f"• {item}"
                draw.text((x1 + 20, content_y + i * 45), bullet, fill=TEXT_COLOR, font=fonts['body'])
        
        elif 'caption' in zone_name_lower and slide.get('caption'):
            caption = slide['caption']
            if len(caption) > 60:
                caption = caption[:60] + "..."
            draw.text((x1 + 20, y1 + 20), f'"{caption}"', fill=TEXT_COLOR, font=fonts['body'])
        
        elif 'visual' in zone_name_lower or 'image' in zone_name_lower or 'diagram' in zone_name_lower:
            # 绘制图像占位
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            # 对角线表示图像区
            draw.line([(x1, y1), (x2, y2)], fill=ZONE_COLOR, width=1)
            draw.line([(x2, y1), (x1, y2)], fill=ZONE_COLOR, width=1)
            # 图像描述
            if slide.get('visual'):
                desc = slide['visual'][:50] + "..." if len(slide.get('visual', '')) > 50 else slide.get('visual', '')
                draw.text((x1 + 20, y2 - 40), desc, fill=LABEL_COLOR, font=fonts['label'])
    
    # 底部信息栏
    info_y = CANVAS_HEIGHT - 45
    draw.rectangle([(0, info_y - 10), (CANVAS_WIDTH, CANVAS_HEIGHT)], fill=(20, 20, 20))
    info_text = f"ID: {slide['id']}  |  Type: [{slide_type}]  |  LAYOUT GREYBOX v2"
    draw.text((MARGIN, info_y), info_text, fill=(100, 100, 100), font=fonts['label'])
    
    # 保存
    img.save(output_path, 'PNG')


def load_fonts() -> Dict:
    """加载字体"""
    fonts = {}
    try:
        fonts['title'] = ImageFont.truetype(FONT_PATH, 48)
        fonts['body'] = ImageFont.truetype(FONT_PATH, 32)
        fonts['label'] = ImageFont.truetype(FONT_PATH, 24)
    except OSError:
        try:
            fonts['title'] = ImageFont.truetype(FALLBACK_FONT_PATH, 48)
            fonts['body'] = ImageFont.truetype(FALLBACK_FONT_PATH, 32)
            fonts['label'] = ImageFont.truetype(FALLBACK_FONT_PATH, 24)
        except OSError:
            print("⚠️  无法加载系统字体，使用默认字体")
            fonts['title'] = ImageFont.load_default()
            fonts['body'] = ImageFont.load_default()
            fonts['label'] = ImageFont.load_default()
    return fonts


# ============================================================
# 主程序 (Main)
# ============================================================

def generate_greyboxes(base_dir: str, force_ids: List[str] = None):
    """
    生成灰盒占位图
    
    Args:
        base_dir: 项目根目录
        force_ids: 强制重新生成的 Slide IDs
    """
    db_path = os.path.join(base_dir, "02_Visuals", "Slide_Database.md")
    assets_dir = os.path.join(base_dir, "02_Visuals", "assets")
    
    if not os.path.exists(db_path):
        print(f"❌ 找不到 Slide_Database.md: {db_path}")
        return
    
    # 解析数据
    slides = parse_slide_database(db_path)
    slide_to_module = get_structure_map(base_dir)
    
    print(f"📋 找到 {len(slides)} 个 Slide 定义")
    
    # 加载字体
    fonts = load_fonts()
    
    # 生成灰盒
    generated = 0
    skipped = 0
    
    for slide in slides:
        sid = slide['id']
        module = slide_to_module.get(sid, "_Global")
        
        # 确定模块目录
        # 如果模块名匹配 Section 模式，使用它
        if module.startswith('S') and '_' in module:
            dest_dir = os.path.join(assets_dir, module)
        else:
            dest_dir = os.path.join(assets_dir, "_Global")
        
        os.makedirs(dest_dir, exist_ok=True)
        
        output_path = os.path.join(dest_dir, f"{sid}.png")
        
        # 检查是否需要生成
        if os.path.exists(output_path) and not (force_ids and sid in force_ids):
            skipped += 1
            continue
        
        # 渲染
        render_greybox(slide, output_path, fonts)
        print(f"✅ 生成: {module}/{sid}.png")
        generated += 1
    
    print(f"\n📊 完成: 生成 {generated}, 跳过 {skipped} (已存在)")


def main():
    parser = argparse.ArgumentParser(
        description="Layout Greybox 生成器 - 带布局框架的低保真占位图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        '--force', '-f',
        nargs='*',
        default=None,
        help="强制重新生成指定的 Slide IDs (如 S01_Title S02_BadCase)"
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help="强制重新生成所有灰盒"
    )
    
    args = parser.parse_args()
    
    # 定位项目根目录
    # 从 .agent/skills/validation-suite/scripts/ 向上 4 层
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    
    force_ids = None
    if args.all:
        # 加载所有 Slide IDs
        db_path = os.path.join(base_dir, "02_Visuals", "Slide_Database.md")
        slides = parse_slide_database(db_path)
        force_ids = [s['id'] for s in slides]
    elif args.force:
        force_ids = args.force
    
    generate_greyboxes(base_dir, force_ids)


if __name__ == "__main__":
    main()
