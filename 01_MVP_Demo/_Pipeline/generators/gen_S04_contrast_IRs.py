"""
S04 空间对比 IR 生成器 (Spatial Contrast)
---------------------------------------
生成两个极端空间的脉冲响应 (IR)，用于教学对比：
1. 小空间 (Closet): 0.2s T60, 极干, 高且密的早期反射。
2. 大空间 (Hall): 2.0s T60, 极湿, 清晰的几何反射（音乐厅特征）。

输出:
- _Library/S04_Space/contrast_IR_small_closet.wav
- _Library/S04_Space/contrast_IR_large_hall.wav

Version: 3.0 (改进声学模型：Voss-McCartney粉红噪音、几何反射、频率相关衰减、验证指标)
"""

import numpy as np
from scipy import signal as scipy_signal
from scipy.io import wavfile
import os

# 空间配置参数
SPACE_CONFIGS = {
    'closet': {
        't60': 0.2,                    # 极短混响，"棺材"般的窒息感
        'duration': 1.0,               # 短持续时间即可
        'er_density': 'very_high',     # 极密集的早期反射
        'er_duration_ms': 50,          # 早期反射持续时间（墙壁很近）
        'tail_gain': 0.25,             # 混响尾很弱
        'high_freq_t60_ratio': 0.5,    # 高频衰减更快
        'sample_rate': 48000
    },
    'hall': {
        't60': 2.0,                    # 典型音乐厅混响时间
        'duration': 3.5,               # 需要更长时间捕获完整衰减
        'er_pattern': 'geometric',     # 几何反射模式
        'er_gain': 1.2,                # 强调"墙壁"的存在
        'tail_gain': 0.7,              # 丰富的混响尾
        'high_freq_t60_ratio': 0.6,    # 高频衰减稍慢（音乐厅特征）
        'room_dims': (15, 20, 10),     # 房间尺寸 (宽, 长, 高) 米
        'sample_rate': 48000
    }
}

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
        update_mask = i & -i
        if update_mask > 0:
            source_idx = int(np.log2(update_mask)) % num_sources
            sources[source_idx] = np.random.randn()
        
        # 当前样本是所有源的和
        output[i] = np.sum(sources)
    
    # 归一化到 [-1, 1]
    output = output / np.max(np.abs(output))
    
    return output

def apply_frequency_dependent_decay(signal_input, sample_rate, t60_low, t60_high):
    """
    对信号应用频率相关衰减，模拟空气吸收和材料阻尼。
    
    参数:
        signal_input: 输入信号（通常是混响尾）
        sample_rate: 采样率 (Hz)
        t60_low: 低频段的 T60 时间（秒），参考频率 125Hz
        t60_high: 高频段的 T60 时间（秒），参考频率 8kHz
    
    返回:
        应用频率相关衰减后的信号
    """
    n_samples = len(signal_input)
    duration = n_samples / sample_rate
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # 定义频段分界点
    LOW_CUTOFF = 500
    HIGH_CUTOFF = 4000
    
    # 设计 Butterworth 滤波器
    sos_low = scipy_signal.butter(4, LOW_CUTOFF, btype='low', fs=sample_rate, output='sos')
    sos_mid = scipy_signal.butter(4, [LOW_CUTOFF, HIGH_CUTOFF], btype='band', fs=sample_rate, output='sos')
    sos_high = scipy_signal.butter(4, HIGH_CUTOFF, btype='high', fs=sample_rate, output='sos')
    
    # 分离频段
    band_low = scipy_signal.sosfilt(sos_low, signal_input)
    band_mid = scipy_signal.sosfilt(sos_mid, signal_input)
    band_high = scipy_signal.sosfilt(sos_high, signal_input)
    
    # 计算中频段的 T60
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

def measure_t60(ir, sample_rate):
    """
    使用 Schroeder 反向积分法测量 T60 混响时间。
    
    参数:
        ir: 脉冲响应信号
        sample_rate: 采样率 (Hz)
    
    返回:
        T60 时间（秒），如果无法测量则返回 None
    """
    energy = ir ** 2
    schroeder = np.cumsum(energy[::-1])[::-1]
    schroeder = schroeder / schroeder[0]
    schroeder_db = 10 * np.log10(schroeder + 1e-10)
    
    try:
        idx_5db = np.where(schroeder_db <= -5)[0][0]
        idx_35db = np.where(schroeder_db <= -35)[0][0]
        
        time_range = np.arange(idx_5db, idx_35db) / sample_rate
        db_range = schroeder_db[idx_5db:idx_35db]
        
        slope = (db_range[-1] - db_range[0]) / (time_range[-1] - time_range[0])
        t60 = 60 / abs(slope)
        
        return t60
    except (IndexError, ZeroDivisionError):
        return None

