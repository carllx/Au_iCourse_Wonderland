"""
S05 定位 (Position) - 心理声像资产生成器
---------------------------------------
Narrative: "镜中双生" (Shadow Self)

Fix (v2):
- Improved Tick Sound: More "Clock-like", less "Sine-like".
- Normalized Reverse Voice: Ensure readability of the reversed phonemes.
- Balanced Mix: 50/50 mix to ensure both elements are clear.

输出:
- _Library/S05_Position/asset_S05_shadow_self.wav
- _Library/S05_Position/asset_S05_heartbeat_visceral.wav
"""

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import os

def generate_visceral_heartbeat(duration_sec, fs=48000):
    """
    S05 的心跳：沉重、贴耳、干涩。
    """
    t = np.linspace(0, duration_sec, int(fs * duration_sec), endpoint=False)
    audio = np.zeros_like(t)
    bpm = 60 
    beat_interval = 60.0 / bpm
    num_beats = int(duration_sec / beat_interval)
    
    for i in range(num_beats):
        start = i * beat_interval
        
        # Lub - Distortion Kick
        dur = 0.1
        t_w = np.linspace(0, dur, int(fs * dur))
        f_sweep = np.linspace(90, 40, len(t_w))
        wave = np.sin(2 * np.pi * np.cumsum(f_sweep)/fs)
        wave = np.clip(wave * 2.0, -1.0, 1.0) # Hard Clip
        env = np.exp(-25 * t_w)
        wave *= env
        
        s_idx = int(start * fs)
        if s_idx + len(wave) < len(audio):
            audio[s_idx:s_idx+len(wave)] += wave
            
    return audio

def generate_slowing_tick(duration_sec, fs=48000):
    """
    凝固的时间：逐渐变慢的机械钟表声 (Impulse).
    """
    audio = np.zeros(int(fs * duration_sec))
    t_ptr = 0.0
    interval = 0.5 # Start at 120 BPM equivalent (0.5s)
    
    while t_ptr < duration_sec:
        # Generate one Tick (Short Impulse + High Pass)
        # Impulse
        dur_tick = 0.02 # Very short
        t_tick = np.linspace(0, dur_tick, int(fs * dur_tick))
        noise = np.random.randn(len(t_tick))
        env = np.exp(-200 * t_tick)
        raw_tick = noise * env
        
        # Bandpass to simulate metal mechanic
        # Center at 3000Hz
        nos = signal.resample(raw_tick, len(raw_tick)) # Copy
        b, a = signal.butter(4, [2500/(fs/2), 3500/(fs/2)], 'bandpass')
        tick = signal.filtfilt(b, a, nos)
        
        s_idx = int(t_ptr * fs)
        if s_idx + len(tick) < len(audio):
            audio[s_idx:s_idx+len(tick)] += tick * 0.8
            
        t_ptr += interval
        interval *= 1.15 # Slow down by 15% - Dramatic
        
    return audio

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    
    in_path = os.path.join(project_root, "01_MVP_Demo", "_Library", "S0X_Shared", "asset_S0X_dry_voice_clean.wav")
    out_dir = os.path.join(project_root, "01_MVP_Demo", "_Library", "S05_Position")
    os.makedirs(out_dir, exist_ok=True)

    FS = 48000
    DUR = 10.0
    
    # 1. Heartbeat Visceral
    print("生成沉重心跳...")
    hb = generate_visceral_heartbeat(DUR, FS)
    wavfile.write(os.path.join(out_dir, "asset_S05_heartbeat_visceral.wav"), FS, (hb * 32767).astype(np.int16))
    
    # 2. Shadow Self (Reverse Voice + Tick)
    print("生成镜中阴影 (Reverse + Tick)...")
    if os.path.exists(in_path):
        fs_v, voice = wavfile.read(in_path)
        if voice.dtype != np.float32: voice = voice.astype(np.float32) / 32768.0
        if len(voice.shape) > 1: voice = voice[:, 0]
        
        # Reverse
        voice_rev = voice[::-1]
        
        # Normalize Voice before mix
        voice_rev = voice_rev / np.max(np.abs(voice_rev))
        
        # Trim looped
        # If voice is short, tile it?
        # Let's just tile it to be safe if it's shorter than DUR
        while len(voice_rev) < int(FS * DUR):
            voice_rev = np.concatenate([voice_rev, voice_rev])
            
        voice_rev = voice_rev[:int(FS * DUR)]
            
        # Tick
        tick = generate_slowing_tick(DUR, FS)
        if len(tick) != len(voice_rev):
            tick = np.resize(tick, len(voice_rev))
            
        # Mix: Voice clearly audible, Tick as metronome
        shadow = (voice_rev * 0.6) + (tick * 0.4)
        
        wavfile.write(os.path.join(out_dir, "asset_S05_shadow_self.wav"), FS, (shadow * 32767).astype(np.int16))
    else:
        print(f"Warning: Base voice not found at {in_path}, skipping Shadow Self generation.")

    print(f"--- S05 心理声像资产生成完毕 (FIXED): {out_dir}) ---")

if __name__ == "__main__":
    main()
