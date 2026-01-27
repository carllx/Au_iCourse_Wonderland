"""
S02 净化 (Purify) - 资产生成器 (v12 - 真实粉红噪音版本)
-----------------------------
Narrative: "生命派" (Path B)
目标: 生成一段被厚重"现实尘埃" (Pink Noise) 掩盖的 "卑微生命" (Heartbeat)。
学生任务: 采样噪音(避开心跳)，降噪，显露心跳。

Fix (v12 - 真实粉红噪音): 
- v11 问题: 频率分离太完美，看起来不自然，不像真实音频
- v12 修复: 
  * 使用真实的粉红噪音（宽带，覆盖整个频谱）
  * 心跳: 60Hz 基频 + 谐波 (自然的心跳声)
  * 噪音: 粉红噪音 (自然的背景噪音)
  * 心跳能量: +3dB (1.4)
  * 噪音能量: -6dB (0.5)
  * 比例: 心跳 : 噪音 = 1.4 : 0.5 ≈ 3 : 1
- Result: 清除前听到自然的混合声，清除后只听到清晰心跳

输出: _Library/S02_Purify/asset_S02_dirty_heartbeat.wav
"""

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import os

def generate_natural_heartbeat(duration_sec, sample_rate=48000, bpm=50):
    """
    生成自然的心跳信号 (v12 - 真实版本)
    - 基频 60Hz
    - 多个谐波 (120Hz, 180Hz, 240Hz)
    - 自然的包络
    """
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    audio = np.zeros_like(t)
    
    beat_interval = 60.0 / bpm
    num_beats = int(duration_sec / beat_interval)
    
    for i in range(num_beats):
        start = i * beat_interval
        
        # Lub (Systole)
        dur_lub = 0.15
        t_lub = np.linspace(0, dur_lub, int(sample_rate * dur_lub))
        
        f_fundamental = 60
        lub = np.zeros_like(t_lub)
        
        # 包络
        env = np.exp(-8 * t_lub)
        
        # 基频 + 谐波
        lub += np.sin(2 * np.pi * f_fundamental * t_lub) * env * 1.5
        lub += np.sin(2 * np.pi * f_fundamental * 2 * t_lub) * env * 0.8
        lub += np.sin(2 * np.pi * f_fundamental * 3 * t_lub) * env * 0.4
        lub += np.sin(2 * np.pi * f_fundamental * 4 * t_lub) * env * 0.2
        
        s_idx = int(start * sample_rate)
        if s_idx + len(lub) < len(audio):
            audio[s_idx:s_idx+len(lub)] += lub * 1.5
            
        # Dub (Diastole)
        s_idx_d = s_idx + int(0.25 * sample_rate)
        if s_idx_d + len(lub) < len(audio):
            audio[s_idx_d:s_idx_d+len(lub)] += lub * 0.8
    
    return audio

def generate_pink_noise(n_samples, fs=48000):
    """
    生成真实的粉红噪音 (宽带)
    强度: -6dB (0.5)
    """
    white = np.random.randn(n_samples)
    X = np.fft.rfft(white)
    S = np.sqrt(np.arange(len(X)) + 1.)
    X = X / S
    pink = np.fft.irfft(X)
    
    return pink

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    output_dir = os.path.join(project_root, "01_MVP_Demo", "_Library", "S02_Purify")
    os.makedirs(output_dir, exist_ok=True)
    
    FS = 48000
    DURATION = 15.0 
    
    # 1. Heartbeat (自然)
    print("生成自然的心跳...")
    heartbeat = generate_natural_heartbeat(DURATION, FS, bpm=50)
    
    # 2. Pink Noise (真实)
    print("生成真实的粉红噪音...")
    noise = generate_pink_noise(len(heartbeat), FS)
    
    # 3. Mixing
    # 心跳: +3dB (1.4)
    # 噪音: -6dB (0.5)
    
    noise = noise / np.max(np.abs(noise)) * 0.5   # -6dB
    heartbeat = heartbeat / np.max(np.abs(heartbeat)) * 1.4  # +3dB
    
    final_mix = noise + heartbeat
    
    # 归一化
    max_val = np.max(np.abs(final_mix))
    if max_val > 0:
        final_mix = final_mix / max_val * 0.95
    
    output_path = os.path.join(output_dir, "asset_S02_dirty_heartbeat.wav")
    wavfile.write(output_path, FS, (final_mix * 32767).astype(np.int16))
    print(f"--- S02 资产生成完毕 (v12 真实粉红噪音): {output_path} ---")
    print(f"\n混合参数:")
    print(f"  心跳: 自然的 60Hz 基频 + 谐波 - 能量: +3dB")
    print(f"  噪音: 真实的粉红噪音 (宽带) - 能量: -6dB")
    print(f"  能量比例: 心跳 : 噪音 = 1.4 : 0.5 ≈ 3 : 1")

if __name__ == "__main__":
    main()