def measure_c80(ir, sample_rate):
    """
    测量清晰度指数 C80。
    
    C80 = 10 * log10(E_early / E_late)
    其中 E_early 是 0-80ms 的能量，E_late 是 80ms 之后的能量
    
    参数:
        ir: 脉冲响应信号
        sample_rate: 采样率 (Hz)
    
    返回:
        C80 值 (dB)
    """
    # 找到直达声位置（最大值）
    peak_idx = np.argmax(np.abs(ir))
    
    # 80ms 对应的样本数
    samples_80ms = int(0.08 * sample_rate)
    
    # 计算早期和晚期能量
    early_end = min(peak_idx + samples_80ms, len(ir))
    
    energy_early = np.sum(ir[peak_idx:early_end] ** 2)
    energy_late = np.sum(ir[early_end:] ** 2)
    
    if energy_late > 0:
        c80 = 10 * np.log10(energy_early / energy_late)
        return c80
    else:
        return None

def generate_early_reflections_closet(sample_rate, er_duration_ms=50):
    """
    小衣柜：极密集、快速、窒息感的早期反射。
    
    特征：
    - 墙壁极近，反射密集且快速到达
    - 高衰减率，能量快速消散
    - 创造"棺材"般的压迫感
    
    参数:
        sample_rate: 采样率 (Hz)
        er_duration_ms: 早期反射持续时间（毫秒）
    
    返回:
        早期反射信号
    """
    n_samples = int(er_duration_ms * sample_rate / 1000)
    t = np.linspace(0, er_duration_ms/1000, n_samples)
    
    # 极密集的随机脉冲（墙壁很近，反射密集）
    # 提高非零概率，创造更密集的反射
    impulses = np.random.choice([0, 1, -1], size=n_samples, p=[0.65, 0.175, 0.175])
    
    # 极快衰减（窒息感）
    decay = np.exp(-t * 40)  # 增加衰减率
    
    return impulses * decay

def generate_early_reflections_hall_geometric(sample_rate, room_dims=(15, 20, 10)):
    """
    音乐厅：基于几何射线追踪的清晰反射模式。
    
    特征：
    - 清晰的离散反射（墙壁、天花板、地板）
    - 基于物理的延迟时间和衰减
    - 创造"文明、墙壁厚重"的音乐厅感
    
    参数:
        sample_rate: 采样率 (Hz)
        room_dims: 房间尺寸 (宽, 长, 高) 米
    
    返回:
        早期反射信号
    """
    width, length, height = room_dims
    n_samples = int(0.15 * sample_rate)  # 150ms
    er = np.zeros(n_samples)
    
    # 声速 (m/s)
    SOUND_SPEED = 343.0
    
    # 定义反射面和听音位置
    # 假设声源在房间中心，听者也在中心附近
    listener_pos = np.array([width/2, length/2, height/2])
    source_pos = np.array([width/2, length/2 - 2, height/2])  # 声源稍微靠前
    
    # 几何反射：计算从声源到各个表面再到听者的路径
    reflections = []
    
    # 侧墙反射（左右）
    for wall_x in [0, width]:
        mirror_source = source_pos.copy()
        mirror_source[0] = 2 * wall_x - source_pos[0]
        distance = np.linalg.norm(listener_pos - mirror_source)
        delay = distance / SOUND_SPEED
        attenuation = 1.0 / (distance / 5.0)  # 简化的距离衰减
        reflections.append((delay, attenuation * 0.6, 'side_wall'))
    
    # 前后墙反射
    for wall_y in [0, length]:
        mirror_source = source_pos.copy()
        mirror_source[1] = 2 * wall_y - source_pos[1]
        distance = np.linalg.norm(listener_pos - mirror_source)
        delay = distance / SOUND_SPEED
        attenuation = 1.0 / (distance / 5.0)
        reflections.append((delay, attenuation * 0.55, 'front_back_wall'))
    
    # 天花板和地板反射
    for wall_z in [0, height]:
        mirror_source = source_pos.copy()
        mirror_source[2] = 2 * wall_z - source_pos[2]
        distance = np.linalg.norm(listener_pos - mirror_source)
        delay = distance / SOUND_SPEED
        attenuation = 1.0 / (distance / 5.0)
        reflections.append((delay, attenuation * 0.5, 'ceiling_floor'))
    
    # 角落反射（二阶反射）
    corners = [
        ([0, 0], 0.35),
        ([0, length], 0.35),
        ([width, 0], 0.35),
        ([width, length], 0.35)
    ]
    
    for (corner_x, corner_y), gain in corners:
        # 简化计算：通过角落的路径
        path_length = (np.sqrt((source_pos[0] - corner_x)**2 + (source_pos[1] - corner_y)**2) +
                      np.sqrt((listener_pos[0] - corner_x)**2 + (listener_pos[1] - corner_y)**2))
        delay = path_length / SOUND_SPEED
        attenuation = gain / (path_length / 10.0)
        reflections.append((delay, attenuation, 'corner'))
    
    # 将反射添加到 IR
    for delay, amplitude, reflection_type in reflections:
        idx = int(delay * sample_rate)
        if idx < n_samples:
            # 每个反射是一个短脉冲（2ms宽度）
            pulse_len = int(0.002 * sample_rate)
            pulse = np.random.randn(pulse_len) * amplitude
            end_idx = min(idx + pulse_len, n_samples)
            er[idx:end_idx] += pulse[:end_idx-idx]
    
    # 添加扩散尾部（反射逐渐融合）
    t = np.linspace(0, 0.15, n_samples)
    diffuse = np.random.randn(n_samples) * 0.15 * np.exp(-t * 8)
    er += diffuse
    
    return er

