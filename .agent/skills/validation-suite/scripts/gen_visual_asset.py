#!/usr/bin/env python3
"""
视觉资产生成器 (Visual Asset Generator)
使用 AI 根据 Slide_Database.md 中的 Prompt 生成图片

使用方法:
    # 生成单个 Slide
    python gen_visual_asset.py S06_Ghost_Math
    
    # 生成并自动覆盖灰盒
    python gen_visual_asset.py S06_Ghost_Math --deploy
    
    # 自定义 Prompt 生成
    python gen_visual_asset.py S06_Ghost_Math --prompt "A ghost bird in void"
    
    # 批量生成所有有 AI_Prompt 的 Slide
    python gen_visual_asset.py --all
"""

import argparse
import base64
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置区 (Configuration)
# ============================================================

# 项目路径 (从 .agent/skills/validation-suite/scripts/ 向上 4 级)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
SLIDE_DATABASE = PROJECT_ROOT / "02_Visuals" / "Slide_Database.md"
ASSETS_DIR = PROJECT_ROOT / "02_Visuals" / "assets"

def load_env_config():
    """从 .env 文件加载配置"""
    env_file = PROJECT_ROOT / ".env"
    config = {
        "API_BASE_URL": "http://127.0.0.1:8045/v1",
        "API_KEY": "",
        "API_MODEL": "gemini-3-pro-image",
    }
    
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    else:
        print(f"⚠️  未找到 .env 文件,请创建: {env_file}")
        print("   示例内容:")
        print("   API_BASE_URL=http://127.0.0.1:8045/v1")
        print("   API_KEY=your-api-key-here")
        print("   API_MODEL=gemini-3-pro-image")
    
    return config

# 加载配置
ENV_CONFIG = load_env_config()
API_BASE_URL = ENV_CONFIG["API_BASE_URL"]
API_KEY = ENV_CONFIG["API_KEY"]
MODEL = ENV_CONFIG["API_MODEL"]
DEFAULT_SIZE = "1280x720"  # 16:9 适合 PPT

# Slide ID 到模块文件夹的映射
SLIDE_MODULE_MAP = {
    "S01": "S01_Intro",
    "S02": "S02_Phase1_Purify",
    "S03": "S03_Phase2_Sculpt",
    "S04": "S04_Phase3_Space",
    "S05": "S02_Phase1_Purify",  # S05, S06, S07 属于 Phase1
    "S06": "S02_Phase1_Purify",
    "S07": "S02_Phase1_Purify",
    "S08": "S03_Phase2_Sculpt",
    "S09": "S03_Phase2_Sculpt",
    "S10": "S04_Phase3_Space",
    "S11": "S04_Phase3_Space",
    "S12": "S04_Phase3_Space",
    "S13": "S04_Phase3_Space",
    "S14": "S05_Phase4_Position",
    "S15": "S05_Phase4_Position",
    "S16": "S06_Summary",
    "S17": "S06_Summary",
    "S18": "S01_Intro",
    "S19": "S06_Summary",
}


def get_module_folder(slide_id: str) -> str:
    """根据 Slide ID 获取对应的模块文件夹"""
    prefix = slide_id.split("_")[0][:3]  # 提取 S05, S06 等
    return SLIDE_MODULE_MAP.get(prefix, "S01_Intro")


def parse_slide_database() -> dict:
    """解析 Slide_Database.md,提取所有 Slide 的 AI_Prompt"""
    if not SLIDE_DATABASE.exists():
        print(f"❌ 找不到 Slide_Database: {SLIDE_DATABASE}")
        sys.exit(1)
    
    content = SLIDE_DATABASE.read_text(encoding="utf-8")
    slides = {}
    
    # 匹配每个 Slide 块
    pattern = r"## (S\d+[a-z]?_[\w]+).*?\n(.*?)(?=\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    for slide_id, block in matches:
        # 提取 AI_Prompt
        prompt_match = re.search(r"\*\*AI_Prompt\*\*:\s*`([^`]+)`", block)
        if prompt_match:
            slides[slide_id] = {
                "prompt": prompt_match.group(1),
                "module": get_module_folder(slide_id)
            }
    
    return slides


def generate_image(prompt: str, size: str = DEFAULT_SIZE) -> bytes:
    """调用 API 生成图片 (使用 google-generativeai 库)"""
    try:
        import google.generativeai as genai
    except ImportError:
        print("❌ 需要安装 google-generativeai 库: pip install google-generativeai")
        sys.exit(1)
    
    # 配置 Gemini API (使用本地代理)
    # 从 API_BASE_URL 提取 endpoint (去掉 /v1 后缀)
    endpoint = API_BASE_URL.replace("/v1", "")
    genai.configure(
        api_key=API_KEY,
        transport='rest',
        client_options={'api_endpoint': endpoint}
    )
    
    print(f"🎨 正在生成图片...")
    print(f"   Model: {MODEL}")
    print(f"   Prompt: {prompt[:80]}...")
    
    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        
        # 检查响应中是否有图片
        if response.parts:
            for part in response.parts:
                # 如果有图片数据
                if hasattr(part, 'inline_data') and part.inline_data:
                    mime_type = part.inline_data.mime_type
                    data = part.inline_data.data
                    print(f"   ✅ 收到图片: {mime_type}")
                    return data
                # 如果返回的是文本 (可能包含 base64)
                elif hasattr(part, 'text') and part.text:
                    text = part.text
                    # 检查是否是 base64 图片数据
                    if text.startswith("data:image"):
                        base64_data = text.split(",")[1]
                        return base64.b64decode(base64_data)
                    elif len(text) > 1000 and re.match(r'^[A-Za-z0-9+/=]+$', text[:100]):
                        # 可能是纯 base64 数据
                        return base64.b64decode(text)
                    else:
                        print(f"⚠️  API 返回文本: {text[:200]}...")
        
        # 尝试直接访问 response.text
        if hasattr(response, 'text') and response.text:
            print(f"⚠️  API 返回文本响应: {response.text[:200]}...")
        
        return None
        
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return None


