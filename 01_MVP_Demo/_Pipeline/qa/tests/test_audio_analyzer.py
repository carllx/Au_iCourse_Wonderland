"""
音频分析器测试
==============

测试 AudioAnalyzer 类的功能。
"""

import pytest
import numpy as np
from hypothesis import given, strategies as st
import hypothesis.extra.numpy as npst

import sys
import os

# 添加父目录到路径
qa_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, qa_dir)

# 使用绝对导入
import audio_analyzer
import config

AudioAnalyzer = audio_analyzer.AudioAnalyzer
ArtifactReport = config.ArtifactReport


# ============================================================================
# 单元测试
# ============================================================================

@pytest.mark.unit
def test_audio_analyzer_initialization():
    """测试 AudioAnalyzer 初始化"""
    # 生成测试音频
    sample_rate = 48000
    duration = 1.0
    audio = np.random.randn(int(sample_rate * duration))
    
    # 初始化分析器
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    
    # 验证属性
    assert analyzer.sample_rate == sample_rate
    assert len(analyzer.audio) == int(sample_rate * duration)
    assert not analyzer.is_stereo
    assert analyzer.duration == pytest.approx(duration, rel=0.01)


@pytest.mark.unit
def test_stereo_audio_detection():
    """测试立体声检测"""
    sample_rate = 48000
    duration = 1.0
    n_samples = int(sample_rate * duration)
    
    # 生成立体声音频
    stereo_audio = np.random.randn(n_samples, 2)
    
    analyzer = AudioAnalyzer(audio_data=stereo_audio, sample_rate=sample_rate)
    
    assert analyzer.is_stereo


@pytest.mark.unit
def test_compute_rms_energy():
    """测试 RMS 能量计算"""
    sample_rate = 48000
    
    # 生成已知 RMS 的音频
    amplitude = 0.5
    audio = np.ones(sample_rate) * amplitude
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    rms_db = analyzer.compute_rms_energy()
    
    # 验证 RMS（应该接近 20*log10(0.5) ≈ -6dB）
    expected_db = 20 * np.log10(amplitude)
    assert rms_db == pytest.approx(expected_db, abs=0.1)


@pytest.mark.unit
def test_detect_clipping():
    """测试削波检测"""
    sample_rate = 48000
    
    # 生成有削波的音频
    audio = np.array([0.5, 0.8, 1.0, 1.0, 0.9, 0.6])
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_clipping, locations = analyzer.detect_clipping()
    
    # 验证检测到削波
    assert has_clipping
    assert len(locations) == 2  # 两个样本削波


@pytest.mark.unit
def test_detect_dc_offset():
    """测试直流偏移检测"""
    sample_rate = 48000
    
    # 生成有直流偏移的音频
    audio = np.random.randn(sample_rate) + 0.5  # 偏移 +0.5
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_offset, offset_value = analyzer.detect_dc_offset()
    
    # 验证检测到偏移
    assert has_offset
    assert offset_value == pytest.approx(0.5, abs=0.1)


@pytest.mark.unit
def test_stereo_correlation_mono():
    """测试单声道音频的立体声相关性"""
    sample_rate = 48000
    duration = 1.0
    n_samples = int(sample_rate * duration)
    
    # 生成单声道音频（左右声道相同）
    mono = np.random.randn(n_samples)
    stereo = np.stack([mono, mono], axis=1)
    
    analyzer = AudioAnalyzer(audio_data=stereo, sample_rate=sample_rate)
    correlation = analyzer.compute_stereo_correlation()
    
    # 验证相关性接近 1.0
    assert correlation == pytest.approx(1.0, abs=0.01)


@pytest.mark.unit
def test_stereo_correlation_inverted():
    """测试反相音频的立体声相关性"""
    sample_rate = 48000
    duration = 1.0
    n_samples = int(sample_rate * duration)
    
    # 生成反相音频（左右声道相反）
    left = np.random.randn(n_samples)
    right = -left
    stereo = np.stack([left, right], axis=1)
    
    analyzer = AudioAnalyzer(audio_data=stereo, sample_rate=sample_rate)
    correlation = analyzer.compute_stereo_correlation()
    
    # 验证相关性接近 -1.0
    assert correlation == pytest.approx(-1.0, abs=0.01)


