"""
音频分析引擎
============

分析音频文件的声学特性、频谱特征和立体声成像。

核心功能:
- 声学指标测量（T60, C80, EDT）
- 立体声分析（相关系数、宽度、声像位置）
- 频谱分析（PSD, 频谱质心、八度频段能量）
- 伪影检测（削波、直流偏移、不连续性、混叠）
"""

import numpy as np
from scipy import signal as scipy_signal
from scipy.io import wavfile
import soundfile as sf
from typing import Optional, Dict, List, Tuple, Union
import os

# 处理相对导入和绝对导入
try:
    from .config import (
        AcousticMetrics,
        SpectralAnalysis,
        ArtifactReport,
        QAError,
        OCTAVE_BANDS,
        ARTIFACT_THRESHOLDS,
        STEREO_CORRELATION_THRESHOLDS
    )
except ImportError:
    from config import (
        AcousticMetrics,
        SpectralAnalysis,
        ArtifactReport,
        QAError,
        OCTAVE_BANDS,
        ARTIFACT_THRESHOLDS,
        STEREO_CORRELATION_THRESHOLDS
    )


class AudioAnalyzer:
    """
    音频分析引擎
    
    分析音频文件的声学特性、频谱特征和立体声成像。
    
    属性:
        audio: 音频数据（numpy数组）
        sample_rate: 采样率（Hz）
        is_stereo: 是否为立体声
        duration: 音频时长（秒）
    """
    
    def __init__(self, audio_path: Optional[str] = None, 
                 audio_data: Optional[np.ndarray] = None,
                 sample_rate: int = 48000):
        """
        初始化音频分析器
        
        参数:
            audio_path: 音频文件路径（可选）
            audio_data: 音频数据数组（可选）
            sample_rate: 采样率（如果提供audio_data，必须指定）
        
        注意: audio_path 和 audio_data 必须提供其中一个
        """
        if audio_path is None and audio_data is None:
            raise ValueError("必须提供 audio_path 或 audio_data")
        
        if audio_path is not None:
            self.audio_path = audio_path
            self.audio, self.sample_rate = self._load_audio(audio_path)
        else:
            self.audio_path = None
            self.audio = audio_data
            self.sample_rate = sample_rate
        
        # 验证音频不为空
        if self.audio is None or len(self.audio) == 0:
            raise ValueError("音频数据为空")
        
        # 确保音频是浮点数格式 [-1, 1]
        if self.audio.dtype != np.float32 and self.audio.dtype != np.float64:
            self.audio = self.audio.astype(np.float64) / np.max(np.abs(self.audio))
        
        # 检测立体声
        self.is_stereo = len(self.audio.shape) > 1 and self.audio.shape[1] == 2
        
        # 计算时长
        self.duration = len(self.audio) / self.sample_rate
    
    def _load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """
        加载音频文件
        
        参数:
            audio_path: 音频文件路径
        
        返回:
            (音频数据, 采样率) 元组
        
        异常:
            QAError: 文件不存在或格式错误
        """
        if not os.path.exists(audio_path):
            raise QAError(
                error_type="file_not_found",
                severity="critical",
                message=f"音频文件不存在: {audio_path}",
                location=audio_path,
                suggestion="请检查文件路径是否正确"
            )
        
        try:
            # 尝试使用 soundfile 加载（支持更多格式）
            audio, sample_rate = sf.read(audio_path, dtype='float64')
            return audio, sample_rate
        except Exception as e:
            try:
                # 回退到 scipy.io.wavfile
                sample_rate, audio = wavfile.read(audio_path)
                # 转换为浮点数
                if audio.dtype == np.int16:
                    audio = audio.astype(np.float64) / 32768.0
                elif audio.dtype == np.int32:
                    audio = audio.astype(np.float64) / 2147483648.0
                return audio, sample_rate
            except Exception as e2:
                raise QAError(
                    error_type="format_error",
                    severity="critical",
                    message=f"无法加载音频文件: {str(e2)}",
                    location=audio_path,
                    suggestion="请确保文件是有效的音频格式（WAV, FLAC, OGG等）"
                )
    
    # ========================================================================
    # 声学指标测量
    # ========================================================================
    
    def measure_t60(self, verbose: bool = False) -> Optional[float]:
        """
        使用 Schroeder 反向积分法测量 T60 混响时间
        
        T60 定义：声音衰减 60dB 所需的时间
        
        参数:
            verbose: 是否输出详细验证信息
        
        返回:
            T60 时间（秒），如果无法测量则返回 None
        
        参考: 复用自 gen_S04_void_ir.py 和 gen_S04_contrast_IRs.py
        
        验证: 需求 4.1, 4.2
        """
        try:
            # 如果是立体声，使用单声道混音
            if self.is_stereo:
                audio = np.mean(self.audio, axis=1)
            else:
                audio = self.audio
            
            # 计算能量包络（平方）
            energy = audio ** 2
            
            # Schroeder 反向积分
            schroeder = np.cumsum(energy[::-1])[::-1]
            
            # 避免除零
            if schroeder[0] == 0:
                if verbose:
                    print("[T60 测量] 错误: 信号能量为零")
                return None
            
            schroeder = schroeder / schroeder[0]  # 归一化
            
            # 转换为 dB
            schroeder_db = 10 * np.log10(schroeder + 1e-10)  # 避免 log(0)
            
            # 找到 -5dB 和 -35dB 的位置（使用 -5 到 -35 dB 范围来估算 T60）
            idx_5db_candidates = np.where(schroeder_db <= -5)[0]
            idx_35db_candidates = np.where(schroeder_db <= -35)[0]
            
            if len(idx_5db_candidates) == 0:
                if verbose:
                    print("[T60 测量] 错误: 信号未衰减到 -5dB")
                return None
            
            if len(idx_35db_candidates) == 0:
                if verbose:
                    print("[T60 测量] 错误: 信号未衰减到 -35dB")
                return None
            
            idx_5db = idx_5db_candidates[0]
            idx_35db = idx_35db_candidates[0]
            
            # 线性拟合这段衰减曲线
            time_range = np.arange(idx_5db, idx_35db) / self.sample_rate
            db_range = schroeder_db[idx_5db:idx_35db]
            
            if len(time_range) < 2:
                if verbose:
                    print("[T60 测量] 错误: 衰减范围太短，无法拟合")
                return None
            
            # 计算斜率（dB/秒）
            slope = (db_range[-1] - db_range[0]) / (time_range[-1] - time_range[0])
            
            if abs(slope) < 1e-6:
                if verbose:
                    print("[T60 测量] 错误: 衰减斜率接近零")
                return None
            
            # 外推到 60dB
            t60 = 60 / abs(slope)
            
            if verbose:
                print(f"[T60 测量] 成功")
                print(f"  - 测量范围: -5dB 到 -35dB")
                print(f"  - 衰减斜率: {slope:.2f} dB/s")
                print(f"  - T60: {t60:.3f} s")
            
            return t60
            
        except Exception as e:
            if verbose:
                print(f"[T60 测量] 异常: {str(e)}")
            return None
    
    def measure_c80(self, verbose: bool = False) -> Optional[float]:
        """
        计算清晰度指数 C80
        
        C80 定义：前 80ms 能量与后续能量的比值（dB）
        - C80 > 0dB: 近距离、清晰的空间
        - C80 < -5dB: 遥远、扩散的空间
        
        参数:
            verbose: 是否输出详细验证信息
        
        返回:
            C80 值（dB），如果无法计算则返回 None
        
        参考: 复用自 gen_S04_contrast_IRs.py
        
        验证: 需求 4.4
        """
        try:
            # 如果是立体声，使用单声道混音
            if self.is_stereo:
                audio = np.mean(self.audio, axis=1)
            else:
                audio = self.audio
            
            # 计算能量
            energy = audio ** 2
            
            # 80ms 对应的样本数
            samples_80ms = int(0.08 * self.sample_rate)
            
            if len(energy) <= samples_80ms:
                if verbose:
                    print(f"[C80 测量] 错误: 音频长度 ({len(energy)} 样本) 不足 80ms ({samples_80ms} 样本)")
                return None
            
            # 前 80ms 能量
            early_energy = np.sum(energy[:samples_80ms])
            
            # 后续能量
            late_energy = np.sum(energy[samples_80ms:])
            
            if late_energy == 0:
                if verbose:
                    print("[C80 测量] 错误: 后续能量为零")
                return None
            
            # C80 = 10 * log10(early / late)
            c80 = 10 * np.log10(early_energy / late_energy)
            
            if verbose:
                print(f"[C80 测量] 成功")
                print(f"  - 早期能量 (0-80ms): {early_energy:.6e}")
                print(f"  - 晚期能量 (>80ms): {late_energy:.6e}")
                print(f"  - C80: {c80:.2f} dB")
                if c80 > 0:
                    print(f"  - 解释: 近距离、清晰的空间")
                elif c80 < -5:
                    print(f"  - 解释: 遥远、扩散的空间")
                else:
                    print(f"  - 解释: 中等距离空间")
            
            return c80
            
        except Exception as e:
            if verbose:
                print(f"[C80 测量] 异常: {str(e)}")
            return None
    
    def measure_edt(self, verbose: bool = False) -> Optional[float]:
        """
        测量早期衰减时间 EDT (Early Decay Time)
        
        EDT 定义：前 10dB 衰减时间外推到 60dB
        EDT 反映混响的主观感知，通常与 T60 接近（扩散声场）
        
        参数:
            verbose: 是否输出详细验证信息
        
        返回:
            EDT 时间（秒），如果无法测量则返回 None
        
        参考: 复用自 IR 合成改进规范
        
        验证: 需求 4.1, 4.3
        """
        try:
            # 如果是立体声，使用单声道混音
            if self.is_stereo:
                audio = np.mean(self.audio, axis=1)
            else:
                audio = self.audio
            
            # 计算能量包络
            energy = audio ** 2
            
            # Schroeder 反向积分
            schroeder = np.cumsum(energy[::-1])[::-1]
            
            if schroeder[0] == 0:
                if verbose:
                    print("[EDT 测量] 错误: 信号能量为零")
                return None
            
            schroeder = schroeder / schroeder[0]
            
            # 转换为 dB
            schroeder_db = 10 * np.log10(schroeder + 1e-10)
            
            # 找到 0dB 和 -10dB 的位置
            idx_0db = 0  # 起始点
            idx_10db_candidates = np.where(schroeder_db <= -10)[0]
            
            if len(idx_10db_candidates) == 0:
                if verbose:
                    print("[EDT 测量] 错误: 信号未衰减到 -10dB")
                return None
            
            idx_10db = idx_10db_candidates[0]
            
            if idx_10db <= idx_0db:
                if verbose:
                    print("[EDT 测量] 错误: 衰减范围无效")
                return None
            
            # 线性拟合
            time_range = np.arange(idx_0db, idx_10db) / self.sample_rate
            db_range = schroeder_db[idx_0db:idx_10db]
            
            if len(time_range) < 2:
                if verbose:
                    print("[EDT 测量] 错误: 衰减范围太短，无法拟合")
                return None
            
            # 计算斜率
            slope = (db_range[-1] - db_range[0]) / (time_range[-1] - time_range[0])
            
            if abs(slope) < 1e-6:
                if verbose:
                    print("[EDT 测量] 错误: 衰减斜率接近零")
                return None
            
            # 外推到 60dB
            edt = 60 / abs(slope)
            
            if verbose:
                print(f"[EDT 测量] 成功")
                print(f"  - 测量范围: 0dB 到 -10dB")
                print(f"  - 衰减斜率: {slope:.2f} dB/s")
                print(f"  - EDT: {edt:.3f} s")
                print(f"  - 注: EDT 反映混响的主观感知")
            
            return edt
            
        except Exception as e:
            if verbose:
                print(f"[EDT 测量] 异常: {str(e)}")
            return None
    
    def measure_pre_delay(self, threshold_db: float = -40, verbose: bool = False) -> Optional[float]:
        """
        测量预延迟时间（直达声到达时间）
        
        预延迟反映声源到听者的距离感。较长的预延迟（>80ms）
        会产生"遥远"的感觉，适合虚空等深远空间。
        
        参数:
            threshold_db: 检测阈值（dB），默认 -40dB
            verbose: 是否输出详细验证信息
        
        返回:
            预延迟时间（毫秒），如果无法测量则返回 None
        
        验证: 需求 4.1, 4.4
        """
        try:
            # 如果是立体声，使用单声道混音
            if self.is_stereo:
                audio = np.mean(self.audio, axis=1)
            else:
                audio = self.audio
            
            # 计算包络
            envelope = np.abs(audio)
            
            # 找到最大值
            max_val = np.max(envelope)
            
            if max_val == 0:
                if verbose:
                    print("[预延迟测量] 错误: 信号最大值为零")
                return None
            
            # 阈值（线性）
            threshold = max_val * 10 ** (threshold_db / 20)
            
            # 找到第一个超过阈值的样本
            above_threshold = np.where(envelope > threshold)[0]
            
            if len(above_threshold) == 0:
                if verbose:
                    print(f"[预延迟测量] 错误: 没有样本超过阈值 {threshold_db} dB")
                return None
            
            first_sample = above_threshold[0]
            pre_delay_ms = (first_sample / self.sample_rate) * 1000
            
            if verbose:
                print(f"[预延迟测量] 成功")
                print(f"  - 检测阈值: {threshold_db} dB")
                print(f"  - 第一个样本: {first_sample}")
                print(f"  - 预延迟: {pre_delay_ms:.2f} ms")
                if pre_delay_ms >= 80:
                    print(f"  - 解释: 较长预延迟，产生遥远感（适合虚空）")
                elif pre_delay_ms >= 20:
                    print(f"  - 解释: 中等预延迟，产生空间感")
                else:
                    print(f"  - 解释: 短预延迟，声源较近")
            
            return pre_delay_ms
            
        except Exception as e:
            if verbose:
                print(f"[预延迟测量] 异常: {str(e)}")
            return None
    
    # ========================================================================
    # 立体声分析
    # ========================================================================
    
    def compute_stereo_correlation(self) -> Optional[float]:
        """
        计算立体声相关系数
        
        相关系数范围: [-1, 1]
        - +1: 完全相同（单声道）
        - 0: 不相关（宽立体声）
        - -1: 完全反相
        
        返回:
            立体声相关系数，如果不是立体声则返回 None
        
        注意: 如果左右声道都是常数（标准差为零），返回 1.0（完全相关）
        """
        if not self.is_stereo:
            return None
        
        left = self.audio[:, 0]
        right = self.audio[:, 1]
        
        # 检查是否为常数信号（标准差为零）
        left_std = np.std(left)
        right_std = np.std(right)
        
        # 如果两个声道都是常数，它们完全相关
        if left_std == 0 and right_std == 0:
            return 1.0
        
        # 如果只有一个声道是常数，相关性无定义，返回 0
        if left_std == 0 or right_std == 0:
            return 0.0
        
        # 计算相关系数
        correlation = np.corrcoef(left, right)[0, 1]
        
        # 处理 NaN（虽然上面的检查应该已经避免了）
        if np.isnan(correlation):
            return 1.0  # 默认为完全相关
        
        return correlation
    
    def estimate_stereo_width(self) -> Optional[float]:
        """
        估计立体声宽度（百分比）
        
        基于立体声相关系数估算:
        - 100%: 正常立体声（相关系数 ≈ 0.5）
        - 0%: 单声道（相关系数 ≈ 1.0）
        - 150%+: 扩展立体声（相关系数 < 0.3）
        
        返回:
            立体声宽度（百分比），如果不是立体声则返回 None
        """
        correlation = self.compute_stereo_correlation()
        
        if correlation is None:
            return None
        
        # 简单的线性映射（可以改进）
        # correlation = 1.0 -> width = 0%
        # correlation = 0.5 -> width = 100%
        # correlation = 0.0 -> width = 200%
        
        width = (1.0 - correlation) * 200
        
        return width
    
    def detect_pan_position(self) -> Optional[str]:
        """
        检测声像位置
        
        返回:
            "center", "left", "right", "wide" 之一，如果不是立体声则返回 None
        """
        correlation = self.compute_stereo_correlation()
        
        if correlation is None:
            return None
        
        if correlation > STEREO_CORRELATION_THRESHOLDS["mono"]:
            return "center"
        elif correlation < STEREO_CORRELATION_THRESHOLDS["wide"]:
            return "wide"
        else:
            # 检查左右能量平衡
            left_energy = np.sum(self.audio[:, 0] ** 2)
            right_energy = np.sum(self.audio[:, 1] ** 2)
            
            ratio = left_energy / (right_energy + 1e-10)
            
            if ratio > 2.0:
                return "left"
            elif ratio < 0.5:
                return "right"
            else:
                return "center"
    
    # ========================================================================
    # 频谱分析
    # ========================================================================
    
    def compute_psd(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        计算功率谱密度 (Power Spectral Density)
        
        返回:
            (频率数组, PSD数组) 元组
        """
        # 如果是立体声，使用单声道混音
        if self.is_stereo:
            audio = np.mean(self.audio, axis=1)
        else:
            audio = self.audio
        
        # 使用 Welch 方法计算 PSD
        frequencies, psd = scipy_signal.welch(
            audio,
            fs=self.sample_rate,
            nperseg=min(2048, len(audio)),
            scaling='density'
        )
        
        return frequencies, psd
    
    def compute_spectral_centroid(self) -> float:
        """
        计算频谱质心（Hz）
        
        频谱质心是频谱的"重心"，反映音频的"明亮度"
        
        返回:
            频谱质心（Hz）
        """
        frequencies, psd = self.compute_psd()
        
        # 计算质心
        centroid = np.sum(frequencies * psd) / np.sum(psd)
        
        return centroid
    
    def compute_spectral_rolloff(self, percentile: float = 0.85) -> float:
        """
        计算频谱滚降点（Hz）
        
        频谱滚降点是累积能量达到指定百分比的频率
        
        参数:
            percentile: 百分比（默认 0.85 = 85%）
        
        返回:
            频谱滚降点（Hz）
        """
        frequencies, psd = self.compute_psd()
        
        # 计算累积能量
        cumulative_energy = np.cumsum(psd)
        total_energy = cumulative_energy[-1]
        
        # 找到滚降点
        threshold = total_energy * percentile
        rolloff_idx = np.where(cumulative_energy >= threshold)[0][0]
        rolloff_freq = frequencies[rolloff_idx]
        
        return rolloff_freq
    
    def analyze_octave_bands(self) -> Dict[str, float]:
        """
        分析八度频段能量
        
        返回:
            字典，键为频段字符串（如 "125-250 Hz"），值为能量（dB）
        """
        frequencies, psd = self.compute_psd()
        
        # 转换为 dB
        psd_db = 10 * np.log10(psd + 1e-10)
        
        octave_energies = {}
        
        for low, high in OCTAVE_BANDS:
            mask = (frequencies >= low) & (frequencies < high)
            if np.any(mask):
                band_energy = np.mean(psd_db[mask])
                octave_energies[f"{low:.1f}-{high:.0f} Hz"] = band_energy
        
        return octave_energies
    
    def analyze_spectrum(self) -> SpectralAnalysis:
        """
        完整的频谱分析
        
        返回:
            SpectralAnalysis 对象
        """
        frequencies, psd = self.compute_psd()
        octave_energies = self.analyze_octave_bands()
        centroid = self.compute_spectral_centroid()
        rolloff = self.compute_spectral_rolloff()
        
        # 找到主导频率（前5个峰值）
        psd_db = 10 * np.log10(psd + 1e-10)
        peaks, _ = scipy_signal.find_peaks(psd_db, height=np.max(psd_db) - 20)
        
        if len(peaks) > 0:
            # 按幅度排序
            peak_heights = psd_db[peaks]
            sorted_indices = np.argsort(peak_heights)[::-1]
            top_peaks = peaks[sorted_indices[:5]]
            dominant_freqs = frequencies[top_peaks].tolist()
        else:
            dominant_freqs = []
        
        return SpectralAnalysis(
            frequencies=frequencies,
            psd=psd,
            octave_band_energy=octave_energies,
            spectral_centroid=centroid,
            spectral_rolloff=rolloff,
            dominant_frequencies=dominant_freqs
        )
    
    # ========================================================================
    # 伪影检测
    # ========================================================================
    
    def detect_clipping(self) -> Tuple[bool, List[float]]:
        """
        检测削波（样本值接近 ±1.0）
        
        返回:
            (是否有削波, 削波位置列表（秒）) 元组
        """
        threshold = ARTIFACT_THRESHOLDS["clipping"]
        
        # 检测所有声道
        if self.is_stereo:
            clipped = np.abs(self.audio) >= threshold
            clipped = np.any(clipped, axis=1)
        else:
            clipped = np.abs(self.audio) >= threshold
        
        # 找到削波位置
        clipped_indices = np.where(clipped)[0]
        
        if len(clipped_indices) > 0:
            # 转换为时间（秒）
            clipped_times = clipped_indices / self.sample_rate
            return True, clipped_times.tolist()
        else:
            return False, []
    
    def detect_dc_offset(self) -> Tuple[bool, float]:
        """
        检测直流偏移
        
        返回:
            (是否有直流偏移, 偏移值) 元组
        """
        threshold = ARTIFACT_THRESHOLDS["dc_offset"]
        
        # 计算平均值
        if self.is_stereo:
            mean_val = np.mean(np.mean(self.audio, axis=1))
        else:
            mean_val = np.mean(self.audio)
        
        has_offset = abs(mean_val) > threshold
        
        return has_offset, mean_val
    
    def detect_discontinuities(self) -> Tuple[bool, List[float]]:
        """
        检测不连续性（突然的幅度跳跃）
        
        返回:
            (是否有不连续, 不连续位置列表（秒）) 元组
        """
        threshold = ARTIFACT_THRESHOLDS["discontinuity"]
        
        # 计算相邻样本差
        if self.is_stereo:
            diff = np.diff(self.audio, axis=0)
            diff_max = np.max(np.abs(diff), axis=1)
        else:
            diff = np.diff(self.audio)
            diff_max = np.abs(diff)
        
        # 检测跳跃
        discontinuous = diff_max > threshold
        discontinuous_indices = np.where(discontinuous)[0]
        
        if len(discontinuous_indices) > 0:
            # 转换为时间（秒）
            discontinuous_times = discontinuous_indices / self.sample_rate
            return True, discontinuous_times.tolist()
        else:
            return False, []
    
    def detect_aliasing(self) -> bool:
        """
        检测混叠（高频能量超过 Nyquist 频率的 90%）
        
        返回:
            是否有混叠
        """
        frequencies, psd = self.compute_psd()
        
        nyquist = self.sample_rate / 2
        threshold_freq = nyquist * 0.9
        
        # 检查高频能量
        high_freq_mask = frequencies >= threshold_freq
        
        if not np.any(high_freq_mask):
            return False
        
        high_freq_energy = np.sum(psd[high_freq_mask])
        total_energy = np.sum(psd)
        
        # 如果高频能量超过总能量的 10%，认为有混叠
        has_aliasing = (high_freq_energy / total_energy) > 0.1
        
        return has_aliasing
    
    def detect_artifacts(self) -> ArtifactReport:
        """
        完整的伪影检测
        
        返回:
            ArtifactReport 对象
        """
        has_clipping, clipping_locs = self.detect_clipping()
        has_dc, dc_value = self.detect_dc_offset()
        has_disc, disc_locs = self.detect_discontinuities()
        has_aliasing = self.detect_aliasing()
        
        return ArtifactReport(
            has_clipping=has_clipping,
            clipping_locations=clipping_locs,
            has_dc_offset=has_dc,
            dc_offset_value=dc_value,
            has_discontinuities=has_disc,
            discontinuity_locations=disc_locs,
            has_aliasing=has_aliasing
        )
    
    # ========================================================================
    # 综合分析
    # ========================================================================
    
    def compute_rms_energy(self) -> float:
        """
        计算 RMS 能量（dB）
        
        返回:
            RMS 能量（dB）
        """
        # 如果是立体声，使用单声道混音
        if self.is_stereo:
            audio = np.mean(self.audio, axis=1)
        else:
            audio = self.audio
        
        rms = np.sqrt(np.mean(audio ** 2))
        rms_db = 20 * np.log10(rms + 1e-10)
        
        return rms_db
    
    def compute_peak_amplitude(self) -> float:
        """
        计算峰值幅度
        
        返回:
            峰值幅度（线性，0-1）
        """
        return np.max(np.abs(self.audio))
    
    def get_acoustic_metrics(self, verbose: bool = False) -> AcousticMetrics:
        """
        获取所有声学指标
        
        参数:
            verbose: 是否输出详细验证信息
        
        返回:
            AcousticMetrics 对象
        
        验证: 需求 4.1, 4.2, 4.3, 4.4
        """
        if verbose:
            print("\n" + "="*60)
            print("声学指标测量")
            print("="*60)
        
        metrics = AcousticMetrics(
            t60=self.measure_t60(verbose=verbose),
            edt=self.measure_edt(verbose=verbose),
            c80=self.measure_c80(verbose=verbose),
            pre_delay_ms=self.measure_pre_delay(verbose=verbose),
            stereo_correlation=self.compute_stereo_correlation(),
            stereo_width_percent=self.estimate_stereo_width(),
            rms_energy_db=self.compute_rms_energy(),
            peak_amplitude=self.compute_peak_amplitude(),
            spectral_centroid_hz=self.compute_spectral_centroid()
        )
        
        if verbose:
            print("\n" + "-"*60)
            print("测量摘要:")
            print("-"*60)
            if metrics.t60 is not None:
                print(f"T60 (混响时间):        {metrics.t60:.3f} s")
            if metrics.edt is not None:
                print(f"EDT (早期衰减时间):    {metrics.edt:.3f} s")
            if metrics.c80 is not None:
                print(f"C80 (清晰度指数):      {metrics.c80:.2f} dB")
            if metrics.pre_delay_ms is not None:
                print(f"预延迟:                {metrics.pre_delay_ms:.2f} ms")
            if metrics.stereo_correlation is not None:
                print(f"立体声相关性:          {metrics.stereo_correlation:.3f}")
            if metrics.stereo_width_percent is not None:
                print(f"立体声宽度:            {metrics.stereo_width_percent:.1f}%")
            print(f"RMS 能量:              {metrics.rms_energy_db:.2f} dB")
            print(f"峰值幅度:              {metrics.peak_amplitude:.3f}")
            if metrics.spectral_centroid_hz is not None:
                print(f"频谱质心:              {metrics.spectral_centroid_hz:.1f} Hz")
            print("="*60 + "\n")
        
        return metrics
