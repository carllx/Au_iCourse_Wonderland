"""
伪影检测测试
============

测试 AudioAnalyzer 的伪影检测功能。

验证需求：6.1, 6.2, 6.3, 6.4, 6.5
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
ARTIFACT_THRESHOLDS = config.ARTIFACT_THRESHOLDS


# ============================================================================
# 单元测试 - 削波检测
# ============================================================================

@pytest.mark.unit
def test_detect_clipping_positive():
    """测试削波检测 - 正向削波"""
    sample_rate = 48000
    
    # 生成有削波的音频（正向）
    audio = np.array([0.5, 0.8, 1.0, 1.0, 0.9, 0.6])
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_clipping, locations = analyzer.detect_clipping()
    
    # 验证检测到削波
    assert has_clipping
    assert len(locations) == 2  # 两个样本削波（索引 2 和 3）
    
    # 验证位置正确
    expected_times = [2 / sample_rate, 3 / sample_rate]
    assert locations == pytest.approx(expected_times, abs=1e-6)


@pytest.mark.unit
def test_detect_clipping_negative():
    """测试削波检测 - 负向削波"""
    sample_rate = 48000
    
    # 生成有削波的音频（负向）
    audio = np.array([0.5, -0.8, -1.0, -1.0, -0.9, 0.6])
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_clipping, locations = analyzer.detect_clipping()
    
    # 验证检测到削波
    assert has_clipping
    assert len(locations) == 2  # 两个样本削波


@pytest.mark.unit
def test_detect_clipping_stereo():
    """测试削波检测 - 立体声"""
    sample_rate = 48000
    
    # 生成立体声音频，左声道有削波
    left = np.array([0.5, 0.8, 1.0, 0.9, 0.6])
    right = np.array([0.3, 0.4, 0.5, 0.6, 0.7])
    stereo = np.stack([left, right], axis=1)
    
    analyzer = AudioAnalyzer(audio_data=stereo, sample_rate=sample_rate)
    has_clipping, locations = analyzer.detect_clipping()
    
    # 验证检测到削波（左声道）
    assert has_clipping
    assert len(locations) == 1  # 一个样本削波


@pytest.mark.unit
def test_no_clipping():
    """测试削波检测 - 无削波"""
    sample_rate = 48000
    
    # 生成无削波的音频
    audio = np.array([0.5, 0.8, 0.95, 0.9, 0.6])
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_clipping, locations = analyzer.detect_clipping()
    
    # 验证未检测到削波
    assert not has_clipping
    assert len(locations) == 0


# ============================================================================
# 单元测试 - 直流偏移检测
# ============================================================================

@pytest.mark.unit
def test_detect_dc_offset_positive():
    """测试直流偏移检测 - 正向偏移"""
    sample_rate = 48000
    
    # 生成有正向直流偏移的音频
    audio = np.random.randn(sample_rate) * 0.1 + 0.5  # 偏移 +0.5
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_offset, offset_value = analyzer.detect_dc_offset()
    
    # 验证检测到偏移
    assert has_offset
    assert offset_value == pytest.approx(0.5, abs=0.05)


@pytest.mark.unit
def test_detect_dc_offset_negative():
    """测试直流偏移检测 - 负向偏移"""
    sample_rate = 48000
    
    # 生成有负向直流偏移的音频
    audio = np.random.randn(sample_rate) * 0.1 - 0.3  # 偏移 -0.3
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_offset, offset_value = analyzer.detect_dc_offset()
    
    # 验证检测到偏移
    assert has_offset
    assert offset_value == pytest.approx(-0.3, abs=0.05)


@pytest.mark.unit
def test_no_dc_offset():
    """测试直流偏移检测 - 无偏移"""
    sample_rate = 48000
    
    # 生成无直流偏移的音频（零均值）
    audio = np.random.randn(sample_rate) * 0.5
    audio = audio - np.mean(audio)  # 确保零均值
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_offset, offset_value = analyzer.detect_dc_offset()
    
    # 验证未检测到偏移
    assert not has_offset
    assert abs(offset_value) < ARTIFACT_THRESHOLDS["dc_offset"]


# ============================================================================
# 单元测试 - 不连续性检测
# ============================================================================

@pytest.mark.unit
def test_detect_discontinuities():
    """测试不连续性检测 - 有不连续"""
    sample_rate = 48000
    
    # 生成有不连续的音频（突然跳跃）
    audio = np.zeros(100)
    audio[50] = 0.5  # 突然跳跃到 0.5
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_disc, locations = analyzer.detect_discontinuities()
    
    # 验证检测到不连续
    assert has_disc
    assert len(locations) > 0


@pytest.mark.unit
def test_detect_discontinuities_click():
    """测试不连续性检测 - 咔嗒声"""
    sample_rate = 48000
    
    # 生成有咔嗒声的音频
    audio = np.sin(2 * np.pi * 440 * np.arange(1000) / sample_rate) * 0.5
    audio[500] = 0.8  # 插入咔嗒声
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_disc, locations = analyzer.detect_discontinuities()
    
    # 验证检测到不连续
    assert has_disc


@pytest.mark.unit
def test_no_discontinuities():
    """测试不连续性检测 - 无不连续"""
    sample_rate = 48000
    
    # 生成平滑的正弦波（无不连续）
    audio = np.sin(2 * np.pi * 440 * np.arange(1000) / sample_rate) * 0.5
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_disc, locations = analyzer.detect_discontinuities()
    
    # 验证未检测到不连续
    assert not has_disc
    assert len(locations) == 0


# ============================================================================
# 单元测试 - 混叠检测
# ============================================================================

@pytest.mark.unit
def test_detect_aliasing():
    """测试混叠检测 - 有混叠"""
    sample_rate = 48000
    nyquist = sample_rate / 2
    
    # 生成高频信号（接近 Nyquist 频率）
    # 这会产生混叠伪影
    freq = nyquist * 0.95  # 95% Nyquist
    audio = np.sin(2 * np.pi * freq * np.arange(10000) / sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_aliasing = analyzer.detect_aliasing()
    
    # 验证检测到混叠
    assert has_aliasing


@pytest.mark.unit
def test_no_aliasing():
    """测试混叠检测 - 无混叠"""
    sample_rate = 48000
    
    # 生成低频信号（远离 Nyquist 频率）
    freq = 440  # 440 Hz
    audio = np.sin(2 * np.pi * freq * np.arange(10000) / sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_aliasing = analyzer.detect_aliasing()
    
    # 验证未检测到混叠
    assert not has_aliasing


# ============================================================================
# 单元测试 - 综合伪影检测
# ============================================================================

@pytest.mark.unit
def test_detect_artifacts_comprehensive():
    """测试综合伪影检测"""
    sample_rate = 48000
    
    # 生成有多种伪影的音频
    audio = np.random.randn(sample_rate) * 0.3 + 0.2  # 直流偏移
    audio[100] = 1.0  # 削波
    audio[200] = 0.8  # 不连续
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    artifacts = analyzer.detect_artifacts()
    
    # 验证检测到多种伪影
    assert artifacts.has_clipping
    assert artifacts.has_dc_offset
    assert artifacts.has_discontinuities
    
    # 验证报告结构
    assert isinstance(artifacts, ArtifactReport)
    assert isinstance(artifacts.clipping_locations, list)
    assert isinstance(artifacts.discontinuity_locations, list)


@pytest.mark.unit
def test_detect_artifacts_clean():
    """测试综合伪影检测 - 干净音频"""
    sample_rate = 48000
    
    # 生成干净的音频（无伪影）
    audio = np.sin(2 * np.pi * 440 * np.arange(sample_rate) / sample_rate) * 0.5
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    artifacts = analyzer.detect_artifacts()
    
    # 验证未检测到伪影
    assert not artifacts.has_clipping
    assert not artifacts.has_dc_offset
    assert not artifacts.has_discontinuities
    assert not artifacts.has_aliasing


# ============================================================================
# 属性测试
# ============================================================================

# Feature: phase4-synthesis-qa, Property 6: 伪影综合检测
@given(
    audio=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000),
                     elements=st.floats(min_value=-0.8, max_value=0.8, 
                                       allow_nan=False, allow_infinity=False))
)
@pytest.mark.property
def test_artifact_detection_no_false_positives(audio):
    """
    属性：对于正常音频（无伪影），不应该误报削波
    
    **验证：需求 6.1, 6.2, 6.3, 6.4, 6.5**
    """
    # 确保音频在正常范围内（无削波）
    # 使用更保守的范围以避免在移除均值后超过阈值
    audio = np.clip(audio, -0.8, 0.8)
    
    # 移除直流偏移（但要确保不会导致削波）
    mean_val = np.mean(audio)
    audio = audio - mean_val
    
    # 再次裁剪以确保在安全范围内
    audio = np.clip(audio, -0.9, 0.9)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=48000)
    artifacts = analyzer.detect_artifacts()
    
    # 验证不应该检测到削波（因为我们限制在 ±0.9）
    assert not artifacts.has_clipping
    
    # 验证不应该检测到直流偏移（因为我们移除了）
    assert not artifacts.has_dc_offset


# Feature: phase4-synthesis-qa, Property 6: 伪影综合检测
@given(
    audio=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000),
                     elements=st.floats(min_value=-1.0, max_value=1.0, 
                                       allow_nan=False, allow_infinity=False))
)
@pytest.mark.property
def test_clipping_detection_accuracy(audio):
    """
    属性：如果音频包含 ≥0.99 或 ≤-0.99 的样本，应该检测到削波
    
    **验证：需求 6.1, 6.5**
    """
    # 强制添加削波样本
    if len(audio) > 10:
        audio[5] = 1.0  # 添加削波
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=48000)
    has_clipping, locations = analyzer.detect_clipping()
    
    # 验证检测到削波
    assert has_clipping
    assert len(locations) > 0


# Feature: phase4-synthesis-qa, Property 6: 伪影综合检测
@given(
    offset=st.floats(min_value=0.05, max_value=0.5),
    noise_level=st.floats(min_value=0.01, max_value=0.1)
)
@pytest.mark.property
def test_dc_offset_detection_accuracy(offset, noise_level):
    """
    属性：如果音频有显著直流偏移（>0.01），应该检测到
    
    **验证：需求 6.2, 6.5**
    """
    sample_rate = 48000
    
    # 生成有直流偏移的音频
    audio = np.random.randn(sample_rate) * noise_level + offset
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    has_offset, offset_value = analyzer.detect_dc_offset()
    
    # 验证检测到偏移
    assert has_offset
    # 验证偏移值接近预期
    assert abs(offset_value - offset) < noise_level * 3  # 3-sigma 容差


# ============================================================================
# 边缘情况测试
# ============================================================================

@pytest.mark.unit
def test_artifact_detection_empty_audio():
    """测试伪影检测 - 空音频"""
    audio = np.array([])
    
    # 空数组应该能够创建分析器，但某些操作可能失败
    # 这是一个边缘情况，我们只验证不会崩溃
    try:
        analyzer = AudioAnalyzer(audio_data=audio, sample_rate=48000)
        # 如果成功创建，验证时长为0
        assert analyzer.duration == 0.0
    except (ValueError, IndexError, ZeroDivisionError):
        # 这些异常都是可接受的
        pass


@pytest.mark.unit
def test_artifact_detection_silent_audio():
    """测试伪影检测 - 静音音频"""
    sample_rate = 48000
    audio = np.zeros(sample_rate)
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    artifacts = analyzer.detect_artifacts()
    
    # 静音音频不应该有伪影（除了可能的直流偏移为零）
    assert not artifacts.has_clipping
    assert not artifacts.has_discontinuities
    assert not artifacts.has_aliasing


@pytest.mark.unit
def test_artifact_detection_constant_audio():
    """测试伪影检测 - 常数音频"""
    sample_rate = 48000
    audio = np.ones(sample_rate) * 0.5
    
    analyzer = AudioAnalyzer(audio_data=audio, sample_rate=sample_rate)
    artifacts = analyzer.detect_artifacts()
    
    # 常数音频应该有直流偏移，但无其他伪影
    assert artifacts.has_dc_offset
    assert not artifacts.has_clipping
    assert not artifacts.has_discontinuities


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