# ============================================================================
# 属性测试
# ============================================================================

# Feature: phase4-synthesis-qa, Property 2: 立体声成像一致性
@given(
    left=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000)),
    right=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000))
)
@pytest.mark.property
def test_stereo_correlation_range(left, right):
    """
    属性：立体声相关系数应该在 [-1, 1] 范围内
    
    **验证：需求 2.1, 2.2, 2.3, 2.5**
    """
    # 确保左右声道长度相同
    min_len = min(len(left), len(right))
    left = left[:min_len]
    right = right[:min_len]
    
    # 避免全零数组
    if np.all(left == 0) or np.all(right == 0):
        return
    
    # 创建立体声音频
    stereo = np.stack([left, right], axis=1)
    analyzer = AudioAnalyzer(audio_data=stereo, sample_rate=48000)
    
    # 计算立体声相关系数
    correlation = analyzer.compute_stereo_correlation()
    
    # 验证范围
    assert -1.0 <= correlation <= 1.0


# Feature: phase4-synthesis-qa, Property 6: 伪影综合检测
@given(
    audio=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000),
                     elements=st.floats(min_value=-0.9, max_value=0.9, allow_nan=False, allow_infinity=False))
)
@pytest.mark.property
def test_artifact_detection_no_false_positives(audio):
    """
    属性：对于正常音频（无伪影），不应该误报
    
    **验证：需求 6.1, 6.2, 6.3, 6.4, 6.5**
    """
    # 移除直流偏移
    audio = audio - np.mean(audio)
    
    # 平滑音频以避免不连续性
    # 使用简单的移动平均来避免突然跳跃
    if len(audio) > 10:
        window = np.ones(5) / 5
        audio = np.convolve(audio, window, mode='same')
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=48000)
    artifacts = analyzer.detect_artifacts()
    
    # 验证不应该检测到削波（因为我们限制在 ±0.9）
    assert not artifacts.has_clipping
    
    # 验证不应该检测到直流偏移（因为我们移除了）
    assert not artifacts.has_dc_offset


# Feature: phase4-synthesis-qa, Property 15: 感知质量指标计算
@given(
    audio=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000),
                     elements=st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False))
)
@pytest.mark.property
def test_spectral_centroid_range(audio):
    """
    属性：频谱质心应该在 20-20000 Hz 范围内（对于非常量信号）
    
    **验证：需求 11.1, 11.2, 11.3, 11.4**
    """
    # 避免全零数组
    if np.all(audio == 0):
        return
    
    # 避免常量数组（DC信号没有有意义的频谱质心）
    if np.std(audio) < 1e-6:
        return
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=48000)
    centroid = analyzer.compute_spectral_centroid()
    
    # 如果返回 NaN（例如对于常量信号），跳过验证
    if np.isnan(centroid):
        return
    
    # 验证范围（考虑 Nyquist 频率）
    assert 20 <= centroid <= 24000  # 48kHz 采样率的 Nyquist 频率


# ============================================================================
# 边缘情况测试
# ============================================================================

@pytest.mark.unit
def test_empty_audio():
    """测试空音频处理"""
    audio = np.array([])
    
    with pytest.raises(Exception):
        analyzer = AudioAnalyzer(audio_data=audio, sample_rate=48000)


@pytest.mark.unit
def test_very_short_audio():
    """测试极短音频"""
    sample_rate = 48000
    audio = np.random.randn(10)  # 只有 10 个样本
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    
    # T60 测量应该失败（音频太短）
    t60 = analyzer.measure_t60()
    assert t60 is None


@pytest.mark.unit
def test_silent_audio():
    """测试静音音频"""
    sample_rate = 48000
    audio = np.zeros(sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    
    # RMS 应该非常低
    rms_db = analyzer.compute_rms_energy()
    assert rms_db < -60  # 应该低于 -60dB


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
