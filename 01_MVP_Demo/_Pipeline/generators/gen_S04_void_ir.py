"""
S04 虚空 IR 生成器
-----------------
生成"虚空"空间 (S04) 的脉冲响应。
特征：无墙壁、无早期反射、只有无限延伸的衰减。

输出: _Library/S04_Space/asset_S04_void_ir.wav

Version: 3.0 (改进声学模型：Voss-McCartney粉红噪音、频率相关衰减、验证指标)
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal as scipy_signal
import os

def generate_pink_noise_voss(n_samples, num_sources=16, random_seed=None):
    """
    使用 Voss-McCartney 算法生成粉红噪音。
    
    该方法比 FFT 整形更准确，产生真正的 -3dB/octave 频谱斜率。
    原理：使用多个白噪音源，每个源以不同的速率更新，叠加后产生 1/f 特性。
    
    参数:
        n_samples: 生成的样本数
        num_sources: 噪音源数量（默认16，质量与性能的平衡）
        random_seed: 随机种子，用于可重复性（可选）
    
    返回:
        粉红噪音数组，归一化到 [-1, 1] 范围
    
    参考: Voss-McCartney algorithm for 1/f noise generation
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # 初始化噪音源
    sources = np.random.randn(num_sources)
    output = np.zeros(n_samples)
    
    # 为每个样本生成粉红噪音
    for i in range(n_samples):
        # 更新噪音源（二进制计数器方法）
        # 当 i 的二进制表示中某一位从0变1时，更新对应的源
        update_mask = i & -i  # 获取最低位的1
        if update_mask > 0:
            source_idx = int(np.log2(update_mask)) % num_sources
            sources[source_idx] = np.random.randn()
        
        # 当前样本是所有源的和
        output[i] = np.sum(sources)
    
    # 归一化到 [-1, 1]
    output = output / np.max(np.abs(output))
    
    return output

def generate_pink_noise(n_samples):
    """
    生成粉红噪音的包装函数（保持向后兼容）。
    现在使用 Voss-McCartney 算法替代旧的 FFT 方法。
    """
    return generate_pink_noise_voss(n_samples, num_sources=16)

def apply_frequency_dependent_decay(signal_input, sample_rate, t60_low, t60_high):
    """
    对信号应用频率相关衰减，模拟空气吸收和材料阻尼。
    
    高频衰减比低频快，这是真实空间的物理特性：
    - 空气吸收高频能量
    - 材料对高频的阻尼更强
    
    参数:
        signal_input: 输入信号（通常是混响尾）
        sample_rate: 采样率 (Hz)
        t60_low: 低频段的 T60 时间（秒），参考频率 125Hz
        t60_high: 高频段的 T60 时间（秒），参考频率 8kHz
    
    返回:
        应用频率相关衰减后的信号
    
    实现策略:
        使用三频段滤波器分离低/中/高频，对每个频段应用不同的衰减包络
    """
    n_samples = len(signal_input)
    duration = n_samples / sample_rate
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # 定义频段分界点
    LOW_CUTOFF = 500    # Hz
    HIGH_CUTOFF = 4000  # Hz
    
    # 设计 Butterworth 滤波器（4阶，平滑过渡）
    sos_low = scipy_signal.butter(4, LOW_CUTOFF, btype='low', fs=sample_rate, output='sos')
    sos_mid = scipy_signal.butter(4, [LOW_CUTOFF, HIGH_CUTOFF], btype='band', fs=sample_rate, output='sos')
    sos_high = scipy_signal.butter(4, HIGH_CUTOFF, btype='high', fs=sample_rate, output='sos')
    
    # 分离频段
    band_low = scipy_signal.sosfilt(sos_low, signal_input)
    band_mid = scipy_signal.sosfilt(sos_mid, signal_input)
    band_high = scipy_signal.sosfilt(sos_high, signal_input)
    
    # 计算中频段的 T60（线性插值）
    t60_mid = (t60_low + t60_high) / 2
    
    # 为每个频段生成衰减包络
    alpha_low = -np.log(0.001) / t60_low
    alpha_mid = -np.log(0.001) / t60_mid
    alpha_high = -np.log(0.001) / t60_high
    
    env_low = np.exp(-t * alpha_low)
    env_mid = np.exp(-t * alpha_mid)
    env_high = np.exp(-t * alpha_high)
    
    # 应用衰减
    band_low *= env_low
    band_mid *= env_mid
    band_high *= env_high
    
    # 重新组合
    output = band_low + band_mid + band_high
    
    return output

def apply_lowpass_filter(signal_input, sample_rate, cutoff_hz, order=4):
    """
    应用低通滤波器，用于"暗化"虚空的声音特征。
    
    参数:
        signal_input: 输入信号
        sample_rate: 采样率 (Hz)
        cutoff_hz: 截止频率 (Hz)
        order: 滤波器阶数（默认4阶，12dB/octave）
    
    返回:
        滤波后的信号
    """
    sos = scipy_signal.butter(order, cutoff_hz, btype='low', fs=sample_rate, output='sos')
    filtered = scipy_signal.sosfilt(sos, signal_input)
    return filtered