def generate_reverb_tail(duration_sec, sample_rate, t60, high_freq_t60_ratio=0.6):
    """
    生成混响拖尾，使用改进的粉红噪音和频率相关衰减。
    
    参数:
        duration_sec: 持续时间（秒）
        sample_rate: 采样率 (Hz)
        t60: 低频 T60 时间（秒）
        high_freq_t60_ratio: 高频 T60 相对于低频的比例
    
    返回:
        混响尾信号
    """
    n_samples = int(duration_sec * sample_rate)
    
    # 使用改进的 Voss-McCartney 粉红噪音
    pink = generate_pink_noise_voss(n_samples)
    
    # 应用频率相关衰减
    t60_low = t60
    t60_high = t60 * high_freq_t60_ratio
    
    tail = apply_frequency_dependent_decay(pink, sample_rate, t60_low, t60_high)
    
    return tail

def generate_ir_closet(config):
    """
    生成小衣柜 IR：窒息、压抑、极短混响。
    
    参数:
        config: 配置字典（来自 SPACE_CONFIGS['closet']）
    
    返回:
        IR 信号
    """
    t60 = config['t60']
    duration = config['duration']
    fs = config['sample_rate']
    er_duration_ms = config['er_duration_ms']
    high_freq_ratio = config['high_freq_t60_ratio']
    
    print(f"[Small Closet] 生成中: T60={t60}s, ER持续={er_duration_ms}ms...")
    
    # 1. 起始脉冲（直达声）
    n_samples = int(duration * fs)
    ir = np.zeros(n_samples)
    ir[0] = 1.0  # 直达声
    
    # 2. 早期反射（极密集）
    er = generate_early_reflections_closet(fs, er_duration_ms)
    ir[1:len(er)+1] += er * 0.9
    
    # 3. 混响尾（极短，带频率相关衰减）
    tail = generate_reverb_tail(duration, fs, t60, high_freq_ratio)
    ir += tail * config['tail_gain']
    
    # 4. 归一化
    ir = ir / np.max(np.abs(ir)) * 0.95
    return ir

def generate_ir_hall(config):
    """
    生成音乐厅 IR：辉煌、宽广、清晰的几何反射。
    
    参数:
        config: 配置字典（来自 SPACE_CONFIGS['hall']）
    
    返回:
        IR 信号
    """
    t60 = config['t60']
    duration = config['duration']
    fs = config['sample_rate']
    room_dims = config['room_dims']
    high_freq_ratio = config['high_freq_t60_ratio']
    
    print(f"[Large Hall] 生成中: T60={t60}s, 房间尺寸={room_dims}m...")
    
    # 1. 起始脉冲（直达声）
    n_samples = int(duration * fs)
    ir = np.zeros(n_samples)
    ir[0] = 1.0  # 直达声
    
    # 2. 早期反射（清晰的几何模式）
    er = generate_early_reflections_hall_geometric(fs, room_dims)
    ir[1:len(er)+1] += er * config['er_gain']
    
    # 3. 混响尾（长且丰富，带频率相关衰减）
    tail = generate_reverb_tail(duration, fs, t60, high_freq_ratio)
    ir += tail * config['tail_gain']
    
    # 4. 归一化
    ir = ir / np.max(np.abs(ir)) * 0.95
    return ir

