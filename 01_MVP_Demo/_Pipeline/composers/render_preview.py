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
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_FPS = 30


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
    
    # 查找 TTS 音频和字幕
    audio_path = TTS_DIR / f"{section_id}.wav"
    srt_path = TTS_DIR / f"{section_id}.srt"
    
    if audio_path.exists():
        assets["audio"] = audio_path
    else:
        print(f"⚠️  未找到 TTS 音频: {audio_path}")
    
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


def render_preview(assets: dict, output_path: Path) -> bool:
    """
    使用 FFmpeg 生成预览视频
    
    策略:
    1. 如果只有一张图片: 循环显示整个音频时长
    2. 如果有多张图片: 均匀分配时长
    3. 添加字幕 (如有 SRT)
    """
    if not assets["audio"]:
        print("❌ 无法生成预览: 缺少 TTS 音频")
        return False
    
    if not assets["visuals"]:
        print("❌ 无法生成预览: 缺少视觉素材")
        return False
    
    duration = get_audio_duration(assets["audio"])
    if duration <= 0:
        print("❌ 无法获取音频时长")
        return False
    
    print(f"📊 音频时长: {duration:.2f}s")
    print(f"🖼️  视觉素材: {len(assets['visuals'])} 张")
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 构建 FFmpeg 命令
    if len(assets["visuals"]) == 1:
        # 单图模式: 循环显示
        cmd = [
            FFMPEG_PATH, "-y",
            "-loop", "1",
            "-i", str(assets["visuals"][0]),
            "-i", str(assets["audio"]),
            "-c:v", "libx264",
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
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-shortest",
            str(output_path)
        ]
    
    # 如果有字幕，添加字幕滤镜
    if assets["srt"]:
        # 在 vf 中添加 subtitles
        for i, arg in enumerate(cmd):
            if arg == "-vf":
                cmd[i+1] = cmd[i+1] + f",subtitles='{assets['srt']}':force_style='FontSize=24,Alignment=2'"
                break
    
    print(f"🎬 正在生成预览视频...")
    print(f"   输出: {output_path}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ FFmpeg 错误:\n{result.stderr}")
            return False
        
        # 清理临时文件
        if len(assets["visuals"]) > 1:
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
        required=True,
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
    
    # 查找资产
    assets = find_section_assets(args.section)
    
    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = OUTPUT_DIR / f"preview_{args.section}.mp4"
    
    # 生成预览
    success = render_preview(assets, output_path)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
