"""
S05 声像可视化渲染器 (Panning Visual)
-----------------------------------
生成雷达图 (Polar Plot) 可视化左右声道的能量分布。
输入: 
- asset_S05_threat_L.wav
- asset_S05_threat_R.wav
输出:
- visual_S05_radar.mp4 (合成演示)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.io import wavfile
import os
import sys
import subprocess

# --- Path Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../")) 
CONFIG_DIR = os.path.join(PROJECT_ROOT, ".agent/skills/lab-factory/config")
sys.path.append(CONFIG_DIR)

try:
    from Visual_System_Config import VisualTheme, Palette, CURRENT_THEME
except ImportError:
    pass

def render_radar(l_path, r_path, output_mp4):
    print(f"渲染雷达图: {os.path.basename(output_mp4)}...")
    
    fs, l_data = wavfile.read(l_path)
    _, r_data = wavfile.read(r_path)
    
    # 确保是单声道数据用于计算
    if len(l_data.shape) > 1: l_data = l_data[:, 0]
    if len(r_data.shape) > 1: r_data = r_data[:, 1] # R取第二通道
    
    # 归一化
    l_data = l_data.astype(np.float32) / 32768.0
    r_data = r_data.astype(np.float32) / 32768.0
    
    duration = min(len(l_data), len(r_data)) / fs
    duration = min(duration, 5.0) # 只渲染前5秒演示
    
    # Setup Polar Plot
    plt.rcParams.update(CURRENT_THEME)
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111, projection='polar')
    
    # 设置角度: 左=180(pi), 右=0(0), 中=90(pi/2)
    # 我们映射: 
    # Left Threat (at 135 deg)
    # Right Threat (at 45 deg)
    
    ax.set_ylim(0, 1.0)
    ax.set_yticklabels([])
    ax.set_xticklabels(['R', 'FR', 'F', 'FL', 'L', 'BL', 'B', 'BR'], color='#888888')
    ax.grid(color='#333333')
    
    # Bars
    bar_l = ax.bar(np.radians(135), 0, width=0.5, color=Palette.WAVE, alpha=0.8)[0]
    bar_r = ax.bar(np.radians(45), 0, width=0.5, color=Palette.HIGHLIGHT, alpha=0.8)[0]
    
    fps = 30
    n_frames = int(duration * fps)
    step = int(fs / fps)
    
    def update(frame):
        idx = frame * step
        chunk_len = 500
        if idx + chunk_len >= len(l_data): return bar_l, bar_r
        
        # Calculate RMS
        rms_l = np.sqrt(np.mean(l_data[idx:idx+chunk_len]**2)) * 5 # Scale up
        rms_r = np.sqrt(np.mean(r_data[idx:idx+chunk_len]**2)) * 5
        
        bar_l.set_height(min(rms_l, 1.0))
        bar_r.set_height(min(rms_r, 1.0))
        
        return bar_l, bar_r
        
    ani = animation.FuncAnimation(fig, update, frames=n_frames, blit=True)
    
    temp_mp4 = output_mp4.replace(".mp4", "_temp.mp4")
    ani.save(temp_mp4, writer='ffmpeg', fps=fps)
    plt.close(fig)
    
    # Rename (No audio merge for this radar demo)
    if os.path.exists(output_mp4): os.remove(output_mp4)
    os.rename(temp_mp4, output_mp4)
    print(f"  -> 完成: {output_mp4}")

def main():
    lib_dir = os.path.join(PROJECT_ROOT, "01_MVP_Demo", "_Library", "S05_Position")
    l_path = os.path.join(lib_dir, "asset_S05_threat_L.wav")
    r_path = os.path.join(lib_dir, "asset_S05_threat_R.wav")
    out_path = os.path.join(lib_dir, "visual_S05_radar.mp4")
    
    if os.path.exists(l_path) and os.path.exists(r_path):
        render_radar(l_path, r_path, out_path)

if __name__ == "__main__":
    main()
