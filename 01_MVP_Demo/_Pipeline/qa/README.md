# Phase 4 合成质量保证系统

自动化验证、诊断和改进 Phase 4（定位）音频合成的质量保证工具包。

## 概述

本 QA 系统提供全面的质量保证功能，用于验证 Phase 4 音频合成的质量，包括：

- **音频分析**：声学指标（T60, C80, EDT）、频谱分析、立体声成像、伪影检测
- **脚本分析**：参数提取、范围验证、算法检测、处理顺序验证
- **心理声学验证**：生物拟真性、威胁音频、空间分离、感知影响评估
- **诊断报告**：Markdown/JSON 格式报告、可视化、修复建议

## 快速开始

### 安装依赖

```bash
cd 01_MVP_Demo/_Pipeline/qa
pip install -r requirements.txt
```

### 基本使用

```python
from qa import AudioAnalyzer, ScriptAnalyzer, PsychoacousticValidator

# 1. 分析音频文件
analyzer = AudioAnalyzer(audio_path="path/to/audio.wav")

# 获取声学指标
metrics = analyzer.get_acoustic_metrics()
print(f"T60: {metrics.t60}s")
print(f"立体声相关性: {metrics.stereo_correlation}")

# 检测伪影
artifacts = analyzer.detect_artifacts()
if artifacts.has_clipping:
    print(f"检测到削波: {len(artifacts.clipping_locations)} 处")

# 2. 分析生成器脚本
script_analyzer = ScriptAnalyzer(script_path="path/to/generator.py")

# 提取参数
params = script_analyzer.extract_parameters()
print(f"提取的参数: {params}")

# 验证参数范围
issues = script_analyzer.validate_parameter_ranges()
for issue in issues:
    print(issue)

# 3. 心理声学验证
validator = PsychoacousticValidator(audio_path="path/to/heartbeat.wav")

# 验证心跳生物拟真性
result = validator.validate_heartbeat_biofidelity()
print(f"生物拟真性得分: {result['biofidelity_score']:.2f}")
```

## 核心模块

### AudioAnalyzer

音频分析引擎，提供以下功能：

- **声学指标测量**：`measure_t60()`, `measure_c80()`, `measure_edt()`, `measure_pre_delay()`
- **立体声分析**：`compute_stereo_correlation()`, `estimate_stereo_width()`, `detect_pan_position()`
- **频谱分析**：`compute_psd()`, `compute_spectral_centroid()`, `analyze_octave_bands()`
- **伪影检测**：`detect_clipping()`, `detect_dc_offset()`, `detect_discontinuities()`, `detect_aliasing()`

### ScriptAnalyzer

脚本分析引擎，提供以下功能：

- **参数提取**：`extract_parameters()` - 使用 AST 解析提取配置参数
- **参数验证**：`validate_parameter_ranges()` - 验证参数是否在合理范围内
- **算法检测**：`detect_algorithm_issues()` - 检测 Voss-McCartney、频率相关衰减等
- **处理顺序验证**：`validate_processing_order()` - 验证处理步骤顺序
- **修复建议**：`generate_fix_suggestions()` - 生成代码级别的修复建议

### PsychoacousticValidator

心理声学验证器，提供以下功能：

- **心跳验证**：`validate_heartbeat_biofidelity()` - 检测 sine_sweep 和低通滤波
- **威胁音频验证**：`validate_threat_audio()` - 检测 3000Hz 和尖锐包络
- **空间分离验证**：`validate_spatial_separation()` - 验证内/外声像分离
- **感知影响评估**：`assess_perceptual_impact()` - 评估明亮度、黑暗度、焦虑值

## 项目结构

```
01_MVP_Demo/_Pipeline/qa/
├── __init__.py                    # 包初始化
├── config.py                      # 配置和数据模型
├── audio_analyzer.py              # 音频分析引擎
├── script_analyzer.py             # 脚本分析引擎
├── psychoacoustic_validator.py    # 心理声学验证器
├── requirements.txt               # 依赖列表
├── pytest.ini                     # Pytest 配置
├── README.md                      # 本文件
└── tests/                         # 测试套件
    ├── __init__.py
    ├── test_audio_analyzer.py     # 音频分析器测试
    ├── test_script_analyzer.py    # 脚本分析器测试
    └── test_psychoacoustic.py     # 心理声学验证器测试
```

## 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/ -m unit

# 运行属性测试
pytest tests/ -m property

# 运行集成测试
pytest tests/ -m integration

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

## 配置

### 参数合理范围

在 `config.py` 中定义了参数的合理范围：

```python
PARAMETER_RANGES = {
    "t60": (0.1, 10.0),           # 秒
    "pre_delay_ms": (0, 200),     # 毫秒
    "stereo_width": (0, 200),     # 百分比
    "sample_rate": (44100, 96000), # Hz
    "bit_depth": (16, 24),        # bits
}
```

### 立体声相关性阈值

```python
STEREO_CORRELATION_THRESHOLDS = {
    "mono": 0.95,  # > 0.95 认为是单声道/居中
    "wide": 0.5,   # < 0.5 认为是宽立体声
}
```

### 伪影检测阈值

