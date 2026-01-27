"""
S04 湿声演示生成器
----------------
将干净人声与虚空 IR 进行卷积，生成"湿声"演示。

重要物理原理：
- 卷积操作 (convolution) 模拟声音在空间中的传播
- IR 的第一个脉冲 (impulse) 代表直达声 (direct sound)
- 卷积结果已经包含了完整的声学响应：直达声 + 所有反射
- 因此不应再叠加额外的干声，否则会造成"双重直达声"问题

输入: 
  - 1. 干声: _Library/S0X_Shared/asset_S0X_dry_voice_clean.wav
  - 2. IR: _Library/S04_Space/asset_S04_void_ir.wav
输出: 
  - _Library/S04_Space/demo_S04_wet_voice.wav

Version: 3.0 (修正混音逻辑：移除双重干声，输出纯卷积结果)
"""

import numpy as np
import scipy.signal as signal
from scipy.io import wavfile
import os
import sys

def load_wav_normalized(path, target_fs=48000):
    """
    读取 WAV 并归一化为 float32 (-1.0 ~ 1.0)。
    
    参数:
        path: WAV 文件路径
        target_fs: 目标采样率 (Hz)
    
    返回:
        (采样率, 归一化音频数据) 元组
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到文件: {path}")
        
    fs, data = wavfile.read(path)
    
    if fs != target_fs:
        print(f"警告: 采样率不匹配 {path} (文件: {fs}, 目标: {target_fs})。可能会变调。")
        
    # 转换为 float32
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.float32:
        pass
    else:
        # 其他格式简单处理
        data = data.astype(np.float32)
        data = data / np.max(np.abs(data))
        
    # 如果是立体声，取单声道平均
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
        
    return fs, data

def main():
    # 1. 路径设置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    
    # 输入路径
    dry_voice_path = os.path.join(project_root, "01_MVP_Demo", "_Library", "S0X_Shared", "asset_S0X_dry_voice_clean.wav")
    ir_path = os.path.join(project_root, "01_MVP_Demo", "_Library", "S04_Space", "asset_S04_void_ir.wav")
    
    # 输出路径
    output_dir = os.path.join(project_root, "01_MVP_Demo", "_Library", "S04_Space")
    output_path = os.path.join(output_dir, "demo_S04_wet_voice.wav")
    
    print("=" * 60)
    print("S04 湿声演示生成器 v3.0")
    print("=" * 60)
    
    # 2. 加载音频
    try:
        print(f"\n[加载音频文件]")
        print(f"  干声: {os.path.basename(dry_voice_path)}")
        fs_dry, dry_sig = load_wav_normalized(dry_voice_path)
        print(f"    ✓ 采样率: {fs_dry}Hz, 长度: {len(dry_sig)/fs_dry:.2f}s")
        
        print(f"  IR:   {os.path.basename(ir_path)}")
        fs_ir, ir_sig = load_wav_normalized(ir_path, target_fs=fs_dry)
        print(f"    ✓ 采样率: {fs_ir}Hz, 长度: {len(ir_sig)/fs_ir:.2f}s")
        
    except FileNotFoundError as e:
        print(f"\n错误: {e}")
        print("请先运行 gen_S04_void_ir.py 生成虚空 IR")
        return

    # 3. 卷积 (Convolution)
    print(f"\n[执行卷积运算]")
    print(f"  算法: FFT 快速卷积")
    print(f"  物理意义: 模拟声音在虚空空间中的传播")
    
    # mode='full' 会导致长度 = len(a) + len(b) - 1
    wet_sig = signal.fftconvolve(dry_sig, ir_sig, mode='full')
    
    print(f"  ✓ 卷积完成")
    print(f"  输出长度: {len(wet_sig)/fs_dry:.2f}s")
    
    # 4. 混合策略说明
    print(f"\n[混音逻辑]")
    print(f"  策略: 100% 卷积输出（纯湿声）")
    print(f"  ")
    print(f"  原理解释:")
    print(f"    • IR 的第一个脉冲 (t=0) 已经包含直达声")
    print(f"    • 卷积结果 = 直达声 + 早期反射 + 混响尾")
    print(f"    • 不需要再叠加干声（会造成双重直达声）")
    print(f"  ")
    print(f"  旧版本问题（已修正）:")
    print(f"    ✗ 旧: final = dry×0.7 + wet×0.4")
    print(f"    ✗ 结果: 直达声增益 170%，破坏空间感")
    print(f"    ✓ 新: final = wet×1.0")
    print(f"    ✓ 结果: 正确的空间声学响应")
    
    # 使用纯卷积结果
    final_mix = wet_sig * 1.0
    
    # 5. 归一化输出
    print(f"\n[归一化处理]")
    max_val = np.max(np.abs(final_mix))
    if max_val > 0:
        final_mix = final_mix / max_val * 0.95  # -0.5 dB headroom
        print(f"  ✓ 峰值归一化到 -0.5 dBFS")
    
    # 保存
    final_pcm = (final_mix * 32767).astype(np.int16)
    wavfile.write(output_path, fs_dry, final_pcm)
    
    print(f"\n[输出文件]")
    print(f"  ✓ 已生成: {output_path}")
    print(f"  格式: {fs_dry}Hz, 16-bit PCM, 单声道")
    print(f"  长度: {len(final_mix)/fs_dry:.2f}s")
    
    # 6. 听感预期
    print(f"\n[听感预期]")
    print(f"  ✓ 声音应该听起来遥远、空旷")
    print(f"  ✓ 有明显的距离感（100ms 预延迟）")
    print(f"  ✓ 声音\"暗化\"（高频衰减）")
    print(f"  ✓ 混响极长（T60 ≈ 6s）")
    print(f"  ✓ 无墙壁反射（无早期反射）")
    print(f"  ✓ 整体感觉：被深渊吞噬、无限虚空")
    
    print(f"\n[对比测试建议]")
    print(f"  1. 听原始干声: {os.path.basename(dry_voice_path)}")
    print(f"  2. 听虚空湿声: {os.path.basename(output_path)}")
    print(f"  3. 对比差异: 干声清晰近距离 vs 湿声遥远虚空感")
    
    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