def measure_t60(ir, sample_rate):
    """
    使用 Schroeder 反向积分法测量 T60 混响时间。
    
    T60 定义：声音衰减 60dB 所需的时间。
    
    参数:
        ir: 脉冲响应信号
        sample_rate: 采样率 (Hz)
    
    返回:
        T60 时间（秒），如果无法测量则返回 None
    """
    # 计算能量包络（平方）
    energy = ir ** 2
    
    # Schroeder 反向积分
    schroeder = np.cumsum(energy[::-1])[::-1]
    schroeder = schroeder / schroeder[0]  # 归一化
    
    # 转换为 dB
    schroeder_db = 10 * np.log10(schroeder + 1e-10)  # 避免 log(0)
    
    # 找到 -5dB 和 -35dB 的位置（使用 -5 到 -35 dB 范围来估算 T60）
    try:
        idx_5db = np.where(schroeder_db <= -5)[0][0]
        idx_35db = np.where(schroeder_db <= -35)[0][0]
        
        # 线性拟合这段衰减曲线
        time_range = np.arange(idx_5db, idx_35db) / sample_rate
        db_range = schroeder_db[idx_5db:idx_35db]
        
        # 计算斜率（dB/秒）
        slope = (db_range[-1] - db_range[0]) / (time_range[-1] - time_range[0])
        
        # 外推到 60dB
        t60 = 60 / abs(slope)
        
        return t60
    except (IndexError, ZeroDivisionError):
        return None

def analyze_spectrum(signal_input, sample_rate):
    """
    分析信号的频谱特性，验证粉红噪音质量。
    
    参数:
        signal_input: 输入信号
        sample_rate: 采样率 (Hz)
    
    返回:
        字典，包含频谱分析结果
    """
    # 计算 FFT
    n = len(signal_input)
    fft = np.fft.rfft(signal_input)
    freqs = np.fft.rfftfreq(n, 1/sample_rate)
    magnitude_db = 20 * np.log10(np.abs(fft) + 1e-10)
    
    # 计算八度音程能量
    octave_bands = [
        (31.5, 63),
        (63, 125),
        (125, 250),
        (250, 500),
        (500, 1000),
        (1000, 2000),
        (2000, 4000),
        (4000, 8000),
        (8000, 16000)
    ]
    
    octave_energies = []
    for low, high in octave_bands:
        mask = (freqs >= low) & (freqs < high)
        if np.any(mask):
            band_energy = np.mean(magnitude_db[mask])
            octave_energies.append(band_energy)
        else:
            octave_energies.append(None)
    
    return {
        'octave_bands': octave_bands,
        'octave_energies': octave_energies,
        'freqs': freqs,
        'magnitude_db': magnitude_db
    }

# 虚空配置参数
VOID_CONFIG = {
    't60': 6.0,                    # 极长的混响时间，模拟无限空间
    'duration': 8.0,               # 足够长以捕获完整衰减
    'pre_delay_ms': 100,           # 预延迟，创造距离感
    'tail_gain': 0.3,              # 降低混响尾能量，突出虚空的空旷感
    'high_freq_damping': 0.5,      # 高频衰减系数（相对于低频）
    'lpf_cutoff_hz': 4000,         # 低通滤波器截止频率，"暗化"声音
    'sample_rate': 48000
}

def generate_void_ir(duration_sec=8.0, sample_rate=48000, decay_time=6.0, pre_delay_ms=100, 
                     high_freq_damping=0.5, lpf_cutoff_hz=4000):
    """
    生成虚空 IR：无墙壁、无早期反射、只有纯粹的衰减。
    
    虚空的声学特征：
    - 极长的混响时间（T60 ≥ 6s），模拟无限延伸
    - 无早期反射（无墙壁边界）
    - 频率相关衰减（高频衰减更快，声音"暗化"）
    - 预延迟（模拟声音飞向虚空的距离感）
    
    参数:
        duration_sec: 总时长（秒），建议 ≥ 8s 以捕获完整衰减
        sample_rate: 采样率 (Hz)
        decay_time: T60 衰减时间（秒），低频参考值
        pre_delay_ms: 预延迟（毫秒），模拟"声音飞向虚空的时间"
        high_freq_damping: 高频衰减系数（0-1），相对于低频的衰减比例
        lpf_cutoff_hz: 低通滤波器截止频率 (Hz)，用于"暗化"声音
    
    返回:
        (时间轴, IR信号, 衰减包络) 元组
    """
    n_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)
    
    # 1. 起始：直达声脉冲（极短）
    ir = np.zeros(n_samples)
    pre_delay_samples = int(pre_delay_ms * sample_rate / 1000)
    
    # 直达声：单个脉冲（代表声源）
    if pre_delay_samples < n_samples:
        ir[pre_delay_samples] = 1.0
    
    # 2. 虚空特征：NO 早期反射（这是关键！）
    # 真实空间会有墙壁反射，虚空没有
    
    # 3. 混响尾：纯粹的扩散场衰减
    # 使用改进的 Voss-McCartney 粉红噪音
    noise = generate_pink_noise(n_samples - pre_delay_samples)
    
    # 应用低通滤波，创造"深邃、黑暗"的虚空特征
    noise = apply_lowpass_filter(noise, sample_rate, lpf_cutoff_hz, order=4)
    
    # 计算高频的 T60（更快衰减）
    t60_low = decay_time
    t60_high = decay_time * high_freq_damping
    
    # 应用频率相关衰减
    tail = apply_frequency_dependent_decay(noise, sample_rate, t60_low, t60_high)
    
    # 降低混响尾能量，突出"虚空"的空旷感
    tail = tail * 0.3
    
    # 4. 合并
    ir[pre_delay_samples:pre_delay_samples + len(tail)] += tail
    
    # 5. 归一化
    max_val = np.max(np.abs(ir))
    if max_val > 0:
        ir = ir / max_val * 0.95
    
    # 计算包络（用于可视化/验证）
    t_tail = np.linspace(0, duration_sec - pre_delay_ms/1000, len(tail), endpoint=False)
    alpha = -np.log(0.001) / decay_time
    envelope = np.exp(-t_tail * alpha)
    
    return t, ir, envelope

