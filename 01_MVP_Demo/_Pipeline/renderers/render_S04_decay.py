"""
S04 衰减视频渲染器
----------------
可视化 S04 虚空 IR 的衰减。
输入: _Library/S04_Space/asset_S04_void_ir.wav
输出: _Library/S04_Space/asset_S04_void_visual.mp4
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from scipy.io import wavfile
import os
import sys
import subprocess

# --- Path Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../")) # renderers -> _Pipeline -> 01_MVP_Demo -> ROOT
CONFIG_DIR = os.path.join(PROJECT_ROOT, ".agent/skills/lab-factory/config")

sys.path.append(CONFIG_DIR)
try:
    from Visual_System_Config import VisualTheme, Palette, MetricTranslator, CURRENT_THEME, FONT_REGULAR, FONT_MEDIUM
except ImportError:
    print(f"严重警告: 在 {CONFIG_DIR} 未找到 Visual_System_Config")

# --- Helpers ---
def calc_envelope(t, decay_time=2.5):
    """重建理论指数衰减包络。"""
    alpha = -np.log(0.001) / decay_time
    return np.exp(-t * alpha)

def render_decay_video(t, audio, envelope, output_video_path, input_audio_path, output_cover_path):
    """渲染霓虹风格的 DAW 动画。"""
    
    # 1. 应用主题
    plt.rcParams.update(CURRENT_THEME)
    
    # 2. 图表设置
    dpi = 120
    fig, ax = plt.subplots(figsize=(12, 6), dpi=dpi)
    fig.subplots_adjust(right=0.85) 
    
    # 坐标轴限制
    ax.set_xlim(0, 3.5)
    ax.set_ylim(-1.0, 1.0) # 归一化音频
    
    # 标签
    ax.set_title(f"声学环境衰减分析 ({MetricTranslator.translate('T60')})", 
                 fontproperties=FONT_MEDIUM, fontsize=18, pad=20, color=Palette.HIGHLIGHT)
    ax.set_xlabel("Time (s)", fontproperties=FONT_REGULAR, fontsize=10, alpha=0.6)
    ax.set_ylabel("Amplitude (dB Scale)", fontproperties=FONT_REGULAR, fontsize=10, alpha=0.6)
    
    # 3. 视觉组件
    lines = []
    lines.append(ax.plot([], [], lw=4.0, alpha=0.1, color=Palette.WAVE)[0]) 
    lines.append(ax.plot([], [], lw=2.0, alpha=0.3, color=Palette.WAVE)[0])
    line_wave, = ax.plot([], [], lw=0.8, alpha=0.9, color=Palette.WAVE, label='Raw Signal')
    lines.append(line_wave)

    line_env, = ax.plot([], [], lw=2.0, color=Palette.ENV, linestyle='-', label='Energy Env')
    
    # 幽灵标记 (T60 点)
    t60_line = ax.axvline(x=2.5, color=Palette.HIGHLIGHT, linestyle=':', alpha=0.0)
    ghost_text = ax.text(2.55, 0.6, "寂静边界", fontproperties=FONT_MEDIUM, 
                         color=Palette.HIGHLIGHT, fontsize=12, alpha=0.0)
    
    status_text = ax.text(0.02, 0.90, "", transform=ax.transAxes, 
                          fontproperties=FONT_MEDIUM, fontsize=14, color='#FFFFFF')
    
    # 电平表
    ax_meter = fig.add_axes([0.88, 0.15, 0.03, 0.7])
    ax_meter.set_ylim(-60, 0)
    ax_meter.set_xticklabels([])
    ax_meter.set_ylabel("Level (dBFS)", fontproperties=FONT_REGULAR)
    ax_meter.grid(axis='y', linestyle=':', color=Palette.GRID)
    
    bar_rect = Rectangle((0, -60), 1, 0, color=Palette.WAVE, alpha=0.8)
    peak_rect = Rectangle((0, -60), 1, 0.5, color=Palette.ENV, alpha=0.6)
    ax_meter.add_patch(bar_rect)
    ax_meter.add_patch(peak_rect)

    # --- 动画状态 ---
    fps = 30
    duration = 3.5
    total_frames = int(duration * fps)
    step = int(len(t) / total_frames)
    peak_db = -60

    def init():
        return lines + [line_env, bar_rect, peak_rect, status_text, t60_line, ghost_text]

    def update(frame):
        nonlocal peak_db
        current_idx = min(frame * step, len(t)-1)
        current_time = t[current_idx]
        
        # 绘制数据
        display_idx = np.arange(0, current_idx, 10) 
        if len(display_idx) > 0:
            for l in lines:
                l.set_data(t[display_idx], audio[display_idx])
            line_env.set_data(t[display_idx], envelope[display_idx])
        
        # 电平表逻辑
        window_size = 1000
        win_start = max(0, current_idx - window_size)
        chunk = audio[win_start:current_idx]
        if len(chunk) > 0:
            rms = np.sqrt(np.mean(chunk**2)) + 1e-9
            db = 20 * np.log10(rms)
            db = max(-60, db)
        else:
            db = -60
            
        peak_db = max(peak_db - 0.5, db)
        bar_rect.set_height(db + 60)
        bar_rect.set_y(-60)
        peak_rect.set_y(peak_db)
        
        if db > -5: bar_rect.set_color('#FF0000')
        elif db > -10: bar_rect.set_color('#FFFF00')
        else: bar_rect.set_color(Palette.WAVE)
        
        # 叙事逻辑
        if current_time >= 2.5:
            status_text.set_text("时间的遗物：寂静的边界")
            status_text.set_color(Palette.HIGHLIGHT)
            alpha_decay = max(0, 1.0 - (current_time - 2.5))
            t60_line.set_alpha(alpha_decay)
            ghost_text.set_alpha(alpha_decay)
        else:
            status_text.set_text(f"Decay: {current_time:.2f} s")
            status_text.set_color('#FFFFFF')
            
        return lines + [line_env, bar_rect, peak_rect, status_text, t60_line, ghost_text]

    print("正在渲染动画帧...")
    ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=True)
    
    # 保存临时视频
    temp_video = output_video_path.replace(".mp4", "_silent.mp4")
    ani.save(temp_video, writer='ffmpeg', fps=fps, dpi=dpi)
    
    # 保存封面
    update(int(2.5 * fps))
    fig.savefig(output_cover_path, facecolor=Palette.BG)
    print(f"[图片] 已保存封面: {output_cover_path}")
    
    plt.close(fig)
    
    # 合并音频
    print("正在合并音频...")
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", input_audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    if os.path.exists(output_video_path):
        os.remove(temp_video)
        print(f"[视频] 已保存: {output_video_path}")
    else:
        print("错误: FFmpeg 合并失败。")

def main():
    # 路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mvp_root = os.path.dirname(os.path.dirname(base_dir))
    library_dir = os.path.join(mvp_root, "_Library", "S04_Space")
    
    input_wav = os.path.join(library_dir, "asset_S04_void_ir.wav")
    output_mp4 = os.path.join(library_dir, "asset_S04_void_visual.mp4")
    output_png = os.path.join(library_dir, "cover_S04_void.png")
    
    if not os.path.exists(input_wav):
        print(f"错误: 未找到输入文件 {input_wav}。请先运行生成器。")
        return

    # 加载数据
    fs, audio_int16 = wavfile.read(input_wav)
    audio = audio_int16.astype(np.float32) / 32768.0 # 归一化到 -1..1
    
    duration = len(audio) / fs
    t = np.linspace(0, duration, len(audio), endpoint=False)
    
    # 重建包络 (理论值)
    env = calc_envelope(t, decay_time=2.5)
    
    # 渲染
    render_decay_video(t, audio, env, output_mp4, input_wav, output_png)

if __name__ == "__main__":
    main()
