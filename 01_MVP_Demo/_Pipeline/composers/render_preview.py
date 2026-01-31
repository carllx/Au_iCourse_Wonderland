#!/usr/bin/env python3
"""
章节预览视频生成器 (Section Preview Renderer)
将 TTS 音频、字幕与视觉素材合成为预览视频

使用方法:
    # 生成 S01 的预览视频
    python render_preview.py --section S01_Intro
    
    # 指定输出路径
    python render_preview.py --section S01_Intro --output ./preview.mp4
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# ============================================================
# 配置区 (Configuration)
# ============================================================

# 从 01_MVP_Demo/_Pipeline/composers/ 向上定位项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "03_Scripts"
TTS_DIR = SCRIPTS_DIR / "tts"
VISUALS_DIR = PROJECT_ROOT / "02_Visuals" / "assets"
OUTPUT_DIR = PROJECT_ROOT / "01_MVP_Demo" / "_Media" / "previews"

# FFmpeg 路径
FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"

# 视频参数
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30

# 字体路径 (macOS 系统字体)
FONT_PATH = "/System/Library/Fonts/PingFang.ttc"


def find_section_assets(section_id: str) -> dict:
    """
    根据 Section ID 查找相关资产
    
    Args:
        section_id: 如 "S01_Intro" 或 "S02_Phase1_Purify"
    
    Returns:
        dict: 包含 audio, srt, visuals, script 路径
    """
    assets = {
        "section_id": section_id,
        "audio": None,
        "srt": None,
        "visuals": [],
        "script": None,
    }
    
    # 查找 TTS 音频和字幕 (优先 mp3，回退 wav)
    audio_path = TTS_DIR / f"{section_id}.mp3"
    if not audio_path.exists():
        audio_path = TTS_DIR / f"{section_id}.wav"
    srt_path = TTS_DIR / f"{section_id}.srt"
    
    if audio_path.exists():
        assets["audio"] = audio_path
    else:
        print(f"⚠️  未找到 TTS 音频: {TTS_DIR / section_id}.[mp3|wav]")
    
    if srt_path.exists():
        assets["srt"] = srt_path
    else:
        print(f"⚠️  未找到字幕文件: {srt_path}")
    
    # 查找脚本文件
    script_path = SCRIPTS_DIR / f"{section_id}.md"
    if script_path.exists():
        assets["script"] = script_path
    
    # 查找视觉资产目录
    # 映射 Section ID 到模块目录
    module_dir = VISUALS_DIR / section_id
    if module_dir.exists():
        # 收集所有 Sxx_*.png 文件 (排除 src_, ref_, doc_)
        for f in sorted(module_dir.glob("S*.png")):
            if not f.name.startswith(("src_", "ref_", "doc_")):
                assets["visuals"].append(f)
    
    return assets


def parse_srt(srt_path: Path) -> list:
    """
    解析 SRT 字幕文件
    
    Returns:
        list of dict: [{index, start_time, end_time, text}, ...]
    """
    if not srt_path or not srt_path.exists():
        return []
    
    subtitles = []
    content = srt_path.read_text(encoding="utf-8")
    
    # SRT 格式解析
    pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    for match in matches:
        idx, start, end, text = match
        subtitles.append({
            "index": int(idx),
            "start": start.replace(",", "."),  # FFmpeg 格式
            "end": end.replace(",", "."),
            "text": text.strip().replace("\n", " ")
        })
    
    return subtitles


def get_audio_duration(audio_path: Path) -> float:
    """使用 ffprobe 获取音频时长"""
    if not audio_path or not audio_path.exists():
        return 0.0
    
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"❌ 无法获取音频时长: {e}")
        return 0.0


def generate_title_background(section_id: str, duration: float, output_path: Path) -> Path:
    """
    生成带标题的渐变背景视频（无视觉素材时的回退方案）
    
    使用 FFmpeg lavfi 生成：
    - 深蓝到紫色的渐变背景
    - 居中显示 Section ID 标题
    """
    temp_bg = output_path.parent / f"_bg_{section_id}.mp4"
    
    # 格式化标题：S01_Intro -> S01 · Intro
    title = section_id.replace("_", " · ")
    
    # 使用 FFmpeg lavfi 生成渐变背景 + 标题
    # gradients: 深蓝 (#1a1a2e) 到紫色 (#4a0080)
    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "lavfi",
        "-i", f"color=c=#1a1a2e:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:d={duration:.3f}:r={VIDEO_FPS}",
        "-vf", (
            f"drawtext=fontfile='{FONT_PATH}':"
            f"text='{title}':"
            f"fontsize=72:fontcolor=white:"
            f"x=(w-text_w)/2:y=(h-text_h)/2,"
            f"drawtext=fontfile='{FONT_PATH}':"
            f"text='🎧 数字音频编辑 · Audition':"
            f"fontsize=36:fontcolor=#888888:"
            f"x=(w-text_w)/2:y=h-100"
        ),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        str(temp_bg)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 生成背景失败: {result.stderr}")
            return None
        return temp_bg
    except Exception as e:
        print(f"❌ 生成背景失败: {e}")
        return None


def render_preview(assets: dict, output_path: Path, fast_mode: bool = False) -> bool:
    """
    使用 FFmpeg 生成预览视频
    
    策略:
    1. 如果无视觉素材: 生成带标题的渐变背景
    2. 如果只有一张图片: 循环显示整个音频时长
    3. 如果有多张图片: 均匀分配时长
    4. 添加字幕 (如有 SRT)
    """
    if not assets["audio"]:
        print("❌ 无法生成预览: 缺少 TTS 音频")
        return False
    
    preset = "ultrafast" if fast_mode else "medium"
    use_generated_bg = False
    temp_bg_path = None
    
    duration = get_audio_duration(assets["audio"])
    if duration <= 0:
        print("❌ 无法获取音频时长")
        return False
    
    print(f"📊 音频时长: {duration:.2f}s")
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 如果无视觉素材，生成标题背景
    if not assets["visuals"]:
        print(f"⚠️  无视觉素材，生成标题背景...")
        temp_bg_path = generate_title_background(assets["section_id"], duration, output_path)
        if not temp_bg_path:
            return False
        use_generated_bg = True
    else:
        print(f"🖼️  视觉素材: {len(assets['visuals'])} 张")
    
    # 构建 FFmpeg 命令
    if use_generated_bg:
        # 已生成背景视频模式: 合并音频
        cmd = [
            FFMPEG_PATH, "-y",
            "-i", str(temp_bg_path),
            "-i", str(assets["audio"]),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_path)
        ]
    elif len(assets["visuals"]) == 1:
        # 单图模式: 循环显示
        cmd = [
            FFMPEG_PATH, "-y",
            "-loop", "1",
            "-i", str(assets["visuals"][0]),
            "-i", str(assets["audio"]),
            "-c:v", "libx264",
            "-preset", preset,
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-shortest",
            str(output_path)
        ]
    else:
        # 多图模式: 使用 concat demuxer
        # 计算每张图片的时长
        per_image_duration = duration / len(assets["visuals"])
        
        # 创建临时 concat 文件
        concat_file = output_path.parent / f"_concat_{assets['section_id']}.txt"
        with open(concat_file, "w") as f:
            for img in assets["visuals"]:
                f.write(f"file '{img}'\n")
                f.write(f"duration {per_image_duration:.3f}\n")
            # 最后一张需要再写一次 (concat 要求)
            f.write(f"file '{assets['visuals'][-1]}'\n")
        
        cmd = [
            FFMPEG_PATH, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-i", str(assets["audio"]),
            "-c:v", "libx264",
            "-preset", preset,
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-shortest",
            str(output_path)
        ]
    
    # 如果有字幕，添加字幕滤镜
    if assets["srt"] and not use_generated_bg:
        # 在 vf 中添加 subtitles（仅非生成背景模式）
        for i, arg in enumerate(cmd):
            if arg == "-vf":
                cmd[i+1] = cmd[i+1] + f",subtitles='{assets['srt']}':force_style='FontSize=24,Alignment=2'"
                break
    elif assets["srt"] and use_generated_bg:
        # 生成背景模式需要重新编码以添加字幕
        final_output = output_path
        temp_nosub = output_path.parent / f"_nosub_{assets['section_id']}.mp4"
        cmd[-1] = str(temp_nosub)
        
        # 先生成无字幕版本，稍后添加字幕
        print(f"🎬 正在生成预览视频 (将添加字幕)...")
    
    if not (assets["srt"] and use_generated_bg):
        print(f"🎬 正在生成预览视频...")
    print(f"   输出: {output_path}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ FFmpeg 错误:\n{result.stderr}")
            return False
        
        # 如果是生成背景模式且有字幕，添加字幕
        if assets["srt"] and use_generated_bg:
            temp_nosub = output_path.parent / f"_nosub_{assets['section_id']}.mp4"
            subtitle_cmd = [
                FFMPEG_PATH, "-y",
                "-i", str(temp_nosub),
                "-vf", f"subtitles='{assets['srt']}':force_style='FontSize=28,Alignment=2,PrimaryColour=&Hffffff&'",
                "-c:v", "libx264",
                "-preset", preset,
                "-c:a", "copy",
                str(output_path)
            ]
            print(f"   添加字幕...")
            sub_result = subprocess.run(subtitle_cmd, capture_output=True, text=True)
            if sub_result.returncode != 0:
                print(f"⚠️  字幕添加失败，使用无字幕版本: {sub_result.stderr[:200]}")
                temp_nosub.rename(output_path)
            else:
                temp_nosub.unlink()
        
        # 清理临时文件
        if use_generated_bg and temp_bg_path and temp_bg_path.exists():
            temp_bg_path.unlink()
        
        if not use_generated_bg and len(assets["visuals"]) > 1:
            concat_file = output_path.parent / f"_concat_{assets['section_id']}.txt"
            if concat_file.exists():
                concat_file.unlink()
        
        print(f"✅ 预览视频生成成功: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="章节预览视频生成器 - 合成 TTS + 视觉素材",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--section", "-s",
        type=str,
        required=False,
        help="Section ID (如 S01_Intro, S02_Phase1_Purify)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="输出路径 (默认: 01_MVP_Demo/_Media/previews/preview_Sxx.mp4)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出可用的 Section 和资产"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="批量处理所有 TTS 文件"
    )
    
    parser.add_argument(
        "--fast", "-f",
        action="store_true",
        help="使用快速编码 (ultrafast preset)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("📋 可用的 TTS 文件:")
        if TTS_DIR.exists():
            for f in sorted(TTS_DIR.glob("*.wav")):
                srt = TTS_DIR / f.name.replace(".wav", ".srt")
                srt_status = "✅" if srt.exists() else "❌"
                print(f"   {f.stem} (SRT: {srt_status})")
        else:
            print(f"   (目录不存在: {TTS_DIR})")
        return
    
    # 批量处理模式
    if args.all:
        if not TTS_DIR.exists():
            print(f"❌ TTS 目录不存在: {TTS_DIR}")
            sys.exit(1)
        
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # 查找所有 TTS 音频文件 (优先 mp3)
        sections = []
        for f in sorted(TTS_DIR.glob("*.mp3")):
            sections.append(f.stem)
        if not sections:
            for f in sorted(TTS_DIR.glob("*.wav")):
                sections.append(f.stem)
        
        print(f"🎯 找到 {len(sections)} 个章节待处理")
        success_count = 0
        
        for section_id in sections:
            print(f"\n{'='*50}")
            print(f"📹 处理: {section_id}")
            print(f"{'='*50}")
            
            assets = find_section_assets(section_id)
            output_path = OUTPUT_DIR / f"preview_{section_id}.mp4"
            
            if render_preview(assets, output_path, fast_mode=args.fast):
                success_count += 1
        
        print(f"\n{'='*50}")
        print(f"✅ 完成: {success_count}/{len(sections)} 个视频生成成功")
        print(f"📁 输出目录: {OUTPUT_DIR}")
        
        if success_count < len(sections):
            sys.exit(1)
        return
    
    # 单个章节模式
    if not args.section:
        print("❌ 请指定 --section 或使用 --all")
        parser.print_help()
        sys.exit(1)
    
    # 查找资产
    assets = find_section_assets(args.section)
    
    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"preview_{args.section}.mp4"
    
    # 生成预览
    success = render_preview(assets, output_path, fast_mode=args.fast)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
