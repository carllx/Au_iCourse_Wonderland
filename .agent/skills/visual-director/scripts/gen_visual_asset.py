#!/usr/bin/env python3
"""
Visual Asset Generator (Style Enforced)
Visual Director Skill Component
"""

import argparse
import base64
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置区 (Configuration)
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
YAML_PATH = PROJECT_ROOT / ".agent/standards/visual_system.yaml"
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
    return config

ENV_CONFIG = load_env_config()
API_BASE_URL = ENV_CONFIG["API_BASE_URL"]
API_KEY = ENV_CONFIG["API_KEY"]
MODEL = ENV_CONFIG["API_MODEL"]

# Slide ID 到模块文件夹的映射 (Legacy Map, need automated way ideally)
SLIDE_MODULE_MAP = {
    "S01": "S01_Intro",
    "S02": "S02_Phase1_Purify",
    "S03": "S03_Phase2_Sculpt",
    "S04": "S04_Phase3_Space",
    "S05": "S05_Phase4_Position",
    "S06": "S02_Phase1_Purify", # S06 is Purify
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
    prefix = slide_id.split("_")[0][:3]  # S05
    return SLIDE_MODULE_MAP.get(prefix, "S01_Intro")

def load_visual_system():
    if not YAML_PATH.exists():
        print(f"❌ Visual Constitution not found: {YAML_PATH}")
        sys.exit(1)
    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def parse_slide_database() -> dict:
    if not SLIDE_DATABASE.exists():
        sys.exit(1)
    content = SLIDE_DATABASE.read_text(encoding="utf-8")
    slides = {}
    
    # Match blocks
    pattern = r"## (S\d+[a-z]?_[\w]+).*?\n(.*?)(?=\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    for slide_id, block in matches:
        # Extract Type
        type_match = re.search(r"\*\*Type\*\*:\s*\[(.*?)\]", block)
        slide_type = type_match.group(1) if type_match else "Diagram"
        
        # Extract Prompt
        prompt_match = re.search(r"\*\*AI_Prompt\*\*:\s*`([^`]+)`", block)
        custom_prompt = prompt_match.group(1) if prompt_match else None
        
        # Extract Concept/Visual if prompt missing
        concept_match = re.search(r"\*\*Concept\*\*:\s*(.*)", block)
        visual_match = re.search(r"\*\*Visual\*\*:\s*(.*)", block)
        
        slides[slide_id] = {
            "type": slide_type,
            "prompt": custom_prompt,
            "concept": concept_match.group(1) if concept_match else "",
            "visual": visual_match.group(1) if visual_match else "",
            "module": get_module_folder(slide_id)
        }
    return slides

def construct_prompt(slide_info, visual_config):
    """
    Construct the final prompt using the Visual Constitution
    """
    prompt = ""
    style_config = visual_config.get('style', {})
    
    # 1. Subject (User defined or constructed)
    if slide_info['prompt']:
        prompt = slide_info['prompt']
    else:
        # Fallback: Construct from Visual description
        prompt = f"Subject: {slide_info['visual']}. Concept: {slide_info['concept']}."

    # 2. Inject Type-specific Suffix (Safety Net)
    # Check if prompt already contains style keywords. If not, inject global style.
    
    global_keywords = style_config.get('keywords', "")
    atmosphere = style_config.get('atmosphere', "")
    
    # Determine aspect ratio text (for the model's understanding, though typical API use width/height)
    slide_type = slide_info['type']
    target_dim = "16:9" # Default
    
    # Match type to config
    dim_config = visual_config.get('dimensions', {})
    
    # Map [Concept Art] -> concept_art
    type_key = slide_type.lower().replace(" ", "_").replace("/", "_")
    
    # Fuzzy match logic
    if "diagram" in type_key: type_key = "diagram"
    elif "icon" in type_key: type_key = "icon"
    elif "ui" in type_key: type_key = "ui_slide"
    else: type_key = "concept_art"
    
    type_settings = dim_config.get(type_key, dim_config.get('concept_art'))
    
    # Append Style if not present
    if "bauhaus" not in prompt.lower():
        prompt += f", {global_keywords}, {atmosphere}, {type_settings.get('suffix', '')}"
        
    return prompt, type_settings

def generate_image(prompt: str, width: int, height: int) -> bytes:
    try:
        import requests
        import json
    except ImportError:
        print("❌ pip install requests")
        sys.exit(1)
        
    print(f"🎨 Generating: {prompt[:60]}... [{width}x{height}]")
    
    # Construct REST API URL
    endpoint = f"{API_BASE_URL.rstrip('/')}/models/{MODEL}:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 1,
            "topK": 32,
            "maxOutputTokens": 2048,
        }
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return None
            
        result = response.json()
        
        # Parse standard Gemini response structure for text (wait, this is image gen?)
        # Standard Gemini generates TEXT.
        # But this script claims to generate images ("gemini-3-pro-image").
        # If it's generating images, the response structure is different (or it returns a base64 string in text).
        
        # CRITICAL CHECK: Does "gemini-3-pro-image" imply Imagen via Vertex or Gemini multimodal output?
        # The previous code looked for `part.inline_data`. This implies the model returns raw image bytes.
        # Let's check for inline_data structure.
        
        # Potential Structure:
        # {
        #   "candidates": [
        #     {
        #       "content": {
        #         "parts": [
        #           {
        #             "inlineData": {
        #               "mimeType": "image/png",
        #               "data": "..."
        #             }
        #           }
        #         ]
        #       }
        #     }
        #   ]
        # }
        
        candidates = result.get('candidates', [])
        if not candidates:
            print(f"⚠️ No candidates returned: {result}")
            return None
            
        parts = candidates[0].get('content', {}).get('parts', [])
        for part in parts:
            if 'inlineData' in part:
                b64_data = part['inlineData']['data']
                return base64.b64decode(b64_data)
                
            # Fallback: maybe it returns a URL or text describing the image?
            # If the model is actually a text model being asked to describe an image, this whole thing fails.
            # But the previous code expected `part.inline_data`.
            
        print(f"⚠️ Structure mismatch (No inlineData): {result}")
        return None

    except Exception as e:
        print(f"❌ API Request Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_image(image_data: bytes, slide_id: str, module: str, deploy: bool = False) -> Path:
    module_dir = ASSETS_DIR / module
    module_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%H%M%S")
    asset_path = module_dir / f"{slide_id}_ai_{timestamp}.png"
    asset_path.write_bytes(image_data)
    print(f"✅ Saved: {asset_path.relative_to(PROJECT_ROOT)}")
    
    if deploy:
        final_path = module_dir / f"{slide_id}.png"
        final_path.write_bytes(image_data)
        print(f"🚀 Deployed: {final_path.relative_to(PROJECT_ROOT)}")
        return final_path
    return asset_path

def main():
    parser = argparse.ArgumentParser(description="Visual Director Asset Generator")
    parser.add_argument("slide_id", help="Slide ID")
    parser.add_argument("--deploy", action="store_true", help="Deploy immediately")
    parser.add_argument("--dry-run", action="store_true", help="Show prompt only")
    
    args = parser.parse_args()
    
    # Load
    visual_config = load_visual_system()
    slides = parse_slide_database()
    
    # Find Slide
    target_info = None
    target_id = args.slide_id
    for sid, info in slides.items():
        if args.slide_id.lower() in sid.lower():
            target_info = info
            target_id = sid
            break
            
    if not target_info:
        print(f"❌ Slide {args.slide_id} not found in Database")
        return

    # Construct Prompt & Settings
    prompt, type_settings = construct_prompt(target_info, visual_config)
    width = type_settings.get('width', 1920)
    height = type_settings.get('height', 1080)
    
    if args.dry_run:
        print(f"🔍 [DRY RUN] {target_id}")
        print(f"   Prompt: {prompt}")
        print(f"   Size: {width}x{height}")
        return

    # Execute
    data = generate_image(prompt, width, height)
    if data:
        save_image(data, target_id, target_info['module'], args.deploy)

if __name__ == "__main__":
    main()
