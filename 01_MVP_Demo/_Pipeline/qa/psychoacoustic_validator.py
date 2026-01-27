"""
心理声学验证器
==============

验证音频的心理声学设计是否达到预期效果。

核心功能:
- 心跳生物拟真性检测（sine_sweep、低通滤波）
- 威胁音频检测（3000Hz、尖锐包络）
- 空间分离验证（内/外声像分离）
- 感知影响评估（明亮度、黑暗度、焦虑值）
"""

import numpy as np
from scipy import signal as scipy_signal
from typing import Dict, Optional, Tuple
import soundfile as sf

# 处理相对导入和绝对导入
try:
    from .config import PSYCHOACOUSTIC_FREQUENCIES
    from .audio_analyzer import AudioAnalyzer
except ImportError:
    from config import PSYCHOACOUSTIC_FREQUENCIES
    from audio_analyzer import AudioAnalyzer


class PsychoacousticValidator:
    """
    心理声学验证器
    
    验证音频的心理声学设计是否达到预期效果。
    
    属性:
        analyzer: AudioAnalyzer 实例
        audio: 音频数据
        sample_rate: 采样率
    """
    
    def __init__(self, audio_path: Optional[str] = None,
                 audio_data: Optional[np.ndarray] = None,
                 sample_rate: int = 48000):
        """
        初始化心理声学验证器
        
        参数:
            audio_path: 音频文件路径（可选）
            audio_data: 音频数据数组（可选）
            sample_rate: 采样率（如果提供audio_data，必须指定）
        """
        # 创建 AudioAnalyzer 实例
        self.analyzer = AudioAnalyzer(
            audio_path=audio_path,
            audio_data=audio_data,
            sample_rate=sample_rate
        )
        
        self.audio = self.analyzer.audio
        self.sample_rate = self.analyzer.sample_rate
    
    # ========================================================================
    # 心跳生物拟真性检测
    # ========================================================================
    
    def validate_heartbeat_biofidelity(self) -> Dict[str, any]:
        """
        验证心跳的生物拟真性
        
        检测内容:
        1. 是否使用 sine_sweep 模拟肌肉收缩（检测频率扫描特征）
        2. 是否应用低通滤波器模拟骨传导（检测高频衰减 > 20dB @ 500Hz）
        
        返回:
            字典，包含验证结果
        """
        result = {
            'has_sine_sweep': False,
            'sine_sweep_confidence': 0.0,
            'has_lowpass_filter': False,
            'high_freq_attenuation_db': 0.0,
            'biofidelity_score': 0.0,
            'issues': []
        }
        
        # 检测 sine_sweep 特征
        has_sweep, confidence = self._detect_sine_sweep()
        result['has_sine_sweep'] = has_sweep
        result['sine_sweep_confidence'] = confidence
        
        if not has_sweep:
            result['issues'].append(
                "未检测到 sine_sweep 特征（频率扫描），"
                "心跳可能缺乏 Lub-Dub 的肌肉收缩感"
            )
        
        # 检测低通滤波
        has_lpf, attenuation = self._detect_lowpass_filter()
        result['has_lowpass_filter'] = has_lpf
        result['high_freq_attenuation_db'] = attenuation
        
        if not has_lpf:
            result['issues'].append(
                f"高频衰减不足（{attenuation:.1f}dB @ 500Hz），"
                f"心跳可能听起来太明亮，缺乏骨传导的沉闷感"
            )
        
        # 计算生物拟真性得分
        score = 0.0
        if has_sweep:
            score += 0.5 * confidence
        if has_lpf:
            score += 0.5 * min(attenuation / 20.0, 1.0)
        
        result['biofidelity_score'] = score
        
        return result
    
    def _detect_sine_sweep(self) -> Tuple[bool, float]:
        """
        检测 sine_sweep 特征（频率扫描）
        
        策略:
        1. 计算瞬时频率
        2. 检测频率是否随时间变化（扫描）
        
        返回:
            (是否检测到, 置信度) 元组
        """
        # 如果是立体声，使用单声道混音
        if len(self.audio.shape) > 1:
            audio = np.mean(self.audio, axis=1)
        else:
            audio = self.audio
        
        # 计算解析信号（Hilbert 变换）
        analytic_signal = scipy_signal.hilbert(audio)
        
        # 计算瞬时相位
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        
        # 计算瞬时频率
        instantaneous_frequency = np.diff(instantaneous_phase) / (2.0 * np.pi) * self.sample_rate
        
        # 检测频率变化
        # 如果频率在一段时间内持续变化，认为是 sweep
        window_size = int(0.05 * self.sample_rate)  # 50ms 窗口
        
        if len(instantaneous_frequency) < window_size:
            return False, 0.0
        
        # 计算频率变化率
        freq_changes = []
        for i in range(0, len(instantaneous_frequency) - window_size, window_size):
            window = instantaneous_frequency[i:i+window_size]
            # 计算线性趋势
            trend = np.polyfit(np.arange(len(window)), window, 1)[0]
            freq_changes.append(abs(trend))
        
        # 如果有显著的频率变化，认为是 sweep
        avg_change = np.mean(freq_changes)
        
        # 阈值：平均变化率 > 10 Hz/sample
        has_sweep = avg_change > 10
        confidence = min(avg_change / 100.0, 1.0)  # 归一化到 [0, 1]
        
        return has_sweep, confidence
    
    def _detect_lowpass_filter(self, cutoff_hz: float = 500, threshold_db: float = 20) -> Tuple[bool, float]:
        """
        检测低通滤波器（高频衰减）
        
        参数:
            cutoff_hz: 截止频率（Hz）
            threshold_db: 衰减阈值（dB）
        
        返回:
            (是否检测到, 衰减量) 元组
        """
        # 计算频谱
        frequencies, psd = self.analyzer.compute_psd()
        
        # 转换为 dB
        psd_db = 10 * np.log10(psd + 1e-10)
        
        # 计算低频能量（< cutoff_hz）
        low_freq_mask = frequencies < cutoff_hz
        if not np.any(low_freq_mask):
            return False, 0.0
        
        low_freq_energy = np.mean(psd_db[low_freq_mask])
        
        # 计算高频能量（> cutoff_hz）
        high_freq_mask = frequencies > cutoff_hz
        if not np.any(high_freq_mask):
            return False, 0.0
        
        high_freq_energy = np.mean(psd_db[high_freq_mask])
        
        # 计算衰减量
        attenuation = low_freq_energy - high_freq_energy
        
        # 判断是否满足阈值
        has_lpf = attenuation >= threshold_db
        
        return has_lpf, attenuation
    
    # ========================================================================
    # 威胁音频检测
    # ========================================================================
    
    def validate_threat_audio(self) -> Dict[str, any]:
        """
        验证威胁音频的心理效果
        
        检测内容:
        1. 是否包含 3000Hz 频率成分（婴儿哭声敏感频率）
        2. 包络曲线是否使用高次幂（尖锐突袭感）
        
        返回:
            字典，包含验证结果
        """
        result = {
            'has_threat_frequency': False,
            'threat_frequency_energy_db': 0.0,
            'has_sharp_envelope': False,
            'envelope_sharpness': 0.0,
            'threat_score': 0.0,
            'issues': []
        }
        
        # 检测 3000Hz 频率成分
        has_freq, energy = self._detect_threat_frequency()
        result['has_threat_frequency'] = has_freq
        result['threat_frequency_energy_db'] = energy
        
        if not has_freq:
            result['issues'].append(
                f"未检测到 3000Hz 威胁频率成分（能量: {energy:.1f}dB），"
                f"音频可能缺乏心理威胁感"
            )
        
        # 检测尖锐包络
        has_sharp, sharpness = self._detect_sharp_envelope()
        result['has_sharp_envelope'] = has_sharp
        result['envelope_sharpness'] = sharpness
        
        if not has_sharp:
            result['issues'].append(
                f"包络曲线不够尖锐（锐度: {sharpness:.2f}），"
                f"可能缺乏突袭感，听起来更像背景音而非威胁"
            )
        
        # 计算威胁得分
        score = 0.0
        if has_freq:
            score += 0.5
        if has_sharp:
            score += 0.5 * sharpness
        
        result['threat_score'] = score
        
        return result
    
    def _detect_threat_frequency(self, target_hz: float = 3000, tolerance_hz: float = 200) -> Tuple[bool, float]:
        """
        检测威胁频率（3000Hz）
        
        参数:
            target_hz: 目标频率（Hz）
            tolerance_hz: 容差（Hz）
        
        返回:
            (是否检测到, 能量) 元组
        """
        # 使用配置中的威胁频率
        target_hz = PSYCHOACOUSTIC_FREQUENCIES['threat']
        
        # 计算频谱
        frequencies, psd = self.analyzer.compute_psd()
        
        # 转换为 dB
        psd_db = 10 * np.log10(psd + 1e-10)
        
        # 查找目标频率范围内的能量
        mask = (frequencies >= target_hz - tolerance_hz) & (frequencies <= target_hz + tolerance_hz)
        
        if not np.any(mask):
            return False, -np.inf
        
        threat_energy = np.max(psd_db[mask])
        
        # 计算总能量
        total_energy = np.mean(psd_db)
        
        # 如果威胁频率能量显著高于平均（> 10dB），认为检测到
        has_threat = (threat_energy - total_energy) > 10
        
        return has_threat, threat_energy
    
    def _detect_sharp_envelope(self) -> Tuple[bool, float]:
        """
        检测尖锐包络（高次幂特征）
        
        策略:
        1. 计算包络曲线
        2. 分析包络的峰度（kurtosis）
        3. 高峰度表示尖锐突袭
        
        返回:
            (是否检测到, 锐度) 元组
        """
        # 如果是立体声，使用单声道混音
        if len(self.audio.shape) > 1:
            audio = np.mean(self.audio, axis=1)
        else:
            audio = self.audio
        
        # 计算包络（Hilbert 变换）
        analytic_signal = scipy_signal.hilbert(audio)
        envelope = np.abs(analytic_signal)
        
        # 平滑包络
        window_size = int(0.01 * self.sample_rate)  # 10ms 窗口
        if window_size > 0:
            envelope = np.convolve(envelope, np.ones(window_size)/window_size, mode='same')
        
        # 计算峰度（kurtosis）
        # 峰度 > 3 表示尖锐分布（高次幂特征）
        from scipy.stats import kurtosis
        envelope_kurtosis = kurtosis(envelope)
        
        # 归一化锐度到 [0, 1]
        sharpness = min(max(envelope_kurtosis / 10.0, 0.0), 1.0)
        
        # 如果峰度 > 3，认为是尖锐包络
        has_sharp = envelope_kurtosis > 3
        
        return has_sharp, sharpness
    
    # ========================================================================
    # 空间分离验证
    # ========================================================================
    
    def validate_spatial_separation(self, inner_track_path: str, outer_track_path: str) -> Dict[str, any]:
        """
        验证"内"（心跳）与"外"（虚空）的声像分离
        
        参数:
            inner_track_path: 内部轨道（心跳）文件路径
            outer_track_path: 外部轨道（虚空 IR）文件路径
        
        返回:
            字典，包含验证结果
        """
        result = {
            'inner_correlation': 0.0,
            'outer_correlation': 0.0,
            'separation_degree': 0.0,
            'is_separated': False,
            'issues': []
        }
        
        # 分析内部轨道
        inner_analyzer = AudioAnalyzer(audio_path=inner_track_path)
        inner_corr = inner_analyzer.compute_stereo_correlation()
        
        if inner_corr is None:
            result['issues'].append("内部轨道不是立体声，无法计算相关性")
            return result
        
        result['inner_correlation'] = inner_corr
        
        # 分析外部轨道
        outer_analyzer = AudioAnalyzer(audio_path=outer_track_path)
        outer_corr = outer_analyzer.compute_stereo_correlation()
        
        if outer_corr is None:
            result['issues'].append("外部轨道不是立体声，无法计算相关性")
            return result
        
        result['outer_correlation'] = outer_corr
        
        # 计算分离度
        separation = abs(inner_corr - outer_corr)
        result['separation_degree'] = separation
        
        # 验证分离度
        # 内部应该 > 0.95（居中），外部应该 < 0.5（宽立体声）
        inner_ok = inner_corr > 0.95
        outer_ok = outer_corr < 0.5
        separation_ok = separation > 0.4
        
        result['is_separated'] = inner_ok and outer_ok and separation_ok
        
        if not inner_ok:
            result['issues'].append(
                f"内部轨道（心跳）立体声相关性 {inner_corr:.2f} 不够高，"
                f"应该 > 0.95（居中定位）"
            )
        
        if not outer_ok:
            result['issues'].append(
                f"外部轨道（虚空）立体声相关性 {outer_corr:.2f} 不够低，"
                f"应该 < 0.5（宽立体声）"
            )
        
        if not separation_ok:
            result['issues'].append(
                f"声像分离度 {separation:.2f} 不足，"
                f"应该 > 0.4（清晰的内/外分离）"
            )
        
        return result
    
    # ========================================================================
    # 感知影响评估
    # ========================================================================
    
    def assess_perceptual_impact(self) -> Dict[str, any]:
        """
        评估感知影响（明亮度、黑暗度、焦虑值）
        
        返回:
            字典，包含评估结果
        """
        result = {
            'brightness': 0.0,  # 0-1，0=黑暗，1=明亮
            'darkness': 0.0,    # 0-1，0=明亮，1=黑暗
            'anxiety_level': 0.0,  # 0-1，0=平静，1=焦虑
            'perceptual_description': ""
        }
        
        # 计算明亮度（基于频谱质心）
        centroid = self.analyzer.compute_spectral_centroid()
        
        # 归一化到 [0, 1]
        # 假设 20Hz = 0（最暗），20000Hz = 1（最亮）
        brightness = (centroid - 20) / (20000 - 20)
        brightness = max(0.0, min(1.0, brightness))
        
        result['brightness'] = brightness
        result['darkness'] = 1.0 - brightness
        
        # 计算焦虑值（基于多个因素）
        anxiety = 0.0
        
        # 因素1：威胁频率（3000Hz）
        threat_result = self.validate_threat_audio()
        if threat_result['has_threat_frequency']:
            anxiety += 0.3
        
        # 因素2：尖锐包络
        if threat_result['has_sharp_envelope']:
            anxiety += 0.3 * threat_result['envelope_sharpness']
        
        # 因素3：高频能量（明亮的声音更焦虑）
        if brightness > 0.6:
            anxiety += 0.2 * brightness
        
        # 因素4：动态范围（大动态更焦虑）
        peak = self.analyzer.compute_peak_amplitude()
        rms_db = self.analyzer.compute_rms_energy()
        rms_linear = 10 ** (rms_db / 20)
        if rms_linear > 0:
            dynamic_range = peak / rms_linear
            anxiety += 0.2 * min(dynamic_range / 10.0, 1.0)
        
        result['anxiety_level'] = min(anxiety, 1.0)
        
        # 生成感知描述
        if result['darkness'] > 0.7:
            darkness_desc = "深邃、黑暗"
        elif result['darkness'] > 0.4:
            darkness_desc = "中性"
        else:
            darkness_desc = "明亮"
        
        if result['anxiety_level'] > 0.7:
            anxiety_desc = "高度焦虑、威胁感强"
        elif result['anxiety_level'] > 0.4:
            anxiety_desc = "中度焦虑"
        else:
            anxiety_desc = "平静"
        
        result['perceptual_description'] = f"{darkness_desc}，{anxiety_desc}"
        
        return result