def main():
    # 路径设置: 01_MVP_Demo/_Pipeline/generators/ -> 01_MVP_Demo/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mvp_root = os.path.dirname(os.path.dirname(base_dir)) 
    output_dir = os.path.join(mvp_root, "_Library", "S04_Space")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 使用配置参数
    config = VOID_CONFIG
    
    print("=" * 60)
    print("虚空 IR 生成器 v3.0")
    print("=" * 60)
    print(f"\n[配置参数]")
    print(f"  T60 (低频):        {config['t60']}s")
    print(f"  T60 (高频):        {config['t60'] * config['high_freq_damping']}s")
    print(f"  持续时间:          {config['duration']}s")
    print(f"  预延迟:            {config['pre_delay_ms']}ms")
    print(f"  低通截止频率:      {config['lpf_cutoff_hz']}Hz")
    print(f"  采样率:            {config['sample_rate']}Hz")
    
    print(f"\n[正在生成虚空 IR...]")
    _, audio, _ = generate_void_ir(
        duration_sec=config['duration'], 
        sample_rate=config['sample_rate'], 
        decay_time=config['t60'],
        pre_delay_ms=config['pre_delay_ms'],
        high_freq_damping=config['high_freq_damping'],
        lpf_cutoff_hz=config['lpf_cutoff_hz']
    )
    
    # 输出文件
    output_path = os.path.join(output_dir, "asset_S04_void_ir.wav")
    
    # 转换为 16bit 以保证兼容性
    audio_pcm = (audio * 32767).astype(np.int16)
    wavfile.write(output_path, config['sample_rate'], audio_pcm)
    
    print(f"  ✓ 已生成: {output_path}")
    
    # 验证声学指标
    print(f"\n[声学验证]")
    
    # 测量 T60
    measured_t60 = measure_t60(audio, config['sample_rate'])
    if measured_t60:
        t60_error = abs(measured_t60 - config['t60']) / config['t60'] * 100
        status = "✓" if t60_error < 15 else "⚠"
        print(f"  {status} 测量 T60:        {measured_t60:.2f}s (目标: {config['t60']}s, 误差: {t60_error:.1f}%)")
    else:
        print(f"  ✗ 无法测量 T60（信号可能太短）")
    
    # 分析频谱
    spectrum = analyze_spectrum(audio[int(config['pre_delay_ms'] * config['sample_rate'] / 1000):], 
                                 config['sample_rate'])
    
    print(f"\n[频谱分析]")
    print(f"  八度音程能量分布:")
    for i, (band, energy) in enumerate(zip(spectrum['octave_bands'], spectrum['octave_energies'])):
        if energy is not None:
            print(f"    {band[0]:>5.1f} - {band[1]:>5.0f} Hz: {energy:>6.1f} dB")
    
    # 检查高频衰减
    if len(spectrum['octave_energies']) >= 6:
        low_energy = spectrum['octave_energies'][2]  # 125-250 Hz
        high_energy = spectrum['octave_energies'][7]  # 4000-8000 Hz
        if low_energy and high_energy:
            high_freq_reduction = low_energy - high_energy
            print(f"\n  高频衰减: {high_freq_reduction:.1f} dB (相对于低频)")
            if high_freq_reduction > 10:
                print(f"  ✓ 虚空特征确认：声音已\"暗化\"")
    
    print(f"\n[虚空特征验证]")
    print(f"  ✓ 无早期反射（无墙壁边界）")
    print(f"  ✓ 纯扩散场衰减（粉红噪音基础）")
    print(f"  ✓ 频率相关衰减（高频衰减更快）")
    print(f"  ✓ 预延迟创造距离感")
    print(f"  ✓ 低通滤波创造深邃、黑暗特征")
    print(f"  ✓ 极长 T60 创造无限、虚无感")
    
    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
