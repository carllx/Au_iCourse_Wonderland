#!/usr/bin/env python3
"""
Generate Video Placeholders - 生成动态占位符并注入 H5
用法: python gen_placeholders.py <Section_ID> [Slide_ID]
"""

import sys
import json
import ffmpeg
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SLIDES_JSON_PATH = PROJECT_ROOT / "04_Delivery/h5_preview/public/slides.json"
VISUALS_DIR = PROJECT_ROOT / "04_Delivery/h5_preview/public/visuals"

def gen_placeholder(slide_id, duration, output_path):
    print(f"🎬 Generating placeholder for {slide_id} ({duration}s)...")
    
    # 确保目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 使用 ffmpeg 生成视频
    # 颜色: 深灰
    # 文字: ID + Duration
    text = f"Slide: {slide_id}\nDuration: {duration:.1f}s\n[VIDEO PLACEHOLDER]"
    
    # 为了速度，只生成 3 秒视频 (H5 会 loop)
    # 真实场景应该生成全长，但这里是 Demo
    real_duration = 3 
    
    try:
        (
            ffmpeg
            .input(f'color=c=0x333333:s=1280x720:d={real_duration}', f='lavfi')
            .drawtext(
                text=text,
                fontsize=64,
                fontcolor='white',
                x='(w-text_w)/2',
                y='(h-text_h)/2',
                # 字体如果不存在可能报错，尝试用 arial 或不指定 (ffmpeg default)
                # macos 通常有 Arial
                fontfile='/System/Library/Fonts/Supplemental/Arial.ttf' 
            )
            .output(str(output_path), vcodec='libx264', pix_fmt='yuv420p', loglevel="error")
            .overwrite_output()
            .run()
        )
        print(f"   ✅ Saved to {output_path}")
        return True
    except ffmpeg.Error as e:
        print(f"   ❌ FFmpeg Error: {e.stderr.decode() if e.stderr else str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_placeholders.py <Section_ID> [Slide_ID]")
        sys.exit(1)
        
    section_id = sys.argv[1]
    target_slide_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not SLIDES_JSON_PATH.exists():
        print("Error: slides.json not found")
        return
        
    with open(SLIDES_JSON_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    # 找到 Section
    target_section = None
    for section in manifest.get('sections', []):
        if section_id in section.get('id', '') or section_id in section.get('title', ''):
             target_section = section
             break
             
    if not target_section:
        print(f"Section {section_id} not found")
        return
        
    slides = target_section.get('slides', [])
    updated_count = 0
    
    for i, slide in enumerate(slides):
        sid = slide.get('id')
        if not sid: continue
        
        # 如果指定了 Slide ID，只处理那一个
        if target_slide_id and sid != target_slide_id:
            continue
            
        start_time = slide.get('startTime')
        if start_time is None:
            # 如果没有时间，无法计算时长
            print(f"   Skip {sid}: No startTime")
            continue
            
        # 计算时长
        next_slide = slides[i+1] if i < len(slides)-1 else None
        end_time = next_slide.get('startTime') if next_slide else start_time + 10 # 默认+10s
        
        # 如果是最后一个，暂无 audio duration，只能估算
        if not end_time: end_time = start_time + 10
            
        duration = end_time - start_time
        
        # 生成 Output Path
        # visuals/S03.../ID.mp4
        # 注意: slides.json 里的 image path 是 relative to public/
        # 我们要写入 absolute path
        rel_dir = Path(slide.get('image', '')).parent
        if str(rel_dir) == '.': 
            rel_dir = Path(f"visuals/{section_id}_placeholder")
            
        output_filename = f"{sid}_placeholder.mp4"
        abs_output_path = VISUALS_DIR / rel_dir.name / output_filename # 简化路径假设
        
        # 修正: 使用 slide existing image folder
        if slide.get('image'):
             existing_rel = Path(slide['image']).parent
             abs_output_path = PROJECT_ROOT / "04_Delivery/h5_preview/public" / existing_rel / output_filename
        else:
             abs_output_path = VISUALS_DIR / section_id / output_filename

        if gen_placeholder(sid, duration, abs_output_path):
            # Update JSON
            # image path relative to public
            # e.g. visuals/S03_Phase2_Sculpt/S08d_Chipmunk_placeholder.mp4
            
            # rel path computation
            public_root = PROJECT_ROOT / "04_Delivery/h5_preview/public"
            rel_path = abs_output_path.relative_to(public_root)
            
            slide['image'] = str(rel_path)
            updated_count += 1
            
    if updated_count > 0:
        print(f"💾 Updated {updated_count} slides in slides.json")
        with open(SLIDES_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