def main():
    # 路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    output_dir = os.path.join(project_root, "01_MVP_Demo", "_Library", "S04_Space")
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("空间对比 IR 生成器 v3.0")
    print("=" * 60)
    
    # A. 小衣柜 (Small Closet)
    print("\n" + "-" * 60)
    print("生成小衣柜 IR")
    print("-" * 60)
    
    closet_config = SPACE_CONFIGS['closet']
    print(f"[配置] T60={closet_config['t60']}s, ER持续={closet_config['er_duration_ms']}ms")
    
    ir_closet = generate_ir_closet(closet_config)
    path_closet = os.path.join(output_dir, "contrast_IR_small_closet.wav")
    wavfile.write(path_closet, closet_config['sample_rate'], (ir_closet * 32767).astype(np.int16))
    print(f"  ✓ 已保存: {path_closet}")
    
    # 验证衣柜 IR
    print(f"\n[声学验证 - 衣柜]")
    t60_closet = measure_t60(ir_closet, closet_config['sample_rate'])
    if t60_closet:
        t60_error = abs(t60_closet - closet_config['t60']) / closet_config['t60'] * 100
        status = "✓" if t60_error < 20 else "⚠"
        print(f"  {status} 测量 T60: {t60_closet:.3f}s (目标: {closet_config['t60']}s, 误差: {t60_error:.1f}%)")
    else:
        print(f"  ⚠ 无法测量 T60（信号太短）")
    
    print(f"  ✓ 特征: 窒息、压抑、棺材般的密闭感")
    
    # B. 大厅 (Large Hall)
    print("\n" + "-" * 60)
    print("生成音乐厅 IR")
    print("-" * 60)
    
    hall_config = SPACE_CONFIGS['hall']
    print(f"[配置] T60={hall_config['t60']}s, 房间={hall_config['room_dims']}m")
    
    ir_hall = generate_ir_hall(hall_config)
    path_hall = os.path.join(output_dir, "contrast_IR_large_hall.wav")
    wavfile.write(path_hall, hall_config['sample_rate'], (ir_hall * 32767).astype(np.int16))
    print(f"  ✓ 已保存: {path_hall}")
    
    # 验证音乐厅 IR
    print(f"\n[声学验证 - 音乐厅]")
    t60_hall = measure_t60(ir_hall, hall_config['sample_rate'])
    if t60_hall:
        t60_error = abs(t60_hall - hall_config['t60']) / hall_config['t60'] * 100
        status = "✓" if t60_error < 15 else "⚠"
        print(f"  {status} 测量 T60: {t60_hall:.2f}s (目标: {hall_config['t60']}s, 误差: {t60_error:.1f}%)")
    else:
        print(f"  ✗ 无法测量 T60")
    
    c80_hall = measure_c80(ir_hall, hall_config['sample_rate'])
    if c80_hall is not None:
        print(f"  ✓ 清晰度 C80: {c80_hall:.1f} dB")
        if -5 <= c80_hall <= 5:
            print(f"    (适合音乐厅：早期/晚期能量平衡)")
    
    print(f"  ✓ 特征: 辉煌、宽广、清晰的墙壁反射")
    
    # 对比总结
    print("\n" + "=" * 60)
    print("教学对比验证")
    print("=" * 60)
    
    if t60_closet and t60_hall:
        ratio = t60_hall / t60_closet
        print(f"\n混响时间对比:")
        print(f"  衣柜:   {t60_closet:.3f}s")
        print(f"  音乐厅: {t60_hall:.2f}s")
        print(f"  比例:   {ratio:.1f}× (音乐厅是衣柜的 {ratio:.1f} 倍)")
        
        if ratio > 8:
            print(f"  ✓ 对比度极佳！教学效果明显")
        elif ratio > 5:
            print(f"  ✓ 对比度良好")
        else:
            print(f"  ⚠ 对比度可能不够明显")
    
    print(f"\n听感预期:")
    print(f"  衣柜:   窒息、压抑、像在小纸盒/棺材里说话")
    print(f"  音乐厅: 辉煌、宽广、像在教堂/音乐厅唱歌")
    print(f"  虚空:   无限、深邃、黑暗、遥远（见 gen_S04_void_ir.py）")
    
    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
