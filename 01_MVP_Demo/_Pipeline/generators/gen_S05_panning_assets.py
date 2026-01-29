"""
S05 定位 (Position) - 心理声像资产生成器 (v3: Spiral + Wall)
--------------------------------------------------------------
Narrative: "压力与焦虑"
Design Philosophy:
1. Pressure (The Wall): 一堵从前方逼近的墙。视觉上是扩张的扇形。
2. Anxiety (The Needle): 一根高速旋绕并靠近的刺。视觉上是螺旋线。

输出:
- _Library/S05_Position/asset_S05_heartbeat_visceral.wav
- _Library/S05_Position/asset_S05_shadow_self.wav (Clean Reverse Voice)
- _Library/S05_Position/asset_S05_threat_pressure.wav (Static Mono Source)
- _Library/S05_Position/asset_S05_threat_anxiety.wav (Static Mono Source)
- _Library/S05_Position/demo_S05_spiral_mix.wav (Final Stereo Demo)
"""

import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import os

# --- Global Config ---
FS = 48000
DUR = 15.0  # Longer demo for spiral effect
BPM = 60

def get_project_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != "/":
        if os.path.exists(os.path.join(current, ".agent")):
            return current
        current = os.path.dirname(current)
    return current

PROJECT_ROOT = get_project_root()
OUT_DIR = os.path.join(PROJECT_ROOT, "01_MVP_Demo/_Library/S05_Position")
SRC_VOICE = os.path.join(PROJECT_ROOT, "01_MVP_Demo/_Library/S0X_Shared/asset_S0X_dry_voice_clean.wav")

def ensure_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def save_wav(path, data, fs=FS):
    data = np.clip(data, -1.0, 1.0)
    output = (data * 32767).astype(np.int16)
    wavfile.write(path, fs, output)
    print(f"  -> Saved: {os.path.basename(path)}")

# ==============================================================================
# Part 1: Individual Asset Generators (Mono Sources)
# ==============================================================================

def generate_visceral_heartbeat(duration_sec, fs=48000):
    """
    骨传导心跳。固定在 Center。
    """
    t = np.linspace(0, duration_sec, int(fs * duration_sec), endpoint=False)
    audio = np.zeros_like(t)
    beat_interval = 60.0 / BPM
    num_beats = int(duration_sec / beat_interval)
    
    for i in range(num_beats):
        start = i * beat_interval
        
        # Lub
        dur = 0.1
        t_w = np.linspace(0, dur, int(fs * dur))
        f_sweep = np.linspace(90, 40, len(t_w))
        wave = np.sin(2 * np.pi * np.cumsum(f_sweep)/fs)
        wave = np.clip(wave * 2.0, -1.0, 1.0)
        env = np.exp(-25 * t_w)
        wave *= env
        
        # Dub
        dur2 = 0.08
        t_w2 = np.linspace(0, dur2, int(fs * dur2))
        f_sweep2 = np.linspace(110, 60, len(t_w2))
        wave2 = np.sin(2 * np.pi * np.cumsum(f_sweep2)/fs)
        env2 = np.exp(-30 * t_w2)
        wave2 *= env2
        
        s_idx = int(start * fs)
        if s_idx + len(wave) < len(audio):
            audio[s_idx:s_idx+len(wave)] += wave
            
        s_idx2 = int((start + 0.3) * fs)
        if s_idx2 + len(wave2) < len(audio):
             audio[s_idx2:s_idx2+len(wave2)] += wave2 * 0.7

    return audio

def generate_pressure_source(duration_sec, fs=48000):
    """
    Pressure (The Wall) - 源信号。低频轰鸣。
    """
    t = np.linspace(0, duration_sec, int(fs * duration_sec), endpoint=False)
    drone = signal.square(2 * np.pi * 55 * t)
    sos = signal.butter(2, 100, 'lp', fs=fs, output='sos')
    pressure = signal.sosfilt(sos, drone)
    return pressure * 0.5