```python
ARTIFACT_THRESHOLDS = {
    "clipping": 0.99,        # 样本值 >= 0.99 认为是削波
    "dc_offset": 0.01,       # |平均值| > 0.01 认为有直流偏移
    "discontinuity": 0.1,    # 相邻样本差 > 0.1 认为是不连续
}
```

## 示例

### 示例 1：验证虚空 IR

```python
from qa import AudioAnalyzer

# 加载虚空 IR
analyzer = AudioAnalyzer(audio_path="_Library/S04_Space/asset_S04_void_ir.wav")

# 测量 T60
t60 = analyzer.measure_t60()
print(f"T60: {t60:.2f}s")

# 验证 T60 是否符合要求（≥ 5.0s）
if t60 >= 5.0:
    print("✓ T60 符合虚空空间要求")
else:
    print(f"✗ T60 {t60:.2f}s 低于要求（应 ≥ 5.0s）")

# 测量立体声宽度
width = analyzer.estimate_stereo_width()
print(f"立体声宽度: {width:.1f}%")

# 验证立体声宽度是否符合要求（≥ 150%）
if width >= 150:
    print("✓ 立体声宽度符合虚空空间要求")
else:
    print(f"✗ 立体声宽度 {width:.1f}% 低于要求（应 ≥ 150%）")
```

### 示例 2：分析生成器脚本

```python
from qa import ScriptAnalyzer

# 分析脚本
analyzer = ScriptAnalyzer(script_path="_Pipeline/generators/gen_S04_void_ir.py")

# 提取参数
params = analyzer.extract_parameters()
print("提取的参数:")
for config_name, config_dict in params.items():
    print(f"\n{config_name}:")
    for key, value in config_dict.items():
        print(f"  {key}: {value}")

# 验证参数范围
issues = analyzer.validate_parameter_ranges()
if issues:
    print("\n参数问题:")
    for issue in issues:
        print(f"  {issue}")
else:
    print("\n✓ 所有参数在合理范围内")

# 检测算法问题
algo_issues = analyzer.detect_algorithm_issues()
if algo_issues:
    print("\n算法问题:")
    for issue in algo_issues:
        print(f"  {issue}")
        if issue.fix_suggestion:
            print(f"    修复建议: {issue.fix_suggestion}")
else:
    print("\n✓ 算法实现正确")
```

### 示例 3：验证心跳生物拟真性

```python
from qa import PsychoacousticValidator

# 加载心跳音频
validator = PsychoacousticValidator(audio_path="_Library/S02_Heartbeat/asset_S02_heartbeat.wav")

# 验证生物拟真性
result = validator.validate_heartbeat_biofidelity()

print(f"生物拟真性得分: {result['biofidelity_score']:.2f}")
print(f"Sine sweep 检测: {'✓' if result['has_sine_sweep'] else '✗'}")
print(f"低通滤波检测: {'✓' if result['has_lowpass_filter'] else '✗'}")
print(f"高频衰减: {result['high_freq_attenuation_db']:.1f} dB")

if result['issues']:
    print("\n问题:")
    for issue in result['issues']:
        print(f"  • {issue}")
```

## 开发指南

### 添加新的验证功能

1. 在相应的模块中添加新方法
2. 更新 `config.py` 中的数据模型（如需要）
3. 编写单元测试和属性测试
4. 更新文档

### 编写测试

#### 单元测试示例

```python
import pytest
from qa import AudioAnalyzer
import numpy as np

@pytest.mark.unit
def test_measure_t60_known_ir():
    """测试 T60 测量的准确性（已知 IR）"""
    # 生成已知 T60 = 2.0s 的 IR
    sample_rate = 48000
    duration = 5.0
    t60 = 2.0
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    alpha = -np.log(0.001) / t60
    ir = np.exp(-t * alpha) * np.random.randn(len(t))
    
    analyzer = AudioAnalyzer(audio_data=ir, sample_rate=sample_rate)
    measured_t60 = analyzer.measure_t60()
    
    # 验证测量值在 ±10% 范围内
    assert 1.8 <= measured_t60 <= 2.2
```

#### 属性测试示例

```python
from hypothesis import given, strategies as st
import hypothesis.extra.numpy as npst

# Feature: phase4-synthesis-qa, Property 2: 立体声成像一致性
@given(
    left=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000)),
    right=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000))
)
@pytest.mark.property
def test_stereo_correlation_range(left, right):
    """属性：立体声相关系数应该在 [-1, 1] 范围内"""
    min_len = min(len(left), len(right))
    left = left[:min_len]
    right = right[:min_len]
    
    stereo = np.stack([left, right], axis=1)
    analyzer = AudioAnalyzer(audio_data=stereo, sample_rate=48000)
    
    correlation = analyzer.compute_stereo_correlation()
    
    assert -1.0 <= correlation <= 1.0
```

## 参考

- **设计文档**: `.kiro/specs/phase4-synthesis-qa/design.md`
- **需求文档**: `.kiro/specs/phase4-synthesis-qa/requirements.md`
- **任务列表**: `.kiro/specs/phase4-synthesis-qa/tasks.md`
- **IR 合成改进规范**: `.kiro/specs/ir-synthesis-improvement/`

## 许可

本项目是爱丽丝声音剧场项目的一部分。

## 版本历史

- **v1.0.0** (2024): 初始版本
  - 音频分析引擎
  - 脚本分析引擎
  - 心理声学验证器
  - 基础测试框架
