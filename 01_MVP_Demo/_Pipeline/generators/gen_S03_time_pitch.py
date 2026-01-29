"""
S03 塑形 (Sculpt) - 丑小鸭演示生成器
-----------------------------------
Narrative: "缺陷美学"
目标: 生成一段只有物理变调(Pitch Up)的音频，展示"滑稽感"(Chipmunk Effect)。
教学目的: 反衬 Audition "Format Preservation" 的魔法。

输入: _Library/S0X_Shared/asset_S0X_dry_voice_clean.wav
输出: _Library/S03_Sculpt/demo_S03_ugly_duckling.wav
"""

import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    
    in_path = os.path.join(project_root, "01_MVP_Demo", "_Library", "S0X_Shared", "asset_S0X_dry_voice_clean.wav")
    out_dir = os.path.join(project_root, "01_MVP_Demo", "_Library", "S03_Sculpt")
    out_path = os.path.join(out_dir, "demo_S03_ugly_duckling.wav")
    
    os.makedirs(out_dir, exist_ok=True)
    
    if not os.path.exists(in_path):
        print(f"Error: 找不到输入文件 {in_path}")
        # Fallback: 生成一个简单的 Sawtooth 语音模拟，以防测试失败
        # 但既然 user 确认了 base asset 存在，这里我们只需报错提示。
        return

    fs, data = wavfile.read(in_path)
    if data.dtype != np.float32:
        data = data.astype(np.float32) / 32768.0
    if len(data.shape) > 1: data = data[:, 0] # Mono
    
    # 截取前 5 秒
    if len(data) > fs * 5:
        data = data[:fs*5]
        
    # --- The Ugly Transformation ---
    # Target: Pitch +5 Semitones
    # Formula: Rate_new = Rate_old * 2^(5/12)
    # Resample to FEWER samples (play faster = pitch up)
    semitones = 5
    speed_factor = 2 ** (semitones / 12.0) # ~1.3348
    
    new_len = int(len(data) / speed_factor)
    
    print(f"Resampling: +{semitones} Semitones (Speed x{speed_factor:.2f})...")
    # scipy.signal.resample performs FFT-based resampling (high quality but maintains speed-pitch link)
    ugly_duckling = signal.resample(data, new_len)
    
    # Normalize
    ugly_duckling = ugly_duckling / np.max(np.abs(ugly_duckling)) * 0.95
    
    wavfile.write(out_path, fs, (ugly_duckling * 32767).astype(np.int16))
    print(f"--- S03 丑小鸭演示生成完毕: {out_path} ---")

if __name__ == "__main__":
    main()