def generate_anxiety_source(duration_sec, fs=48000):
    """
    Anxiety (The Needle) - 源信号。高频金属摩擦。
    """
    t = np.linspace(0, duration_sec, int(fs * duration_sec), endpoint=False)
    
    # Interference Tones
    s1 = np.sin(2 * np.pi * 3000 * t)
    s2 = np.sin(2 * np.pi * 3150 * t)
    metallic = (s1 + s2) * 0.5
    return metallic * 0.2

def process_shadow_self(src_path, duration_sec, fs=48000):
    """
    Shadow Self: 纯净反向人声。
    """
    if not os.path.exists(src_path):
        print("  Warning: Source voice not found.")
        return np.zeros(int(fs * duration_sec))
        
    fs_v, voice = wavfile.read(src_path)
    if len(voice.shape) > 1: voice = voice[:, 0]
    if voice.dtype != np.float32: 
        voice = voice.astype(np.float32) / 32768.0 if voice.dtype == np.int16 else voice.astype(np.float32)

    # RESAMPLE FIX
    if fs_v != fs:
        num_samples = int(len(voice) * fs / fs_v)
        voice = signal.resample(voice, num_samples)
        
    # REVERSE
    voice_rev = voice[::-1]
    
    # NORMALIZE
    voice_rev = voice_rev / (np.max(np.abs(voice_rev)) + 1e-6)
    
    # LOOP/TRIM
    target_samples = int(fs * duration_sec)
    while len(voice_rev) < target_samples:
        voice_rev = np.concatenate([voice_rev, voice_rev])
    
    return voice_rev[:target_samples]

# ==============================================================================
# Part 2: Dynamic Panning DSP Functions (The Core Algorithms)
# ==============================================================================

def apply_spiral_pan(mono_signal, fs, rotations=3.0, start_radius=1.0, end_radius=0.1):
    """
    将一个单声道信号处理成"螺旋靠近"的立体声效果。
    Needle: 360度环绕 + 逐渐靠近 (音量增大)。
    """
    n_samples = len(mono_signal)
    t = np.linspace(0, 1, n_samples)  # Normalized time 0..1
    
    # 1. Angle (Rotations * 2π)
    angle = t * rotations * 2 * np.pi
    
    # 2. Radius (Lerp from start to end)
    radius = start_radius + t * (end_radius - start_radius)
    
    # 3. Pan Law (Sin/Cos)
    pan_L = np.cos(angle)
    pan_R = np.sin(angle)
    
    # 4. Distance Gain (Inverse of radius, capped)
    distance_gain = np.clip(1.0 / (radius + 0.1), 0.5, 3.0)
    
    # Apply
    L = mono_signal * pan_L * distance_gain
    R = mono_signal * pan_R * distance_gain
    
    return L, R

def apply_approaching_wall(mono_signal, fs,
                            start_cutoff=200, end_cutoff=8000,
                            start_width=0.2, end_width=1.0):
    """
    将一个单声道信号处理成"墙体逼近"的立体声效果。
    Wall: Filter opens up (Low -> High) + Stereo Width expands (Narrow -> Wide)。
    """
    n_samples = len(mono_signal)
    t_norm = np.linspace(0, 1, n_samples)  # Normalized time
    
    # 1. Dynamic Low Pass Filter (Cutoff Sweeps)
    # 实现: 分块处理，每块应用不同的截止频率
    chunk_size = fs // 10  # 100ms chunks
    n_chunks = n_samples // chunk_size
    filtered = np.zeros_like(mono_signal)
    
    for i in range(n_chunks):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        if end_idx > n_samples: end_idx = n_samples
        
        # Interpolate cutoff for this chunk
        chunk_t = (i + 0.5) / n_chunks
        cutoff = start_cutoff + chunk_t * (end_cutoff - start_cutoff)
        cutoff = min(cutoff, fs / 2 - 100)  # Nyquist safety
        
        sos = signal.butter(2, cutoff, 'lp', fs=fs, output='sos')
        filtered[start_idx:end_idx] = signal.sosfilt(sos, mono_signal[start_idx:end_idx])
    
    # Handle remaining samples
    if n_chunks * chunk_size < n_samples:
        start_idx = n_chunks * chunk_size
        filtered[start_idx:] = mono_signal[start_idx:]

    # 2. Stereo Width (M/S Processing)
    # Mid = Mono, Side = Noise/Detune for "width"
    # Width factor grows over time
    width_env = start_width + t_norm * (end_width - start_width)
    
    # Create a pseudo-side signal by delaying one channel
    delay_samples = int(0.0005 * fs)  # 0.5ms Haas Effect
    side_L = np.roll(filtered, delay_samples)
    side_R = np.roll(filtered, -delay_samples)
    
    # Mix Mid and Side based on width envelope
    L = filtered * (1 - width_env) + side_L * width_env
    R = filtered * (1 - width_env) + side_R * width_env
    
    # 3. Volume Swell (Closer = Louder)
    volume_env = 0.5 + t_norm * 0.5  # From 0.5x to 1.0x
    L *= volume_env
    R *= volume_env
    
    return L, R