def save_image(image_data: bytes, slide_id: str, module: str, deploy: bool = False) -> Path:
    """保存图片到指定位置"""
    module_dir = ASSETS_DIR / module
    module_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%H%M%S")
    src_filename = f"src_{slide_id.lower()}_ai_{timestamp}.png"
    src_path = module_dir / src_filename
    
    # 保存原图
    src_path.write_bytes(image_data)
    print(f"✅ 原图已保存: {src_path.relative_to(PROJECT_ROOT)}")
    
    if deploy:
        # 覆盖灰盒
        final_filename = f"{slide_id}.png"
        final_path = module_dir / final_filename
        final_path.write_bytes(image_data)
        print(f"✅ 已覆盖灰盒: {final_path.relative_to(PROJECT_ROOT)}")
        return final_path
    
    return src_path


def generate_single(slide_id: str, prompt: str = None, deploy: bool = False, size: str = DEFAULT_SIZE):
    """生成单个 Slide 的图片"""
    slides = parse_slide_database()
    
    # 查找 Slide
    slide_info = None
    for sid, info in slides.items():
        if slide_id.lower() in sid.lower():
            slide_info = info
            slide_id = sid  # 使用完整的 ID
            break
    
    if prompt:
        # 使用自定义 Prompt
        module = get_module_folder(slide_id)
    elif slide_info:
        prompt = slide_info["prompt"]
        module = slide_info["module"]
    else:
        print(f"❌ 找不到 Slide '{slide_id}' 或其 AI_Prompt")
        print(f"   可用的 Slide: {list(slides.keys())}")
        return
    
    # 生成图片
    image_data = generate_image(prompt, size)
    if image_data:
        save_image(image_data, slide_id, module, deploy)


def generate_all(deploy: bool = False, size: str = DEFAULT_SIZE):
    """批量生成所有有 AI_Prompt 的 Slide"""
    slides = parse_slide_database()
    
    if not slides:
        print("❌ 没有找到任何含 AI_Prompt 的 Slide")
        return
    
    print(f"📦 找到 {len(slides)} 个待生成的 Slide:")
    for sid in slides:
        print(f"   - {sid}")
    
    confirm = input("\n是否继续? [y/N]: ")
    if confirm.lower() != "y":
        print("已取消")
        return
    
    for i, (slide_id, info) in enumerate(slides.items(), 1):
        print(f"\n[{i}/{len(slides)}] 生成 {slide_id}...")
        image_data = generate_image(info["prompt"], size)
        if image_data:
            save_image(image_data, slide_id, info["module"], deploy)


def main():
    parser = argparse.ArgumentParser(
        description="视觉资产生成器 - 使用 AI 生成 PPT 图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python gen_visual_asset.py S06_Ghost_Math           # 生成单个
  python gen_visual_asset.py S06 --deploy             # 生成并覆盖灰盒
  python gen_visual_asset.py S06 --prompt "A bird"    # 自定义 Prompt
  python gen_visual_asset.py --all                    # 批量生成
  python gen_visual_asset.py --list                   # 列出所有可生成的 Slide
        """
    )
    
    parser.add_argument("slide_id", nargs="?", help="Slide ID (如 S06_Ghost_Math 或 S06)")
    parser.add_argument("--all", action="store_true", help="生成所有有 AI_Prompt 的 Slide")
    parser.add_argument("--list", action="store_true", help="列出所有可生成的 Slide")
    parser.add_argument("--deploy", action="store_true", help="生成后自动覆盖灰盒")
    parser.add_argument("--prompt", type=str, help="使用自定义 Prompt")
    parser.add_argument("--size", type=str, default=DEFAULT_SIZE, 
                        help=f"图片尺寸 (默认: {DEFAULT_SIZE})")
    
    args = parser.parse_args()
    
    if args.list:
        slides = parse_slide_database()
        print(f"📋 可生成的 Slide ({len(slides)} 个):\n")
        for sid, info in slides.items():
            print(f"  {sid}")
            print(f"    Module: {info['module']}")
            print(f"    Prompt: {info['prompt'][:60]}...")
            print()
        return
    
    if args.all:
        generate_all(deploy=args.deploy, size=args.size)
    elif args.slide_id:
        generate_single(args.slide_id, prompt=args.prompt, deploy=args.deploy, size=args.size)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
