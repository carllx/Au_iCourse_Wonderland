"""
S04 空间对比视频渲染器 (Spatial Contrast)
---------------------------------------
生成两个 IR 的波形对比视频，用于可视化不同空间的声音特征。
输入:
- contrast_IR_small_closet.wav
- contrast_IR_large_hall.wav
输出:
- contrast_visual_closet.mp4
- contrast_visual_hall.mp4
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.io import wavfile
import os
import sys
import subprocess

# --- Path Setup ---
# renderers -> _Pipeline -> 01_MVP_Demo -> ROOT
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../")) 
CONFIG_DIR = os.path.join(PROJECT_ROOT, ".agent/skills/lab-factory/config")
sys.path.append(CONFIG_DIR)

try:
    from Visual_System_Config import VisualTheme, Palette, MetricTranslator, CURRENT_THEME, FONT_REGULAR, FONT_MEDIUM
except ImportError:
    print("WARNING: Config not found.")

def render_simple_waveform(wav_path, output_mp4, title, color):
    """简易波形渲染器。"""
    print(f"渲染视频: {os.path.basename(output_mp4)}...")
    
    fs, audio = wavfile.read(wav_path)
    audio = audio.astype(np.float32) / 32768.0
    duration = len(audio) / fs
    t = np.linspace(0, duration, len(audio))
    
    # Setup Plot
    plt.rcParams.update(CURRENT_THEME)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
    ax.set_ylim(-1.0, 1.0)
    ax.set_xlim(0, duration)
    ax.set_title(title, fontproperties=FONT_MEDIUM, fontsize=16, color=color, pad=15)
    ax.set_xlabel("Time (s)", fontproperties=FONT_REGULAR, color='#888888')
    
    line, = ax.plot([], [], lw=1.5, color=color)
    scanline = ax.axvline(x=0, color='#FFFFFF', alpha=0.5, linestyle=':')
    
    # Animation
    fps = 30
    n_frames = int(duration * fps)
    step = int(len(audio) / n_frames)
    
    def init():
        line.set_data([], [])
        return line, scanline
        
    def update(frame):
        current_idx = min(frame * step, len(audio))
        # Draw full waveform up to current point (Scan effect)
        # Optimization: Downsample
        disp_idx = np.arange(0, current_idx, max(1, int(current_idx/1000)))
        if len(disp_idx) > 0:
            line.set_data(t[disp_idx], audio[disp_idx])
            
        current_t = frame / fps
        scanline.set_xdata([current_t])
        return line, scanline

    ani = animation.FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=True)
    
    # Save video only (no audio merge needed for pure visual, but better to have audio)
    temp_mp4 = output_mp4.replace(".mp4", "_temp.mp4")
    ani.save(temp_mp4, writer='ffmpeg', fps=fps)
    plt.close(fig)
    
    # Merge Audio
    cmd = ["ffmpeg", "-y", "-i", temp_mp4, "-i", wav_path, "-c:v", "copy", "-c:a", "aac", output_mp4]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if os.path.exists(temp_mp4): os.remove(temp_mp4)
    print(f"  -> 完成: {output_mp4}")

def main():
    library_dir = os.path.join(PROJECT_ROOT, "01_MVP_Demo", "_Library", "S04_Space")
    
    # 1. Closet
    path_closet = os.path.join(library_dir, "contrast_IR_small_closet.wav")
    out_closet = os.path.join(library_dir, "contrast_visual_closet.mp4")
    if os.path.exists(path_closet):
        render_simple_waveform(path_closet, out_closet, "Small Space: Closet (0.5s)", Palette.WAVE)
        
    # 2. Hall
    path_hall = os.path.join(library_dir, "contrast_IR_large_hall.wav")
    out_hall = os.path.join(library_dir, "contrast_visual_hall.mp4")
    if os.path.exists(path_hall):
        render_simple_waveform(path_hall, out_hall, "Large Space: Hall (2.0s)", Palette.HIGHLIGHT)

if __name__ == "__main__":
    main()