# ==============================================================================
# Part 3: Main Execution
# ==============================================================================

def main():
    print("--- S05 Asset Generator (v3: Spiral + Wall) ---")
    ensure_dir()
    
    # --- Generate Source Assets (Mono) ---
    print("[Phase 1] Generating Source Assets...")
    
    print("  1.1 Visceral Heartbeat")
    hb = generate_visceral_heartbeat(DUR, FS)
    save_wav(os.path.join(OUT_DIR, "asset_S05_heartbeat_visceral.wav"), hb)
    
    print("  1.2 Shadow Self (Reverse Voice)")
    shadow = process_shadow_self(SRC_VOICE, DUR, FS)
    save_wav(os.path.join(OUT_DIR, "asset_S05_shadow_self.wav"), shadow)
    
    print("  1.3 Pressure Source (The Wall)")
    pressure_src = generate_pressure_source(DUR, FS)
    save_wav(os.path.join(OUT_DIR, "asset_S05_threat_pressure.wav"), pressure_src)
    
    print("  1.4 Anxiety Source (The Needle)")
    anxiety_src = generate_anxiety_source(DUR, FS)
    save_wav(os.path.join(OUT_DIR, "asset_S05_threat_anxiety.wav"), anxiety_src)
    
    # --- Generate Final Demo Mix (Stereo) ---
    print("[Phase 2] Generating Demo Mix with Dynamic Panning...")
    
    # Apply dynamic effects
    print("  2.1 Applying Spiral Pan to Anxiety (Needle)...")
    anx_L, anx_R = apply_spiral_pan(anxiety_src, FS, rotations=4, start_radius=1.0, end_radius=0.15)
    
    print("  2.2 Applying Approaching Wall to Pressure...")
    wall_L, wall_R = apply_approaching_wall(pressure_src, FS, 
                                             start_cutoff=150, end_cutoff=5000,
                                             start_width=0.1, end_width=0.9)
    
    # Combine all layers
    print("  2.3 Combining layers...")
    mix_L = np.zeros(int(FS * DUR))
    mix_R = np.zeros(int(FS * DUR))
    
    # Center: Heartbeat + Shadow (Both mono, equal L/R)
    mix_L += hb * 0.7 + shadow * 0.5
    mix_R += hb * 0.7 + shadow * 0.5
    
    # Dynamic: Needle (Spiral)
    n = min(len(mix_L), len(anx_L))
    mix_L[:n] += anx_L[:n] * 0.6
    mix_R[:n] += anx_R[:n] * 0.6
    
    # Dynamic: Wall (Approaching)
    n = min(len(mix_L), len(wall_L))
    mix_L[:n] += wall_L[:n] * 0.5
    mix_R[:n] += wall_R[:n] * 0.5
    
    # Limiter
    stereo = np.vstack((mix_L, mix_R)).T
    stereo = np.clip(stereo, -0.95, 0.95)
    
    save_wav(os.path.join(OUT_DIR, "demo_S05_spiral_mix.wav"), stereo)
    
    print("\n[Done] All assets generated.")
    print(f"Output Directory: {OUT_DIR}")

if __name__ == "__main__":
    main()
