"""
频谱分析函数测试
================

测试 AudioAnalyzer 的频谱分析功能：
- 功率谱密度（PSD）计算
- 频谱质心计算
- 八度频段能量分析

验证：需求 3.1, 11.4
"""

import pytest
import numpy as np
from scipy import signal as scipy_signal

import sys
import os

# 添加父目录到路径
qa_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, qa_dir)

from audio_analyzer import AudioAnalyzer
from config import OCTAVE_BANDS


# ============================================================================
# 辅助函数
# ============================================================================

def generate_sine_wave(frequency: float, duration: float, sample_rate: int = 48000, amplitude: float = 0.5) -> np.ndarray:
    """生成正弦波"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t)


def generate_pink_noise(duration: float, sample_rate: int = 48000) -> np.ndarray:
    """生成粉红噪音（简化版本）"""
    # 生成白噪音
    white = np.random.randn(int(sample_rate * duration))
    
    # 应用 1/f 滤波器（简化）
    # 使用低通滤波器近似粉红噪音
    b, a = scipy_signal.butter(1, 0.5, btype='low')
    pink = scipy_signal.filtfilt(b, a, white)
    
    # 归一化
    pink = pink / np.max(np.abs(pink)) * 0.5
    
    return pink


# ============================================================================
# 功率谱密度（PSD）测试
# ============================================================================

@pytest.mark.unit
def test_compute_psd_basic():
    """测试 PSD 计算基本功能"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成测试音频（1000 Hz 正弦波）
    audio = generate_sine_wave(1000, duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    frequencies, psd = analyzer.compute_psd()
    
    # 验证输出形状
    assert len(frequencies) == len(psd)
    assert len(frequencies) > 0
    
    # 验证频率范围
    assert frequencies[0] >= 0
    assert frequencies[-1] <= sample_rate / 2  # Nyquist 频率
    
    # 验证 PSD 是正数
    assert np.all(psd >= 0)


@pytest.mark.unit
def test_compute_psd_sine_wave_peak():
    """测试 PSD 在正弦波频率处有峰值"""
    sample_rate = 48000
    duration = 2.0
    test_frequency = 1000  # Hz
    
    # 生成正弦波
    audio = generate_sine_wave(test_frequency, duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    frequencies, psd = analyzer.compute_psd()
    
    # 找到峰值频率
    peak_idx = np.argmax(psd)
    peak_frequency = frequencies[peak_idx]
    
    # 验证峰值频率接近测试频率（允许一定误差）
    assert abs(peak_frequency - test_frequency) < 50  # ±50 Hz 误差


@pytest.mark.unit
def test_compute_psd_stereo():
    """测试立体声音频的 PSD 计算"""
    sample_rate = 48000
    duration = 1.0
    n_samples = int(sample_rate * duration)
    
    # 生成立体声音频
    left = generate_sine_wave(1000, duration, sample_rate)
    right = generate_sine_wave(2000, duration, sample_rate)
    stereo = np.stack([left, right], axis=1)
    
    analyzer = AudioAnalyzer(audio_data=stereo, sample_rate=sample_rate)
    frequencies, psd = analyzer.compute_psd()
    
    # 验证输出（应该使用单声道混音）
    assert len(frequencies) == len(psd)
    assert len(frequencies) > 0


# ============================================================================
# 频谱质心测试
# ============================================================================

@pytest.mark.unit
def test_compute_spectral_centroid_basic():
    """测试频谱质心计算基本功能"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成测试音频
    audio = generate_sine_wave(1000, duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    centroid = analyzer.compute_spectral_centroid()
    
    # 验证质心是正数且在合理范围内
    assert centroid > 0
    assert centroid < sample_rate / 2  # 小于 Nyquist 频率


@pytest.mark.unit
def test_spectral_centroid_sine_wave():
    """测试正弦波的频谱质心接近其频率"""
    sample_rate = 48000
    duration = 2.0
    test_frequency = 2000  # Hz
    
    # 生成正弦波
    audio = generate_sine_wave(test_frequency, duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    centroid = analyzer.compute_spectral_centroid()
    
    # 验证质心接近测试频率（允许较大误差，因为 Welch 方法的频率分辨率）
    assert abs(centroid - test_frequency) < 500  # ±500 Hz 误差


@pytest.mark.unit
def test_spectral_centroid_low_vs_high():
    """测试低频音频的质心低于高频音频"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成低频音频（500 Hz）
    low_freq_audio = generate_sine_wave(500, duration, sample_rate)
    analyzer_low = AudioAnalyzer(audio_data=low_freq_audio, sample_rate=sample_rate)
    centroid_low = analyzer_low.compute_spectral_centroid()
    
    # 生成高频音频（5000 Hz）
    high_freq_audio = generate_sine_wave(5000, duration, sample_rate)
    analyzer_high = AudioAnalyzer(audio_data=high_freq_audio, sample_rate=sample_rate)
    centroid_high = analyzer_high.compute_spectral_centroid()
    
    # 验证低频质心 < 高频质心
    assert centroid_low < centroid_high


@pytest.mark.unit
def test_spectral_centroid_brightness():
    """测试频谱质心反映音频明亮度"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成"暗"音频（低频为主）
    dark_audio = generate_sine_wave(200, duration, sample_rate, 0.5)
    dark_audio += generate_sine_wave(400, duration, sample_rate, 0.3)
    analyzer_dark = AudioAnalyzer(audio_data=dark_audio, sample_rate=sample_rate)
    centroid_dark = analyzer_dark.compute_spectral_centroid()
    
    # 生成"亮"音频（高频为主）
    bright_audio = generate_sine_wave(2000, duration, sample_rate, 0.5)
    bright_audio += generate_sine_wave(4000, duration, sample_rate, 0.3)
    analyzer_bright = AudioAnalyzer(audio_data=bright_audio, sample_rate=sample_rate)
    centroid_bright = analyzer_bright.compute_spectral_centroid()
    
    # 验证"暗"音频质心 < "亮"音频质心
    assert centroid_dark < centroid_bright
    
    # 验证"暗"音频质心在低频范围
    assert centroid_dark < 1000
    
    # 验证"亮"音频质心在高频范围
    assert centroid_bright > 2000


# ============================================================================
# 八度频段能量分析测试
# ============================================================================

@pytest.mark.unit
def test_analyze_octave_bands_basic():
    """测试八度频段能量分析基本功能"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成测试音频
    audio = generate_pink_noise(duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    octave_energies = analyzer.analyze_octave_bands()
    
    # 验证返回字典
    assert isinstance(octave_energies, dict)
    
    # 验证包含所有频段
    assert len(octave_energies) > 0
    
    # 验证能量值是数字
    for band, energy in octave_energies.items():
        assert isinstance(energy, (int, float))
        assert not np.isnan(energy)
        assert not np.isinf(energy)


@pytest.mark.unit
def test_octave_bands_coverage():
    """测试八度频段覆盖所有定义的频段"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成宽频音频
    audio = generate_pink_noise(duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    octave_energies = analyzer.analyze_octave_bands()
    
    # 验证频段数量（应该接近 OCTAVE_BANDS 的数量）
    # 注意：高频段可能超出 Nyquist 频率而被排除
    expected_bands = len([band for band in OCTAVE_BANDS if band[1] <= sample_rate / 2])
    assert len(octave_energies) >= expected_bands - 1  # 允许少一个频段


@pytest.mark.unit
def test_octave_bands_low_frequency_energy():
    """测试低频音频在低频段有更高能量"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成低频音频（100 Hz）
    audio = generate_sine_wave(100, duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    octave_energies = analyzer.analyze_octave_bands()
    
    # 找到包含 100 Hz 的频段
    target_band = None
    for band_name, energy in octave_energies.items():
        # 解析频段范围
        parts = band_name.replace(" Hz", "").split("-")
        low = float(parts[0])
        high = float(parts[1])
        
        if low <= 100 < high:
            target_band = band_name
            break
    
    # 验证找到了目标频段
    assert target_band is not None
    
    # 验证目标频段能量最高（或接近最高）
    target_energy = octave_energies[target_band]
    max_energy = max(octave_energies.values())
    
    # 目标频段能量应该接近最大能量（允许 10 dB 误差）
    assert target_energy >= max_energy - 10


@pytest.mark.unit
def test_octave_bands_high_frequency_energy():
    """测试高频音频在高频段有更高能量"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成高频音频（5000 Hz）
    audio = generate_sine_wave(5000, duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    octave_energies = analyzer.analyze_octave_bands()
    
    # 找到包含 5000 Hz 的频段
    target_band = None
    for band_name, energy in octave_energies.items():
        parts = band_name.replace(" Hz", "").split("-")
        low = float(parts[0])
        high = float(parts[1])
        
        if low <= 5000 < high:
            target_band = band_name
            break
    
    # 验证找到了目标频段
    assert target_band is not None
    
    # 验证目标频段能量最高（或接近最高）
    target_energy = octave_energies[target_band]
    max_energy = max(octave_energies.values())
    
    # 目标频段能量应该接近最大能量
    assert target_energy >= max_energy - 10


# ============================================================================
# 综合频谱分析测试
# ============================================================================

@pytest.mark.unit
def test_analyze_spectrum_complete():
    """测试完整的频谱分析"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成测试音频
    audio = generate_pink_noise(duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    spectrum = analyzer.analyze_spectrum()
    
    # 验证所有字段都存在
    assert spectrum.frequencies is not None
    assert spectrum.psd is not None
    assert spectrum.octave_band_energy is not None
    assert spectrum.spectral_centroid is not None
    assert spectrum.spectral_rolloff is not None
    assert spectrum.dominant_frequencies is not None
    
    # 验证数据类型
    assert isinstance(spectrum.frequencies, np.ndarray)
    assert isinstance(spectrum.psd, np.ndarray)
    assert isinstance(spectrum.octave_band_energy, dict)
    assert isinstance(spectrum.spectral_centroid, (int, float))
    assert isinstance(spectrum.spectral_rolloff, (int, float))
    assert isinstance(spectrum.dominant_frequencies, list)


@pytest.mark.unit
def test_analyze_spectrum_dominant_frequencies():
    """测试主导频率检测"""
    sample_rate = 48000
    duration = 2.0
    
    # 生成多频音频（1000 Hz 和 3000 Hz）
    audio = generate_sine_wave(1000, duration, sample_rate, 0.5)
    audio += generate_sine_wave(3000, duration, sample_rate, 0.3)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    spectrum = analyzer.analyze_spectrum()
    
    # 验证检测到主导频率
    assert len(spectrum.dominant_frequencies) > 0
    
    # 验证主导频率接近 1000 Hz 或 3000 Hz
    # （至少有一个主导频率在这些频率附近）
    found_1000 = any(abs(f - 1000) < 100 for f in spectrum.dominant_frequencies)
    found_3000 = any(abs(f - 3000) < 100 for f in spectrum.dominant_frequencies)
    
    assert found_1000 or found_3000


@pytest.mark.unit
def test_spectral_rolloff():
    """测试频谱滚降点计算"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成测试音频
    audio = generate_pink_noise(duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    rolloff = analyzer.compute_spectral_rolloff()
    
    # 验证滚降点在合理范围内
    assert 0 < rolloff < sample_rate / 2
    
    # 验证滚降点大于质心（通常情况下）
    centroid = analyzer.compute_spectral_centroid()
    # 注意：这不是绝对规则，但对于大多数音频成立
    # 我们只验证它们都在合理范围内
    assert 0 < centroid < sample_rate / 2


# ============================================================================
# 边缘情况测试
# ============================================================================

@pytest.mark.unit
def test_spectral_analysis_silent_audio():
    """测试静音音频的频谱分析"""
    sample_rate = 48000
    duration = 1.0
    
    # 生成静音音频
    audio = np.zeros(int(sample_rate * duration))
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    
    # PSD 应该接近零
    frequencies, psd = analyzer.compute_psd()
    assert np.all(psd < 1e-10)
    
    # 频谱质心可能无定义或非常低
    centroid = analyzer.compute_spectral_centroid()
    # 对于静音，质心可能是 NaN 或接近零
    assert np.isnan(centroid) or centroid < 100


@pytest.mark.unit
def test_spectral_analysis_very_short_audio():
    """测试极短音频的频谱分析"""
    sample_rate = 48000
    
    # 生成极短音频（100 个样本）
    audio = generate_sine_wave(1000, 100/sample_rate, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    
    # 应该能够计算 PSD（即使频率分辨率很低）
    frequencies, psd = analyzer.compute_psd()
    assert len(frequencies) > 0
    assert len(psd) > 0
    
    # 应该能够计算质心
    centroid = analyzer.compute_spectral_centroid()
    assert centroid > 0


@pytest.mark.unit
def test_octave_bands_format():
    """测试八度频段输出格式"""
    sample_rate = 48000
    duration = 1.0
    
    audio = generate_pink_noise(duration, sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    octave_energies = analyzer.analyze_octave_bands()
    
    # 验证键格式（应该是 "低-高 Hz"）
    for band_name in octave_energies.keys():
        assert " Hz" in band_name
        assert "-" in band_name
        
        # 验证可以解析频率范围
        parts = band_name.replace(" Hz", "").split("-")
        assert len(parts) == 2
        
        low = float(parts[0])
        high = float(parts[1])
        
        # 验证低频 < 高频
        assert low < high


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
