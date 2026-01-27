"""
验证脚本：用 Python 实现降噪，验证 asset_S02_dirty_heartbeat.wav 是否可被恢复
使用频谱减法 (Spectral Subtraction) 算法
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
import os

def spectral_subtraction(mixed_signal, noise_signal, fs, reduction_factor=0.75, smoothing=2):
    """
    频谱减法降噪
    
    参数:
    - mixed_signal: 混合信号 (心跳 + 噪音)
    - noise_signal: 纯噪音信号 (用于采样)
    - fs: 采样率
    - reduction_factor: 降噪强度 (0-1)
    - smoothing: 平滑因子
    """
    
    # 1. 计算 STFT (Short-Time Fourier Transform)
    nperseg = 2048
    noverlap = nperseg // 2
    
    # 混合信号的频谱
    f, t_mixed, Sxx_mixed = signal.stft(mixed_signal, fs, nperseg=nperseg, noverlap=noverlap)
    
    # 噪音信号的频谱 (用于采样)
    f, t_noise, Sxx_noise = signal.stft(noise_signal, fs, nperseg=nperseg, noverlap=noverlap)
    
    # 2. 计算噪音的平均功率谱
    noise_power = np.mean(np.abs(Sxx_noise) ** 2, axis=1, keepdims=True)
    
    # 3. 频谱减法
    mixed_power = np.abs(Sxx_mixed) ** 2
    
    # 减去噪音功率
    cleaned_power = mixed_power - reduction_factor * noise_power
    
    # 确保不为负
    cleaned_power = np.maximum(cleaned_power, 0.1 * mixed_power)
    
    # 4. 平滑处理
    if smoothing > 1:
        kernel_size = smoothing * 2 + 1
        for i in range(cleaned_power.shape[0]):
            cleaned_power[i, :] = signal.medfilt(cleaned_power[i, :], kernel_size=kernel_size)
    
    # 5. 恢复相位
    phase = np.angle(Sxx_mixed)
    cleaned_magnitude = np.sqrt(cleaned_power)
    Sxx_cleaned = cleaned_magnitude * np.exp(1j * phase)
    
    # 6. 逆 STFT
    _, cleaned_signal = signal.istft(Sxx_cleaned, fs, nperseg=nperseg, noverlap=noverlap)
    
    return cleaned_signal, f, t_mixed, Sxx_mixed, Sxx_cleaned

def analyze_signal(signal_data, fs, label="Signal"):
    """分析信号的频谱特性"""
    f, Pxx = signal.welch(signal_data, fs, nperseg=4096)
    
    # 找出主要峰值
    peak_indices = signal.find_peaks(Pxx, height=np.max(Pxx) * 0.05)[0]
    
    print(f"\n=== {label} 频谱分析 ===")
    print(f"RMS 能量: {np.sqrt(np.mean(signal_data**2)):.4f}")
    
    # 低频能量
    low_freq_mask = f < 200
    low_freq_power = np.sum(Pxx[low_freq_mask])
    total_power = np.sum(Pxx)
    print(f"低频 (0-200Hz) 能量占比: {low_freq_power/total_power*100:.1f}%")
    
    # 高频能量
    high_freq_mask = (f >= 300) & (f <= 24000)
    high_freq_power = np.sum(Pxx[high_freq_mask])
    print(f"高频 (300-24kHz) 能量占比: {high_freq_power/total_power*100:.1f}%")
    
    # 心跳频率
    heartbeat_mask = (f >= 50) & (f <= 80)
    heartbeat_power = np.sum(Pxx[heartbeat_mask])
    print(f"心跳基频 (50-80Hz) 能量占比: {heartbeat_power/total_power*100:.2f}%")
    
    print(f"\n主要频率峰值 (>5% 最大值):")
    for idx in peak_indices[:10]:
        print(f"  {f[idx]:.1f} Hz: {Pxx[idx]:.2e}")
    
    return f, Pxx

def main():
    # 1. 加载音频
    print("=" * 60)
    print("降噪可行性验证")
    print("=" * 60)
    
    mixed_path = '01_MVP_Demo/_Library/S02_Purify/asset_S02_dirty_heartbeat.wav'
    
    if not os.path.exists(mixed_path):
        print(f"错误: 找不到文件 {mixed_path}")
        return
    
    fs, mixed_data = wavfile.read(mixed_path)
    
    # 转换为浮点数
    if mixed_data.dtype == np.int16:
        mixed_data = mixed_data.astype(np.float32) / 32768.0
    
    print(f"\n加载混合信号: {mixed_path}")
    print(f"采样率: {fs} Hz")
    print(f"时长: {len(mixed_data) / fs:.2f} 秒")
    
    # 2. 提取纯噪音样本 (前 1 秒，假设没有心跳)
    # 实际上，我们需要从混合信号中提取噪音
    # 这里我们使用一个简单的方法：取最小能量的片段
    
    # 分割成多个片段，找出最"安静"的片段作为噪音样本
    segment_length = int(fs * 1.0)  # 1 秒
    num_segments = len(mixed_data) // segment_length
    
    segment_energies = []
    for i in range(num_segments):
        segment = mixed_data[i*segment_length:(i+1)*segment_length]
        energy = np.sqrt(np.mean(segment**2))
        segment_energies.append(energy)
    
    # 找出能量最低的片段作为噪音样本
    min_energy_idx = np.argmin(segment_energies)
    noise_sample = mixed_data[min_energy_idx*segment_length:(min_energy_idx+1)*segment_length]
    
    print(f"\n使用第 {min_energy_idx+1} 段作为噪音样本 (能量最低)")
    
    # 3. 分析原始信号
    f_orig, Pxx_orig = analyze_signal(mixed_data, fs, "原始混合信号")
    
    # 4. 执行降噪
    print("\n" + "=" * 60)
    print("执行频谱减法降噪...")
    print("=" * 60)
    
    cleaned_signal, f_stft, t_stft, Sxx_mixed, Sxx_cleaned = spectral_subtraction(
        mixed_data, 
        noise_sample, 
        fs, 
        reduction_factor=0.75,
        smoothing=2
    )
    
    # 确保长度一致
    min_len = min(len(mixed_data), len(cleaned_signal))
    cleaned_signal = cleaned_signal[:min_len]
    
    # 5. 分析降噪后的信号
    f_cleaned, Pxx_cleaned = analyze_signal(cleaned_signal, fs, "降噪后的信号")
    
    # 6. 对比分析
    print("\n" + "=" * 60)
    print("降噪效果对比")
    print("=" * 60)
    
    # 计算信噪比改善
    low_freq_mask = f_orig < 200
    high_freq_mask = (f_orig >= 300) & (f_orig <= 24000)
    
    orig_low = np.sum(Pxx_orig[low_freq_mask])
    orig_high = np.sum(Pxx_orig[high_freq_mask])
    orig_snr = orig_low / orig_high if orig_high > 0 else 0
    
    cleaned_low = np.sum(Pxx_cleaned[low_freq_mask])
    cleaned_high = np.sum(Pxx_cleaned[high_freq_mask])
    cleaned_snr = cleaned_low / cleaned_high if cleaned_high > 0 else 0
    
    print(f"\n信噪比 (低频/高频):")
    print(f"  原始: {orig_snr:.4f}")
    print(f"  降噪后: {cleaned_snr:.4f}")
    print(f"  改善倍数: {cleaned_snr/orig_snr:.2f}x")
    
    # 7. 保存降噪后的音频
    output_path = '01_MVP_Demo/_Library/S02_Purify/asset_S02_cleaned_heartbeat.wav'
    
    # 归一化
    max_val = np.max(np.abs(cleaned_signal))
    if max_val > 0:
        cleaned_signal = cleaned_signal / max_val * 0.95
    
    # 保存
    cleaned_pcm = (cleaned_signal * 32767).astype(np.int16)
    wavfile.write(output_path, fs, cleaned_pcm)
    
    print(f"\n✅ 降噪后的音频已保存: {output_path}")
    
    # 8. 最终结论
    print("\n" + "=" * 60)
    print("结论")
    print("=" * 60)
    
    if cleaned_snr > orig_snr * 1.5:
        print("✅ 降噪成功！")
        print(f"   - 信噪比改善了 {cleaned_snr/orig_snr:.2f} 倍")
        print(f"   - 心跳信号可以被有效恢复")
        print(f"   - Audition 中应该也能成功恢复")
    else:
        print("❌ 降噪效果不理想")
        print(f"   - 信噪比改善不足 ({cleaned_snr/orig_snr:.2f}x)")
        print(f"   - 可能需要调整合成参数")

if __name__ == "__main__":
    main()
